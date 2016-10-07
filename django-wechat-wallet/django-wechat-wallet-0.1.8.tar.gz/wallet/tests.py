from django.test import TestCase
from wechat_member.models import Member
from .api import WalletApi

# Create your tests here.

class WalletApiTest(TestCase):
    def test_api_init(self):
        me, status = Member.objects.get_or_create(
                name='chen',
                avatar='null',
                city='luoyang',
                )
        print(me)
        w = WalletApi(me.id)
        self.assertIs(w.wallet.balance, True)
