__author__ = 'Mahmud'

from django.db import models
from datetime import datetime
import json


class DomainEntity(models.Model):

    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    # following creates an error in django-debug-toolbar
    # def __repr__(self):
    #     return json.dumps(self.__dict__)

    def save(self, *args, **kwargs):

        if self.date_created is None:
            self.date_created = datetime.now()
        self.last_updated = datetime.now()
        super(DomainEntity, self).save(*args, **kwargs)

    class Meta:
        abstract = True