from django.shortcuts import render,HttpResponse,render_to_response
from django.conf import settings
import json,os
# Create your views here.

def get_views(app):
    list1 = []
    views_file = os.path.join(settings.BASE_DIR,app,'views.py')
    for line in file(views_file):
	if line.startswith('def'):
	    list1.append(line[4:line.index('(')])
    return list1

def index(request):
    return render_to_response('django_universe/code_base.html',{})

def code_base_info(request):
    views_dict = {}
    apps = settings.APPS_FOR_UNIVERSE
    for app in apps:
	
	#views
	views_dict[app] = get_views(app)
    dict1 = {}
    dict1['views'] = views_dict
    return HttpResponse(json.dumps(dict1))
