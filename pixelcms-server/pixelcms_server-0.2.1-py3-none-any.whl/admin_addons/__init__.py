from django.contrib import admin

from . import actions

default_app_config = 'cms.admin_addons.apps.AdminAddonsConfig'
admin.site.add_action(actions.duplicate)
