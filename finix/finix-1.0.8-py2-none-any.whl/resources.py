from __future__ import unicode_literals
from . import config
from os.path import basename

import wac


class User(config.Resource):
    type = "users"
    uri_gen = wac.URIGen("users", "")

    def create_application(self, application):
        attrs = application.__dict__.copy()
        return self.applications.create(attrs)


class Application(config.Resource):
    type = "applications"
    uri_gen = wac.URIGen("applications", "")

    def create_partner_user(self, partner):
        attrs = partner.__dict__.copy()
        return self.users.create(attrs)

    def create_processor(self, processor):
        attrs = processor.__dict__.copy()
        return self.processors.create(attrs)


class Processor(config.Resource):
    type = "processors"


class Merchant(config.Resource):
    type = "merchants"
    uri_gen = wac.URIGen("merchants", "")


class Identity(config.Resource):
    type = "identities"
    uri_gen = wac.URIGen("identities", "")

    def provision_merchant_on(self, merchant):
        attrs = merchant.__dict__.copy()
        return self.merchants.create(attrs)

    def create_payment_instrument(self, payment_instrument):
        attrs = payment_instrument.__dict__.copy()
        attrs["identity"] = self.id
        return self.payment_instruments.create(attrs)

    def create_settlement(self, settlement):
        attrs = settlement.__dict__.copy()
        return self.settlements.create(attrs)


class PaymentInstrument(config.Resource):
    type = "payment_instruments"
    uri_gen = wac.URIGen("payment_instruments", "")


class PaymentCard(PaymentInstrument):
    def __init__(self, **kwargs):
        super(PaymentInstrument, self).__init__(**kwargs)
        self.type = "PAYMENT_CARD"


class BankAccount(PaymentInstrument):
    def __init__(self, **kwargs):
        super(PaymentInstrument, self).__init__(**kwargs)
        self.type = "BANK_ACCOUNT"


class Transfer(config.Resource):
    type = "transfers"
    uri_gen = wac.URIGen("transfers", "")

    def reverse(self, refund_amount):
        refund = Refund(refund_amount=refund_amount)
        attrs = refund.__dict__.copy()
        return self.reversals.create(attrs)


class Refund(config.Resource):
    type = "reversals"


class Authorization(config.Resource):
    type = "authorizations"
    uri_gen = wac.URIGen("authorizations", "")

    def set_void_me(self, void_me):
        self.void_me = void_me
        return self.save()

    def capture(self, amount):
        self.capture_amount = amount
        return self.save()


class Webhook(config.Resource):
    type = "webhooks"
    uri_gen = wac.URIGen("webhooks", "")


class Settlement(config.Resource):
    type = "settlements"
    uri_gen = wac.URIGen("settlements", "")


class Verification(config.Resource):
    type = "verifications"
    uri_gen = wac.URIGen("verifications", "")


class Dispute(config.Resource):
    type = "disputes"

    def upload_evidence(self, evidence_file_path):
        files = {'file': (basename(evidence_file_path), open(evidence_file_path, 'rb'), {'Expires': '0'})}
        return self.evidence.create(files=files)


class Evidence(config.Resource):
    type = "evidence"
