from django.contrib import admin

from veriport_dashboard.models import ReportFilter, SystemMessage


class ReportFilterAdmin(admin.ModelAdmin):
    """
    Admin view for :model:'veriport_dashboard.ReportFilter'
    """
    model = ReportFilter


class SystemMessageAdmin(admin.ModelAdmin):
    """
    Admin view for :model:'veriport_dashboard.SystemMessage'
    """
    model = SystemMessage


admin.site.register(ReportFilter, ReportFilterAdmin)
admin.site.register(SystemMessage, SystemMessageAdmin)
