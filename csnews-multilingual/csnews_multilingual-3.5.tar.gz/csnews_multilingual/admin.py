from django.contrib import admin
from csnews_multilingual.models import Article
from django.conf import settings
from tinymce.widgets import TinyMCE
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _


def show_entry_thumbnail(item):
    if item.image:
        return item.image.admin_thumbnail()
    else:
        return None
    # return item.admin_thumbanail()
show_entry_thumbnail.short_description = 'Argazkia'
show_entry_thumbnail.allow_tags = True


class ArticleAdmin(TranslatableAdmin):
    def get_title(self, obj):
        return obj.safe_translation_getter('title')
    get_title.short_description = _('Title')

    list_display = ('id', 'get_title', 'published', 'is_public', show_entry_thumbnail, 'all_translations')
    list_display_links = ('id', 'get_title')
    ordering = ('-id',)
    search_fields = ['title', 'summary']
    # prepopulated_fields = {'slug': ('title_eu',)}
    photologue_image_fields = ('image',)
    # raw_id_fields = ('image',)
    # form = ArticleAdminForm

    use_fieldsets = (
        (_("Language dependent"), {
            'fields': ('title', 'summary', 'body'),
        }),
        (_("Common"), {
            'fields': ('slug', 'published', 'image', 'is_public'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets


class TinyMCEArticleAdmin(ArticleAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('body', 'summary'):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={settings.TINYMCE_DEFAULT_CONFIG},
            ))
        return super(TinyMCEArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Article, ArticleAdmin)
