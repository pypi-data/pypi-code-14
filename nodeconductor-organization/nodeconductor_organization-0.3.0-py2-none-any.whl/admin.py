from django.contrib import admin

from nodeconductor_organization.models import Organization, OrganizationUser


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'native_name', 'customer', 'uuid')
    list_filter = ('abbreviation', 'native_name')
    ordering = ('abbreviation', 'native_name', 'customer')


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'organization')
    list_filter = ('is_approved', 'user')
    ordering = ('user', 'is_approved', 'organization')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
