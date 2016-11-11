# -*- coding: utf-8 -*-
"""
=======================
Django model definition
=======================
"""
import requests
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from djmessenger.utils.serializable import Serializable
from djmessenger.exceptions import DJMInvalidConfigException


logger = logging.getLogger(__name__)


class Messaging(models.Model):
    """
    A table to store :class:`djmessenger.receiving.Messaging`
    """
    body = models.TextField()
    type = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'djm_messaging'


class Reply(models.Model):
    """
    A table to store all replies
    """
    recipient = models.ForeignKey('FBUserProfile')
    date_sent = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    type = models.CharField(max_length=128, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'djm_reply'


class FBUserProfile(models.Model):
    """
    This FBUserProfile class is to represent a user that sent a message to us
    via Facebook Messenger, from the message relayed by Facebook, we can look
    up user details which will be stored here
    """
    psid = models.CharField(max_length=512, primary_key=True)
    first_name = models.CharField('first name', max_length=512, null=True,
                                  blank=True)
    last_name = models.CharField('last name', max_length=512, null=True,
                                 blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    locale = models.CharField(max_length=128, null=True, blank=True)
    timezone = models.SmallIntegerField()
    gender = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    thumbups = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'djm_user'


class UserLocation(models.Model):
    """
    From the message user sent via Facebook to us, addition to saving the raw
    request body into RawBody, we try to see if the sent message is actually a
    location that contains lat and long, if yes, then we save it here
    """
    user = models.ForeignKey(FBUserProfile, null=False, blank=False)
    latitude = models.DecimalField(max_digits=10,
                                   decimal_places=8,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=11,
                                    decimal_places=8,
                                    null=True, blank=True)
    timestamp = models.BigIntegerField(
        help_text='Facebook returns timestamp as EPOCH')
    url = models.URLField(max_length=1000, null=True, blank=True)
    mid = models.CharField(max_length=512, null=True, blank=True)
    seq = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.date_created = datetime.utcnow().replace(tzinfo=utc)
    #     super().save(*args, **kwargs)

    class Meta:
        get_latest_by = 'date_created'
        db_table = 'djm_userlocation'

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%s(%s, %s)' % (self.user, self.latitude, self.longitude)
