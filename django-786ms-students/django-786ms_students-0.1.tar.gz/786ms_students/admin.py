from django.contrib import admin
from .models import *

class StudentTokenAdmin(admin.ModelAdmin):
	list_display=['token','name','datetime','by']

class StudentAdmin(admin.ModelAdmin):
	list_display=['get_name','get_username','get_email','get_img_tag']

admin.site.register(Student,StudentAdmin)
admin.site.register(Course)
admin.site.register(StudentToken,StudentTokenAdmin)
