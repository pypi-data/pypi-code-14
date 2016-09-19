"""
Envar models.
"""
import json
import random
import hashlib
import base64
import rsa
from django.db import models
from django.conf import settings
from django_memdb.mixins import PeristentInMemoryDB
from ..tools import codec

def is_empty(value):
    "Test if value is empty."
    if value is None or len(value) == 0:
        return True
    return False

# pylint: disable=too-many-instance-attributes, no-member
class Environment(models.Model, PeristentInMemoryDB):
    "A single environment instance."
    label = models.CharField(max_length=64, default='', blank=True)
    store = models.URLField(blank=True)
    ident = models.CharField(max_length=56, unique=True, blank=True)
    envar = models.TextField(blank=True)

    def __str__(self):
        return self.ident + ' | ' + self.label

    def save(self, *args, **kwargs):
        "override save."
        if is_empty(self.store):
            self.store = settings.DEFAULT_SERVER

        if is_empty(self.envar):
            _, key = rsa.newkeys(settings.RSA_KEYSIZE)
            self.ident, self.envar = codec.encode_key(key, self.store)

        return models.Model.save(self, *args, **kwargs)

    def resolve_inheritance(self):
        "Resolve inheritance, break if there is a recursion."
        # First get a line of inheritance
        inheritance = list()
        workon = self
        while True:
            inheritance.append(workon)

            if not hasattr(workon, 'offspring'):
                break

            workon = workon.offspring.ascendant
            if workon in inheritance:
                break

        return inheritance

    def get_variables(self):
        "Return all variables"
        tmp = dict()
        inheritances = self.resolve_inheritance()
        inheritances.reverse()
        for environment in inheritances:
            for variable in environment.variable_set.all():
                tmp[variable.key.key] = variable.value

        return tmp

    def add_variable(self, key, value):
        "Add a variable associated to this environment"
        key = Key.objects.get_or_create(key=key)[0]
        var = Variable.objects.create(environment=self, key=key, value=value)
        return key, var



class Key(models.Model, PeristentInMemoryDB):
    "Key, well it is a key."
    key = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.key


class Variable(models.Model, PeristentInMemoryDB):
    "The variable."
    environment = models.ForeignKey(Environment)
    key = models.ForeignKey(Key)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        _ = self.environment.label + ' | ' + self.key.key + ' | ' + self.value
        return  _


class Inheritance(models.Model, PeristentInMemoryDB):
    "Inheritance of Environments."
    # No multiple inheritance, offspring can only have one parent (ascendant).
    offspring = models.OneToOneField(Environment, related_name='offspring')
    ascendant = models.ForeignKey(Environment, related_name='ascendant')

    def __str__(self):
        return self.offspring.label + '<' + self.ascendant.label

