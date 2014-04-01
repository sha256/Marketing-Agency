from __future__ import unicode_literals
import re
from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.http import urlquote
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from apps.auth.models.role import Role
from apps.auth.models.permission import Permission



class UserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):

        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                         is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


@python_2_unicode_compatible
class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)

    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()


def _user_get_all_permissions(user_obj, obj=None):
    if user_obj.is_anonymous() or obj is not None:
        return set()
    if not hasattr(user_obj, '_perm_cache'):
        user_obj._perm_cache = set(["%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.role.permissions.all()])
        #user_obj._perm_cache.update(self.get_group_permissions(user_obj))
    return user_obj._perm_cache


def _user_has_perm(user_obj, perm, obj=None):
    if not user_obj.is_active:
        return False
    return perm in _user_get_all_permissions(user_obj, obj)


def _user_has_module_perms(user_obj, app_label):
    """
    Returns True if user_obj has any permissions in the given app_label.
    """
    if not user_obj.is_active:
        return False
    for perm in _user_get_all_permissions(user_obj):
        if perm[:perm.index('.')] == app_label:
            return True
    return False

SEX_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others'),
)

class ProfileMixin(models.Model):

    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    propic = models.ImageField(null=True, blank=True, upload_to='propics')
    password_reset = models.CharField(null=True, blank=True, max_length=128)
    password_reset_expire = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class PermissionsMixin(models.Model):

    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                                   'explicitly assigning them.'))
    #roles = models.ManyToManyField(Role, blank=True, verbose_name=_("groups"))
    #user_permissions = models.ManyToManyField(Permission, blank=True)
    role = models.ForeignKey(Role, blank=True, null=True)

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):

        return self.role.permissions.all()

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class User(AbstractBaseUser):

    username = models.CharField(_('username'), max_length=30, null=True, blank=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
                                ])
    name = models.CharField(max_length=200)

    is_superuser = models.BooleanField(default=False)

    email = models.EmailField(_('email address'), unique=True)

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(default=False)

    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'auth'
        permissions = (
            ("view_user", "User.View"),
            ("create_user", "User.Create"),
            ("delete_user", "User.Delete"),
            ("edit_user", "User.Edit")
        )

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
user_logged_in.connect(update_last_login)


class SiteProfileNotAvailable(Exception):
    pass