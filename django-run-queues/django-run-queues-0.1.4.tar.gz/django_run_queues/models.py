from __future__ import unicode_literals
from picklefield.fields import PickledObjectField
from django.db import models

# Create your models here.
class DjangoRunQueue(models.Model):
    TaskName=models.CharField(max_length=100)
    TaskQueue= models.CharField(max_length=100)
    TaskArgs=PickledObjectField()
    TaskResults=PickledObjectField()
    Proccessed=models.BooleanField(default=False)
    def __str__(self):
        return self.TaskName