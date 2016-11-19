from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
@login_required(login_url='/student/manager/')
def listShops(request):
    data={}
    try:
        data['shops']=Shop.objects.all()
    except Exception as e:
        data['error']=str(e)
        return render(request,'error.html',data)
    return render(request,'786ms_shops/shops.html',data)

@login_required(login_url='/student/manager/')
def shopSummary(request,shop_id):
    return shopSummary(request,shop_id,'daily','0')

@login_required(login_url='/student/manager/')
def shopSummary(request,shop_id,cycle='all'):
    return shopSummary(request,shop_id,cycle,'0')

@login_required(login_url='/student/manager/')
def shopSummary(request,shop_id,cycle='daily',delta='0'):
    data={}
    try:
        shop_id=int(shop_id)
        delta=int(delta)
        #TODO: send items per cycle
        if cycle=='daily':
            pass
        elif cycle=='monthly':
            pass
        elif cycle=='yearly':
            pass
        elif cycle=='all':
            pass
        else:
            raise Exception('Invalid Url cycle not valid')
        data['cycle']=cycle
        data['delta']=delta
        data['shop']=Shop.objects.get(pk=shop_id)
    except Exception as e:
        data['error']=str(e)
        print('error'+str(e))
        return render(request,'error.html',data)
    return render(request,'786ms_shops/shop_detail.html',data);
