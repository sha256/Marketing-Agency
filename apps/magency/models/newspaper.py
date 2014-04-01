from django.db import models

__author__ = 'sha256'


class Newspaper(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        app_label = "magency"


class Section(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(Newspaper, db_column="newspaper_id", verbose_name="Newspaper")

    class Meta:
        app_label = "magency"