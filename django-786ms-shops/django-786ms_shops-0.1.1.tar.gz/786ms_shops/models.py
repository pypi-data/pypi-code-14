from __future__ import unicode_literals

from django.db import models

class Shop(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    location=models.CharField(max_length=50)

class SaleEntry(models.Model):
    shop=models.ForeignKey(Shop)
    amount=models.FloatField(default=0.0)
    description=models.CharField(max_length=100)
    notes=models.CharField(max_length=500)
    timestamp=models.DateTimeField(auto_now=True,blank=False)
    class Meta:
        ordering = ['-timestamp']
