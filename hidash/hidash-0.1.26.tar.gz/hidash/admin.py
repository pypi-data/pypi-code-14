from django.contrib import admin
import models
from django.core import urlresolvers


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
    extra = 1


class ChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'library', 'chart_type', 'priority', 'grid_width',
                    'height', 'group')
    inlines = [
        ChartMetricInlineAdmin, ChartAuthPermissionInlineAdmin,
        ChartAuthGroupInlineAdmin, ChartGroupInlineAdmin
    ]

    def group(self, instance):
        chart_group = models.ChartGroup.objects.filter(chart=instance.id).values('group')
        if chart_group:
            chart_groups = chart_group[0]
            return str(chart_groups['group'])
        else:
            return "No group assigned"


class ChartParameterAdmin(admin.TabularInline):
    model = models.ChartParameter


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ChartParameterAdmin]


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

class FilterInlineAdmin(admin.TabularInline):
    model = models.Filter
    fields = ('label','filter_type','field_name','comparator','changeform_link')
    readonly_fields = ('changeform_link',)

    def changeform_link(self, instance):
      if instance.id:
        changeform_url = urlresolvers.reverse(
          'admin:Hidash_filter_change', args=(instance.id,)
        )
        return u'<a href="%s">Add Values</a>' % changeform_url
      return u''

    changeform_link.allow_tags = True
    changeform_link.short_description = 'Add Values To Filters'

    extra = 1


class FilterValuesInlineAdmin(admin.TabularInline):
    model = models.FilterValues
    extra = 1


class FilterAdmin(admin.ModelAdmin):
    inlines = [FilterValuesInlineAdmin]


class GroupByInlineAdmin(admin.TabularInline):
    model = models.GroupBy
    extra = 1


class ColumnMetaDataInlineAdmin(admin.TabularInline):
    model = models.ColumnMetaData
    extra = 1


class ReportGroupInlineAdmin(admin.TabularInline):
    model = models.ReportGroup.report.through
    extra = 1



class ReportAdmin(admin.ModelAdmin):
    inlines = [
        ReportGroupInlineAdmin,
        GroupByInlineAdmin,
        ColumnMetaDataInlineAdmin,
        FilterInlineAdmin
    ]


admin.site.register(models.ReportGroup)
admin.site.register(models.Filter, FilterAdmin)
admin.site.register(models.Report, ReportAdmin)
admin.site.register(models.ScheduledReport, ScheduledReportAdmin)
admin.site.register(models.Chart, ChartAdmin)
admin.site.register(models.Group, GroupAdmin)
