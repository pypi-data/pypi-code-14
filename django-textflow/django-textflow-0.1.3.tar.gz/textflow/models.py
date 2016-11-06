# coding: utf-8

from django.db import models

__author__ = 'mhaze'


class FlowObject(models.Model):
    text = models.CharField(max_length=64)

    @staticmethod
    def serialize():
        flow_objects = FlowObject.objects.all()
        texts = ""

        for flow_object in flow_objects:
            if texts:
                texts += ',%s' % str(flow_object)

            else:
                texts = str(flow_object)

        return texts

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)
