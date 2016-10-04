from django.contrib import admin

from blog.models import Blog, Category, Tag
from publishing.mixins import PublishAdminMixin


class CategoryAdmin(admin.ModelAdmin):
    pass


class TagInlines(PublishAdminMixin, admin.TabularInline):
    model = Tag
    extra = 0


class BlogAdmin(PublishAdminMixin, admin.ModelAdmin):
    inlines = [TagInlines, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
