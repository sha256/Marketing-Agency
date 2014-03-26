from django.db import models
from apps.auth.models import User
from apps.magency.models.bill import Bill
from apps.magency.models.billboard import Billboard
from apps.magency.models.website import Website
from apps.magency.models.newspaper import Section
from apps.magency.models.tv import Program

__author__ = 'sha256'


class Advertisement(models.Model):
    company = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    validity = models.DateField()
    media = models.FileField(upload_to="files", null=True, blank=True)
    bill = models.ForeignKey(Bill)

    class Meta:
        app_label = "magency"


class NewspaperAd(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    width = models.FloatField()
    height = models.FloatField()
    color = models.BooleanField()
    newspapers = models.ManyToManyField(Section)

    class Meta:
        app_label = "magency"


class TelevisionAd(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    duration = models.IntegerField()
    programs = models.ManyToManyField(Program)

    class Meta:
        app_label = "magency"


class BillboardAd(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    billboards = models.ManyToManyField(Billboard)

    class Meta:
        app_label = "magency"


class WebsiteAd(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    websites = models.ManyToManyField(Website)

    class Meta:
        app_label = "magency"
