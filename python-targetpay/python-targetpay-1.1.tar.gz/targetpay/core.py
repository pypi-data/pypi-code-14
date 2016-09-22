"""
    Targetpay Python module
    Copyright (C) 2016, Balkan Technologies EOOD & Co. KD

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more information: info@balkan.tech
"""
from __future__ import print_function
from lxml import etree

import requests

DEBUG_MODE = False

VERIFICATION = {
    'IDL': 'ideal',
    'MRC': 'mrcash',
    'SOF': 'directebanking',
}

def to_cents(amount):
    """
    Convert the amount to an int of cents
    :param amount:int
    :return: integer of cents
    """
    return int(amount * 100)

class TargetPay(object):
    """
    TargetPay client object
    :param rtlo:int (mandatory), transaction_id:int (optional, default: None), method:string (optional, default: None), test:bool (optional, default: False)
    """
    def __init__(self, rtlo, transaction_id = None, method = None, test = False):
        self.rtlo = int(rtlo)
        self.test = test
        self.payment_url = None
        self.transaction_id = int(transaction_id)
        self.method = method
        self.methodtransaction_id = None
        self.cname = None
        self.cbank = None
        self.code = None
        self.explanation = None
        self.paid = False

    def process_response(self, response, verification = False):
        """
        Method for processing a payment response
        :param response:response object (mandatory), verification:bool (optional, default: False)
        :returns True on processing of a succesful transaction response, False on processing of an unsuccesful transaction response
        :raises An exception if response is incorrect or contains no status
        """
        if DEBUG_MODE:
            print('Response: %s' % response.text)

        try:
            r = response.text.split(' ')
            status = r[0]
            if DEBUG_MODE:
                print('Status: %s: ' % status)
        except:
            raise Exception("Response has no content or status")

        if str(status) == '000000':
            if DEBUG_MODE:
                print('We have a success status!')
            self.success = True
            self.explanation = None
            self.code = None

            if not verification:
                (self.transaction_id, self.payment_url) = r[1].split('|')
            else:
                self.paid = True

        else:
            if DEBUG_MODE:
                print('No success status!')
            self.success = False
            self.paid = False
            self.code = status
            self.explanation = response.text[7:]

        return self

    def verify_payment(self, once=True):
        """
        Method for verifying a payment
        :param once:bool (optional, default: True)
        """
        if not self.transaction_id or not self.method:
            raise Exception('Object has no transaction_id or method set')

        if self.method:
            try:
                method = VERIFICATION[self.method]
            except:
                raise Exception('Invalid payment method')

            data = {
                'rtlo': self.rtlo,
                'trxid': self.transaction_id
            }

            data['once'] = 1 if once else 0
            if (self.method == 'MRC' or self.method == 'SOF') and self.test:
                data['test'] = 1

            if DEBUG_MODE:
                print(data)

            self.process_response(requests.post('https://www.targetpay.com/%s/check' % method, data=data),
                                  verification=True)

            return self
        else:
            raise Exception('No payment method has been set')

    def callback(self, cname = None, cbank = None, idealtrxid = None):
        """
        Method for processing a callback (webhook) response
        :param trxid: string (optional, default: None), cname:string (optional, default: None), vbank:string (optional, default: None), idealtrxid:int (optional, default: None)
        """
        if not self.transaction_id or not self.method:
            raise Exception('Object has no transaction_id or method set')

        if self.method == 'IDL':
            if idealtrxid:
                self.methodtransaction_id = int(idealtrxid)
            else:
                raise Exception('No idealtrxid has been provided')
            if cname:
                self.cname = cname
            if self.cbank:
                self.cbank = cbank

        return self.verify_payment(once = False)

    def ideal_issuers(self, as_dict = False):
        """
        Method for obtaining the available iDeal issuers
        :param as_dict:bool (optional, default: False)
        """
        url = 'https://www.targetpay.com/ideal/getissuers?ver=3&format=xml'
        req = requests.get(url)
        doc = etree.fromstring(req.content)
        issuers_array = []
        issuers_dict = {}

        for issuer in doc.findall('issuer'):
            if not as_dict:
                issuers_array.append([issuer.get('id'), issuer.text])
            else:
                issuers_dict[issuer.get('id')] = issuer.text
        return issuers_array if not as_dict else issuers_dict

    def ideal_payment(self, description, amount, return_url, cancel_url = None, report_url = None, bank = None, ver = 3):
        """
        Method for initializing an iDeal payment
        :param description:string (mandatory), amount:int (mandatory), return_url:string (mandatory), cancel_url:string (optional, default: None), report_url:string (optional, default: None), bank:string (optional, default: None), ver:int (optional, default: 3)
        """
        self.method = 'IDL'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'returnurl': return_url,
            'ver': ver,
        }

        if bank:
            data['bank'] = bank

        if cancel_url:
            data['cancelurl'] = cancel_url

        if report_url:
            data['reporturl'] = report_url

        if self.test:
            data['test'] = 1

        if DEBUG_MODE:
            print(data)

        self.process_response(requests.post('https://www.targetpay.com/ideal/start', data = data))

        return self

    def mrcash_payment(self, description, amount, ip, return_url, report_url = None, language = 'EN'):
        """
        Method for initializing a Mr. Cash payment
        :param description:string (mandatory), amount:int (mandatory), return_url:string (mandatory), ip:string (mandatory), cancel_url:string (optional, default: None), report_url:string (optional, default: None), bank:string (optional, default: None), language:string (optional, default: EN)
        """
        self.method = 'MRC'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'returnurl': return_url,
            'userip': ip,
            'lang': language
        }

        if report_url:
            data['reporturl'] = report_url

        if DEBUG_MODE:
            print(data)

        self.process_response(requests.post('https://www.targetpay.com/mrcash/start', data = data))

        return self

    def sofort_payment(self, description, amount, ip, country, payment_type, return_url, report_url = None, language = 'EN'):
        """
        Method for initializing a Sofort banking payment
        :param description:string (mandatory), amount:int (mandatory), return_url:string (mandatory), ip:string (mandatory), country:int (mandatory), payment_type:int (mandatory), cancel_url:string (optional, default: None), report_url:string (optional, default: None), bank:string (optional, default: None), language:string (optional, default: EN)
        """
        self.method = 'SOF'
        amount = to_cents(amount)

        data = {
            'rtlo': self.rtlo,
            'description': description,
            'amount': amount,
            'country': country,
            'type': payment_type,
            'returnurl': return_url,
            'userip': ip,
            'lang': language
        }

        if report_url:
            data['reporturl'] = report_url

        if DEBUG_MODE:
            print(data)

        self.process_response(requests.post('https://www.targetpay.com/directebanking/start', data = data))

        return self