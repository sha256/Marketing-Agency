from django.db import models

__author__ = 'sha256'


class Website(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=255)

    class Meta:
        app_label = "magency"