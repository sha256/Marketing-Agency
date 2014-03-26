from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from apps.auth.models.permission import Permission


class RoleManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


@python_2_unicode_compatible
class Role(models.Model):

    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission,
                                         verbose_name=_('permissions'), blank=True)

    objects = RoleManager()

    class Meta:
        app_label = "auth"
        permissions = (
            ("add_role", "Role.Add"),
            ("edit_role", "Role.Edit"),
            ("view_role", "Role.View"),
            ("delete_role", "Role.Delete")
        )

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)