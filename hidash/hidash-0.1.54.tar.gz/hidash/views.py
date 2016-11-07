import json
import copy
import xlwt
import datetime

from django.shortcuts import render
from django.db import connections, connection
from decimal import Decimal
from django.http import HttpResponse
from django.conf import settings
from operator import indexOf
from datetime import date, datetime
from django.db.models import Count
from django.utils.encoding import force_str
from django.utils.decorators import available_attrs
from django.shortcuts import resolve_url
from django.utils.six.moves.urllib.parse import urlparse
from django.core.serializers.json import DjangoJSONEncoder

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from models import Chart, ChartAuthGroup, ChartAuthPermission, ChartGroup,\
    ChartMetric, ScheduledReport, ScheduledReportParam, ReportRecipients,\
    Group


def request_passes_test(test_func, login_url=None, redirect_field_name=None):
    """
    Decorator for views that checks that the request passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the request object and returns True if the request passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            elif hasattr(settings, 'HIDASH_SETTINGS') and 'api_redirector' in settings.HIDASH_SETTINGS:
                return settings.HIDASH_SETTINGS['api_redirector'](request)
            else:
                return HttpResponse("User Not Authorized", status=401)
        return _wrapped_view
    return decorator


def authenticate_url(request, url_params=""):
    if hasattr(settings, 'HIDASH_SETTINGS') and 'api_authenticator' in settings.HIDASH_SETTINGS:
        return settings.HIDASH_SETTINGS['api_authenticator'](request, url_params)
    else:
        return True


def _get_group_filters(request):
    group_id = request.GET.get('group', 'default')
    filters = []
    filter_value_list = [{}]
    if hasattr(settings, 'HIDASH_SETTINGS') and 'filter_values' in settings.HIDASH_SETTINGS:
        filter_value_list = []
        filter_value_list.append(settings.HIDASH_SETTINGS['filter_values'](request))
    group_params = Group.objects.filter(name=group_id)[0].chartparameter_set.all().annotate(null_priority=Count('priority')).order_by('-null_priority', 'priority')
    for param in group_params:
        if param.parameter_type == 0:
            filter_values = [filter.get(str(param.parameter_name), [{'value': 1, 'name': 'No values provided'}]) for filter in filter_value_list]
            type = 'dropdown'
            filters.append({
                            'name': str(param.parameter_name),
                            'type': type,
                            'filter_values': filter_values[0],
                            'grid_width': param.grid_width
                            })
        elif param.parameter_type == 2 or param.parameter_type == 3:
            parameter_name = str(param.parameter_name).split(',')
            start_date = [filter.get(parameter_name[0], {'value': None}) for filter in filter_value_list]
            end_date = [filter.get(parameter_name[1], {'value': None}) for filter in filter_value_list]
            type = 'daterange'
            filter_values = [start_date[0]['value'], end_date[0]['value']]
            if param.parameter_type == 3:
                type = 'periodicDatePicker'
                if hasattr(settings, 'HIDASH_SETTINGS') and 'periodic_config' in settings.HIDASH_SETTINGS:
                    filter_values = settings.HIDASH_SETTINGS['periodic_config']
            filters.append({
                            'name': parameter_name,
                            'type': type,
                            'grid_width': param.grid_width,
                            'filter_value': filter_values
                            })

        else:
            filter_value = [filter.get(str(param.parameter_name), {'value': None}) for filter in filter_value_list]
            type = 'datetime'
            filters.append({
                            'name': str(param.parameter_name),
                            'type': type,
                            'grid_width': param.grid_width,
                            'filter_value': filter_value[0]['value']
                            })
    return filters


def _group_reports_as_json(request):
    group_id = request.GET.get('group', 'default')
    params = _augment_params(request)
    charts = _load_charts()
    data = []
    for chart_id, chart in charts.iteritems():
        if chart.group == group_id:
            if check_permissions(chart, request) and check_groups(chart, request):
                chartdata = {}
                handler = _handler_selector(chart)
                chartdata['chart_data'] = handler(chart,
                                                  chart.query,
                                                  params)
                chartdata['chart_id'] = chart_id
                if chart.lib is not None:
                    chartdata['handler_type'] = 'googlechart'
                    if chart.lib == 0:
                        chartdata['handler_type'] = 'highcharts'
                else:
                    chartdata['handler_type'] = 'hidash'
                chartdata['chart_type'] = chart.chart_type
                chartdata['description'] = chart.description
                chartdata['height'] = chart.height
                chartdata['grid_width'] = chart.grid_width
                data.append(chartdata)
    return data


@request_passes_test(lambda u: authenticate_url(u, "reports_as_json_api"), login_url=None, redirect_field_name=None)
def dispatch_group_reports_as_json(request):
    if hasattr(settings, 'HIDASH_SETTINGS') and 'sql_utils' in settings.HIDASH_SETTINGS:
        settings.HIDASH_SETTINGS['sql_utils']()
    data = _group_reports_as_json(request)
    return HttpResponse(content=json.dumps(data, cls=DjangoJSONEncoder),
                        content_type="application/json")


@request_passes_test(lambda u: authenticate_url(u, "reports_api"), login_url=None, redirect_field_name=None)
def dispatch_group_reports(request):
    return render(request, 'reports.html')


@request_passes_test(lambda u: authenticate_url(u, "groups_api"), login_url=None, redirect_field_name=None)
def dispatch_groups(request):
    groups = []
    all_groups = ChartGroup.objects.all()
    for group in all_groups:
        if not any(hidash_group.get('group_name', None) == group.group.name for hidash_group in groups):
            groups.append({'group_name': str(group.group.name), 'charts': []})
    charts = Chart.objects.all().prefetch_related('chartgroup_set')
    for chart in charts:
        chart_group = chart.chartgroup_set.all()
        if chart_group:
            for group in groups:
                if group['group_name'] == str(chart_group[0]):
                    group['charts'].append(str(chart.name))
    return render(request, 'hidash-groups.html',
                  {'hidash_groups': groups})


@request_passes_test(lambda u: authenticate_url(u, "chart_configurations_api"), login_url=None, redirect_field_name=None)
def dispatch_chart_configurations(request):
    return HttpResponse(content=json.dumps(_get_chart_congiguration(request), cls=DjangoJSONEncoder),
                        content_type="application/json")


@request_passes_test(lambda u: authenticate_url(u, "group_filters_api"), login_url=None, redirect_field_name=None)
def dispatch_group_filters_as_json(request):
    return HttpResponse(content=json.dumps(_get_group_filters(request), cls=DjangoJSONEncoder),
                 content_type="application/json")


def _get_chart_congiguration(request):
    charts = _load_charts()
    chart_configs = []
    for chart_id, chart in charts.iteritems():
        if check_permissions(chart, request) and check_groups(chart, request):
            chart_config = {
                            'chart': chart_id,
                            'description': chart.description,
                            'height': chart.height,
                            'grid_width': chart.grid_width,
                            'chart_type': chart.chart_type
                            }
            if chart.lib is not None:
                chart_config['handler_type'] = 'googlechart'
                if chart.lib == 0:
                    chart_config['handler_type'] = 'highcharts'
            else:
                chart_config['handler_type'] = 'hidash'
            chart_configs.append(chart_config)
    return chart_configs


@request_passes_test(lambda u: authenticate_url(u, "reports_as_excel_api"), login_url=None, redirect_field_name=None)
def dispatch_xls(request, chart_id):
    '''
    Function to render reports in spreadsheet format available for download
    '''
    chart_id = chart_id.split('.')[0]
    params = _augment_params(request)
    wb = xlwt.Workbook()
    ws = wb.add_sheet(chart_id)
    font_style = xlwt.easyxf('font: name Times New Roman, color-index green, bold on;align: wrap on', num_format_str='#,##0.00')
    charts = _load_charts()
    for key, chart in charts.iteritems():
        if key == chart_id:
            if check_permissions(chart, request) and check_groups(chart, request):
                cols = []
                cols.append(chart.dimension.asdict())
                cols.extend(map(lambda c: c.asdict(), chart.metrics))
                for col in cols:
                    ws.col(indexOf(cols, col)).width = int(13 * 260)

                with connections[chart.database].cursor() as cursor:
                    cursor.execute(chart.query, params)
                    for desc in cursor.description:
                        ws.write(0, indexOf(cursor.description, desc), desc[0],
                                 font_style)

                    for db_row in cursor:
                        for col_index, chart_col in enumerate(cols):
                            value = db_row[col_index]
                            value = _convert_to_type(value, chart_col['type'])
                            ws.write(indexOf(cursor, db_row) + 1, col_index,
                                     value)
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=Report.xls'
                wb.save(response)
                return response
            else:
                return HttpResponse("User Not Authorized", status=401)


def check_groups(chart, request):
    user_groups = []
    for group in request.user.groups.all():
        user_groups.append(group.name)
    for group_name in chart.groups_list:
        if group_name not in user_groups:
            return False
    return True


def check_permissions(chart, request):
    for permission in chart.permissions_list:
        if not request.user.has_perm(permission):
            return False
    return True


def _handler_selector(chart):
    # TODO: Find a way to get rid of if else
    if chart.chart_type == 'widget':
        handler = globals()['widget']
    elif chart.lib == 1:
        handler = globals()['multiple_series_row']
        if chart.chart_type == "MapChart":
            handler = globals()['google_map_chart']
        elif chart.separator is None:
            handler = globals()['report']
            if chart.dimension.id == "extract":
                handler = globals()['col_to_series_handler']
            elif len(chart.metrics) >= 1:
                handler = globals()['default_handler']
    elif chart.lib == 0:
        handler = globals()['multiple_series_row_highcharts_handler']
        if chart.separator is None:
            if chart.chart_type == 'table':
                handler = globals()['tabular_data_handler']
            elif chart.dimension.id == "extract":
                handler = globals()['col_to_series_highcharts_handler']
            elif len(chart.metrics) == 1:
                handler = globals()['single_series_highcharts_handler']
