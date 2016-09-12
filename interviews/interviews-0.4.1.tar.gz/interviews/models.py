# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site

from .managers import InterviewManager


class Person(models.Model):
    SEX_CHOICES = (
        (1, _('Man')),
        (2, _('Woman')),
    )
    name = models.CharField(max_length=255)
    birthdate = models.DateField(blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES)
    about = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __unicode__(self):
        return self.name

    @property
    def age(self):
        if self.birthdate:
            today = datetime.date.today()
            return (today.year - self.birthdate.year) - int((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        else:
            return None


class Interview(models.Model):
    """
    """
    person = models.ForeignKey(Person)
    site = models.ForeignKey(Site, default=settings.SITE_ID)

    title = models.CharField(max_length=255)
    slug = models.SlugField()

    is_published = models.BooleanField(default=False)
    published_on = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    introduction = models.TextField(blank=True, null=True)
    footnotes = models.TextField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # place = models.TextField(blank=True, null=True)

    objects = InterviewManager()

    class Meta:
        ordering = ["-published_on"]
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('interviews-detail', [self.slug])

    @property
    def get_full_url(self):
        return "http://%s%s" % (self.site.domain, self.get_absolute_url())

    @property
    def answers(self):
        return Answer.objects.for_interview(self)

    @property
    def selected_picture(self):
        return Picture.objects.filter(interviewpicture__is_selected=True).get(interview=self)

    @property
    def preview_hash(self):
        return hashlib.md5("%s-%s-%s" % (self.id, self.slug, self.site_id)).hexdigest()


class Picture(models.Model):
    interview = models.ForeignKey(Interview)
    image = models.ImageField(upload_to='pictures')
    legend = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')

    def __unicode__(self):
        return "%s - %s (%s)" % (self.interview, self.image, self.legend)


class Answer(models.Model):
    interview = models.ForeignKey(Interview)
    order = models.IntegerField()
    question = models.TextField(blank=True)
    response = models.TextField(blank=True)
    related_pictures = models.ManyToManyField(Picture, blank=True)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        unique_together = (
            ('interview', 'order'),
        )
        ordering = ['order']

    def __unicode__(self):
        return u"%s Q. %s" % (self.interview, self.order)


class Quote(models.Model):
    related_to = models.ForeignKey(Answer, null=True, blank=True)
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    author = models.CharField(max_length=255)
    quote = models.TextField()

    class Meta:
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')

    def __unicode__(self):
        return u"%s : %s" % (self.author, self.quote)


class InterviewPicture(models.Model):
    interview = models.ForeignKey(Interview)
    picture = models.ForeignKey(Picture)
    is_selected = models.BooleanField(default=False)


# Product related
class Brand(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    brand = models.ForeignKey(Brand, blank=True, null=True)
    description = models.TextField(blank=True)
    alternate_titles = models.TextField(blank=True)
    amazon_url = models.URLField(blank=True, null=True)
    # Calculated field
    published_interviews_count = models.IntegerField(_('Published interviews'), default=0, editable=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('product-detail', [self.slug])

    @property
    def interviews_count(self):
        return Interview.objects.published().filter(products__product=self).count()

    @property
    def is_online(self):
        return self.published_interviews_count >= 4


class InterviewProduct(models.Model):
    interview = models.ForeignKey(Interview, related_name='products')
    product = models.ForeignKey(Product)


# Signals
@receiver(post_save, sender=InterviewProduct)
def update_published_interviews_count(sender, **kwargs):
    try:
        instance = kwargs['instance']
        instance.product.published_interviews_count = instance.product.interviews_count
        instance.product.save()
    except Exception, e:
        logging.error(str(e))
