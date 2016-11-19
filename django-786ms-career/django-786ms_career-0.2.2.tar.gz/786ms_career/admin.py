import hashlib
from django.contrib import admin

from .models import *

class QualificationInline(admin.TabularInline):
	model=Qualification
	extra=1
class ExperienceInline(admin.TabularInline):
	model=Experience
	extra=1
	
class UserAdmin(admin.ModelAdmin):
	inlines=[QualificationInline,ExperienceInline]
	list_display=('name','dob','get_qualification','get_experience')
	search_fields=['name']
	
class TokenAdmin(admin.ModelAdmin):
	list_display=('name','dob','token')
	search_fields=['token','name']
	
	def get_readonly_fields(self, request, obj = None):
		return ('token',)+self.readonly_fields
		
admin.site.register(User,UserAdmin)
admin.site.register(Token,TokenAdmin)
