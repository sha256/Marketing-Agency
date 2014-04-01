from django.db import models

__author__ = 'sha256'


class Television(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        app_label = "magency"


class Program(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(Television, db_column="tv_id", verbose_name="Television")

    class Meta:
        app_label = "magency"