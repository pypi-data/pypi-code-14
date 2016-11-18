from django.contrib import admin


# Register your models here.
class AdminDisplay(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(AdminDisplay, self).__init__(model, admin_site)

