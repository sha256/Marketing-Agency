from django.db import models

__author__ = 'sha256'

PAY_CHOICES = (
    ('cheque', 'Cheque'),
    ('cash', 'Cash'),
    ('paypal', 'Paypal'),
    ('bikash', 'Bikash'),
    ('other', 'Other')
)


class Bill(models.Model):
    ammount = models.FloatField()
    paid_by = models.CharField(max_length=200, choices=PAY_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=500)

    class Meta:
        app_label = "magency"