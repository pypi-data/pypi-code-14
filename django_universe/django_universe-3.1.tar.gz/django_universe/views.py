from django.shortcuts import render,HttpResponse,render_to_response
from django.conf import settings
import json,os
# Create your views here.

def index(request):
    views_dict = {}
    apps = settings.APPS_FOR_UNIVERSE
    for app in apps:
	
	#views
	
	list1 = []
	list2 = []
	views_file = os.path.join(settings.BASE_DIR,app,'views.py')
	for line in file(views_file):
	    if line.startswith('def'):
		list1.append(line[4:line.index('(')])
	views_dict[app] = list1
	
    return render_to_response('django_universe/code_base.html',{})
