from django.db import models

__author__ = 'sha256'


class Television(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        app_label = "magency"


class Program(models.Model):
    title = models.CharField(max_length=200)
    tv = models.ForeignKey(Television)

    class Meta:
        app_label = "magency"