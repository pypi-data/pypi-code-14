from django.template import Context, Template, Engine
from django.http import HttpResponse, HttpResponseRedirect
import os
import json

from .models import Request, SQLEntry

engine = Engine()
template_dir = os.path.join(os.path.dirname(__file__), 'templates')


def _template_render(template_name, context=None, content_type=None, status=None):
    with open(os.path.join(template_dir, template_name)) as f:
        template = Template(f.read(), engine=engine)
        return HttpResponse(template.render(Context(context)), content_type, status)


def index(request):
    return HttpResponseRedirect('/analysis/sql/')


def sql_index(request):
    requests = Request.objects.using('analysis_sqlite3').order_by('-date').all()
    return _template_render('analysis/index.html', {'requests': requests})


def sql_detail(request, request_id=1):
    sql_list = SQLEntry.objects.using('analysis_sqlite3').filter(request_id=request_id)
    result = []
    for sql in sql_list:
        result.append(sql.as_json())
    return HttpResponse(json.dumps(result), content_type='application/json')


def sql_clean(request):
    Request.objects.using('analysis_sqlite3').all().delete()
    return HttpResponseRedirect('/analysis/sql/')
