from django.contrib import admin
import models


class ChartMetricInlineAdmin(admin.TabularInline):
    model = models.ChartMetric
    fk_name = 'chart'
    extra = 1


class ChartAuthPermissionInlineAdmin(admin.TabularInline):
    model = models.ChartAuthPermission
    fk_name = 'chart'
    extra = 1


class ChartAuthGroupInlineAdmin(admin.TabularInline):
    model = models.ChartAuthGroup
    fk_name = 'chart'
    extra = 1


class ChartGroupInlineAdmin(admin.TabularInline):
    model = models.ChartGroup
    fk_name = 'chart'
    extra = 1


class ChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'library', 'chart_type', 'priority', 'grid_width',
                    'height', 'group')
    inlines = [
        ChartMetricInlineAdmin, ChartAuthPermissionInlineAdmin,
        ChartAuthGroupInlineAdmin, ChartGroupInlineAdmin
    ]

    def group(self, instance):
        chart_groups = models.ChartGroup.objects.filter(chart=instance.id).values('name')[0]
        return str(chart_groups['name'])


class ChartGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'chart')


class ReportRecipientsAdmin(admin.TabularInline):
    model = models.ReportRecipients


class ScheduledReportParamAdmin(admin.TabularInline):
    model = models.ScheduledReportParam


class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_reports', 'get_parameters')
    inlines = [
        ScheduledReportParamAdmin,
        ReportRecipientsAdmin
    ]


admin.site.register(models.ScheduledReport, ScheduledReportAdmin)
admin.site.register(models.Chart, ChartAdmin)
admin.site.register(models.ChartGroup, ChartGroupAdmin)
