from django.db import models

__author__ = 'sha256'


class Billboard(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    lat = models.FloatField()
    lng = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    is_led = models.BooleanField(default=False)

    class Meta:
        app_label = "magency"