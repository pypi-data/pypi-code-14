from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from wechat_member.views import WxMemberView
from .models import Wallet, Log

class BaseView1(WxMemberView):
    """
    wallet base view
    if no wallet, create it
    """
    def dispatch(self, request, *args, **kwargs):
        #super(WalletBase, self).dispatch(request, *args, **kwargs)
        try:
            self.wallet = Wallet.objects.get(member=self.wx_member)
        except AttritubeError:
            """ if wx member is not exist """
            pass
        except Wallet.DoesNotExist:
            """ if wallet is not exist """
            wallet = Wallet.objects.create(member=self.wx_member)
            self.wallet = wallet
        return super(BaseView, self).dispatch(request, *args, **kwargs)

class BaseView():
    def dispatch(self, request, *args, **kwargs):
        self.wallet = Wallet.objects.first()
        return super(BaseView, self).dispatch(request, *args, **kwargs)

class HomeView(BaseView, DetailView):
    """
    home view of wallet
    """
    model = Wallet
    template_name = 'wallet/index.html'

    def get_object(self):
        return self.wallet


class LogListView(BaseView, ListView):
    """
    wallet log list view
    """
    model = Log
    template_name = 'wallet/logs.html'

    def get_queryset(self, **kwargs):
        return Log.objects.filter(wallet=self.wallet)
