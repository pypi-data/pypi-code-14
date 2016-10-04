from django.contrib import admin

from publishing.models import PublishingProfile, PublishingRegion, PublishingLanguage, PublishingCountry, \
    PublishingProfileRegion


class ProfileRegionInlines(admin.TabularInline):
    model = PublishingProfileRegion
    extra = 0


class PublishingProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileRegionInlines]


class PublishingRegionAdmin(admin.ModelAdmin):
    pass


class PublishingLanguageAdmin(admin.ModelAdmin):
    pass


class PublishingCountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(PublishingProfile, PublishingProfileAdmin)
admin.site.register(PublishingRegion, PublishingRegionAdmin)
admin.site.register(PublishingLanguage, PublishingLanguageAdmin)
admin.site.register(PublishingCountry, PublishingCountryAdmin)