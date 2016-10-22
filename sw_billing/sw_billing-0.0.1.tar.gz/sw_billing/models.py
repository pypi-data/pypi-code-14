import json
from django.conf import settings
from django.db import models
from django.db.models import Sum
from swutils.encrypt import encrypt, decrypt


class Customer(models.Model):
    encrypted_token = models.CharField(max_length=255) #

    def get_password(self):
        return decrypt(self.encrypted_token, settings.SECRET_KEY.encode())

    def set_token(self, token):
        self.encrypted_token = encrypt(token, settings.SECRET_KEY.encode())

    def get_balance(self):
        payments = self.payments.all().aggregate(Sum('sum'))
        expenses = self.expenses.all().aggregate(Sum('cost'))
        return payments - expenses

    def __str__(self):
        return self.auth_token


class Expense(models.Model):

    uuid = models.UUIDField()
    customer = models.ForeignKey(Customer, related_name='expenses')
    sku_code = models.CharField(max_length=255)
    dc = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(help_text='json-объект с дополнительным описанием')
    cost = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True, help_text='Стоимость, по которой была оказана услуга (заполняется в ходе вхаимодействия с CRM)')

    def get_extra(self):
        return json.loads(self.extra)

    def set_extra(self, extra):
        self.extra = json.loads(extra)


class Payment(models.Model):

    uuid = models.UUIDField()
    customer = models.ForeignKey(Customer, related_name='payments')
    sum = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True, help_text='сумма платежа')
    dc = models.DateTimeField(auto_now_add=True)
