# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Interview, Answer, Quote, Person, Brand
from .models import Picture, Product, InterviewProduct, InterviewPicture
from .forms import FilterPictureForm


# Inline
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    form = FilterPictureForm


class InterviewPictureInline(admin.TabularInline):
    model = InterviewPicture
    extra = 4


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'about')
    list_filter = ('sex',)


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'published_on', 'is_published', 'site', 'preview_link')
    list_filter = ('site', 'published_on', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'published_on'
    ordering = ('is_published', '-published_on')
    search_fields = ['title', 'description']
    inlines = (AnswerInline, InterviewPictureInline)
    save_on_top = True

    def preview_link(self, obj):
        preview_url = reverse('interviews-preview', args=[obj.preview_hash, obj.slug])
        return '<a href="%s">Preview</a>' % (preview_url,)
    preview_link.short_description = _(u'Preview')
    preview_link.allow_tags = True


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'quote')


class PictureAdmin(admin.ModelAdmin):
    list_display = ('image_filename', 'interview', 'legend_as_html')
    list_filter = ('interview',)

    def image_filename(self, obj):
        return unicode(obj.image)

    def legend_as_html(self, obj):
        return obj.legend
    legend_as_html.allow_tags = True


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'brand', 'slug', 'published_interviews_count',
        'is_online', 'preview_link')
    list_filter = ('published_interviews_count', 'brand')
    prepopulated_fields = {"slug": ("title",)}
    actions = ['update_published_interviews_count']

    def preview_link(self, obj):
        product_preview_url = reverse('product-detail', args=[obj.slug])
        return '<a href="%s">Preview</a>' % (product_preview_url,)
    preview_link.short_description = _(u'Preview')
    preview_link.allow_tags = True

    def is_online(self, obj):
        return obj.is_online
    is_online.boolean = True

    def update_published_interviews_count(self, request, queryset):
        for product in queryset:
            product.published_interviews_count = product.interviews_count
            product.save()
    update_published_interviews_count.short_description = _(u"Recount the published interviews for the product")


class InterviewProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'interview')
    list_filter = ('product', 'interview')

admin.site.register(Person, PersonAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(InterviewProduct, InterviewProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
