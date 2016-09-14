try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from .processout import ProcessOut
from .networking.response import Response

try:
    from .activity import Activity
except ImportError:
    import sys
    Activity = sys.modules[__package__ + '.activity']
try:
    from .authorizationrequest import AuthorizationRequest
except ImportError:
    import sys
    AuthorizationRequest = sys.modules[__package__ + '.authorizationrequest']
try:
    from .customer import Customer
except ImportError:
    import sys
    Customer = sys.modules[__package__ + '.customer']
try:
    from .token import Token
except ImportError:
    import sys
    Token = sys.modules[__package__ + '.token']
try:
    from .event import Event
except ImportError:
    import sys
    Event = sys.modules[__package__ + '.event']
try:
    from .gateway import Gateway
except ImportError:
    import sys
    Gateway = sys.modules[__package__ + '.gateway']
try:
    from .gatewayconfiguration import GatewayConfiguration
except ImportError:
    import sys
    GatewayConfiguration = sys.modules[__package__ + '.gatewayconfiguration']
try:
    from .customeraction import CustomerAction
except ImportError:
    import sys
    CustomerAction = sys.modules[__package__ + '.customeraction']
try:
    from .project import Project
except ImportError:
    import sys
    Project = sys.modules[__package__ + '.project']
try:
    from .refund import Refund
except ImportError:
    import sys
    Refund = sys.modules[__package__ + '.refund']
try:
    from .subscription import Subscription
except ImportError:
    import sys
    Subscription = sys.modules[__package__ + '.subscription']
try:
    from .tailoredinvoice import TailoredInvoice
except ImportError:
    import sys
    TailoredInvoice = sys.modules[__package__ + '.tailoredinvoice']
try:
    from .transaction import Transaction
except ImportError:
    import sys
    Transaction = sys.modules[__package__ + '.transaction']
try:
    from .webhook import Webhook
except ImportError:
    import sys
    Webhook = sys.modules[__package__ + '.webhook']

from .networking.requestprocessoutprivate import RequestProcessoutPrivate


class Invoice:

    def __init__(self, instance = None):
        if instance == None:
            instance = ProcessOut.getDefault()

        self._instance = instance

        self._id = ""
        self._project = None
        self._transaction = None
        self._customer = None
        self._subscription = None
        self._url = ""
        self._name = ""
        self._amount = ""
        self._currency = ""
        self._metadata = {}
        self._requestEmail = False
        self._requestShipping = False
        self._returnUrl = ""
        self._cancelUrl = ""
        self._sandbox = False
        self._createdAt = ""
        
    @property
    def id(self):
        """Get id"""
        return self._id

    @id.setter
    def id(self, val):
        """Set id
        Keyword argument:
        val -- New id value"""
        self._id = val
        return self
    
    @property
    def project(self):
        """Get project"""
        return self._project

    @project.setter
    def project(self, val):
        """Set project
        Keyword argument:
        val -- New project value"""
        if isinstance(val, Project):
            self._project = val
        else:
            obj = Project(self._instance)
            obj.fillWithData(val)
            self._project = obj
        return self
    
    @property
    def transaction(self):
        """Get transaction"""
        return self._transaction

    @transaction.setter
    def transaction(self, val):
        """Set transaction
        Keyword argument:
        val -- New transaction value"""
        if isinstance(val, Transaction):
            self._transaction = val
        else:
            obj = Transaction(self._instance)
            obj.fillWithData(val)
            self._transaction = obj
        return self
    
    @property
    def customer(self):
        """Get customer"""
        return self._customer

    @customer.setter
    def customer(self, val):
        """Set customer
        Keyword argument:
        val -- New customer value"""
        if isinstance(val, Customer):
            self._customer = val
        else:
            obj = Customer(self._instance)
            obj.fillWithData(val)
            self._customer = obj
        return self
    
    @property
    def subscription(self):
        """Get subscription"""
        return self._subscription

    @subscription.setter
    def subscription(self, val):
        """Set subscription
        Keyword argument:
        val -- New subscription value"""
        if isinstance(val, Subscription):
            self._subscription = val
        else:
            obj = Subscription(self._instance)
            obj.fillWithData(val)
            self._subscription = obj
        return self
    
    @property
    def url(self):
        """Get url"""
        return self._url

    @url.setter
    def url(self, val):
        """Set url
        Keyword argument:
        val -- New url value"""
        self._url = val
        return self
    
    @property
    def name(self):
        """Get name"""
        return self._name

    @name.setter
    def name(self, val):
        """Set name
        Keyword argument:
        val -- New name value"""
        self._name = val
        return self
    
    @property
    def amount(self):
        """Get amount"""
        return self._amount

    @amount.setter
    def amount(self, val):
        """Set amount
        Keyword argument:
        val -- New amount value"""
        self._amount = val
        return self
    
    @property
    def currency(self):
        """Get currency"""
        return self._currency

    @currency.setter
    def currency(self, val):
        """Set currency
        Keyword argument:
        val -- New currency value"""
        self._currency = val
        return self
    
    @property
    def metadata(self):
        """Get metadata"""
        return self._metadata

    @metadata.setter
    def metadata(self, val):
        """Set metadata
        Keyword argument:
        val -- New metadata value"""
        self._metadata = val
        return self
    
    @property
    def requestEmail(self):
        """Get requestEmail"""
        return self._requestEmail

    @requestEmail.setter
    def requestEmail(self, val):
        """Set requestEmail
        Keyword argument:
        val -- New requestEmail value"""
        self._requestEmail = val
        return self
    
    @property
    def requestShipping(self):
        """Get requestShipping"""
        return self._requestShipping

    @requestShipping.setter
    def requestShipping(self, val):
        """Set requestShipping
        Keyword argument:
        val -- New requestShipping value"""
        self._requestShipping = val
        return self
    
    @property
    def returnUrl(self):
        """Get returnUrl"""
        return self._returnUrl

    @returnUrl.setter
    def returnUrl(self, val):
        """Set returnUrl
        Keyword argument:
        val -- New returnUrl value"""
        self._returnUrl = val
        return self
    
    @property
    def cancelUrl(self):
        """Get cancelUrl"""
        return self._cancelUrl

    @cancelUrl.setter
    def cancelUrl(self, val):
        """Set cancelUrl
        Keyword argument:
        val -- New cancelUrl value"""
        self._cancelUrl = val
        return self
    
    @property
    def sandbox(self):
        """Get sandbox"""
        return self._sandbox

    @sandbox.setter
    def sandbox(self, val):
        """Set sandbox
        Keyword argument:
        val -- New sandbox value"""
        self._sandbox = val
        return self
    
    @property
    def createdAt(self):
        """Get createdAt"""
        return self._createdAt

    @createdAt.setter
    def createdAt(self, val):
        """Set createdAt
        Keyword argument:
        val -- New createdAt value"""
        self._createdAt = val
        return self
    

    def fillWithData(self, data):
        """Fill the current object with the new values pulled from data
        Keyword argument:
        data -- The data from which to pull the new values"""
        if "id" in data.keys():
            self.id = data["id"]
        if "project" in data.keys():
            self.project = data["project"]
        if "transaction" in data.keys():
            self.transaction = data["transaction"]
        if "customer" in data.keys():
            self.customer = data["customer"]
        if "subscription" in data.keys():
            self.subscription = data["subscription"]
        if "url" in data.keys():
            self.url = data["url"]
        if "name" in data.keys():
            self.name = data["name"]
        if "amount" in data.keys():
            self.amount = data["amount"]
        if "currency" in data.keys():
            self.currency = data["currency"]
        if "metadata" in data.keys():
            self.metadata = data["metadata"]
        if "request_email" in data.keys():
            self.requestEmail = data["request_email"]
        if "request_shipping" in data.keys():
            self.requestShipping = data["request_shipping"]
        if "return_url" in data.keys():
            self.returnUrl = data["return_url"]
        if "cancel_url" in data.keys():
            self.cancelUrl = data["cancel_url"]
        if "sandbox" in data.keys():
            self.sandbox = data["sandbox"]
        if "created_at" in data.keys():
            self.createdAt = data["created_at"]
        
        return self

    def authorize(self, source, options = None):
        """Authorize the invoice using the given source (customer or token)
        Keyword argument:
		source -- Source -- customer or token ID
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/authorize"
        data    = {
			'source': source
        }

        response = Response(request.post(path, data, options))
        return response.success
        
    def capture(self, source, options = None):
        """Capture the invoice using the given source (customer or token)
        Keyword argument:
		source -- Source -- customer or token ID
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/capture"
        data    = {
			'source': source
        }

        response = Response(request.post(path, data, options))
        return response.success
        
    def customer(self, options = None):
        """Get the customer linked to the invoice.
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/customers"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["customer"]
        customer = Customer(instance)
        return customer.fillWithData(body)
        
    def assignCustomer(self, customerId, options = None):
        """Assign a customer to the invoice.
        Keyword argument:
		customerId -- ID of the customer to be linked to the invoice
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/customers"
        data    = {
			'customer_id': customerId
        }

        response = Response(request.post(path, data, options))
        body = response.body
        body = body["customer"]
        customer = Customer(instance)
        return customer.fillWithData(body)
        
    def customerAction(self, gatewayConfigurationId, options = None):
        """Get the customer action needed to be continue the payment flow on the given gateway.
        Keyword argument:
		gatewayConfigurationId -- ID of the gateway configuration to be used
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/gateway-configurations/" + quote_plus(gatewayConfigurationId) + "/customer-action"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["customer_action"]
        customerAction = CustomerAction(instance)
        return customerAction.fillWithData(body)
        
    def transaction(self, options = None):
        """Get the transaction of the invoice.
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/transactions"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["transaction"]
        transaction = Transaction(instance)
        return transaction.fillWithData(body)
        
    def void(self, options = None):
        """Void the invoice
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(self.id) + "/void"
        data    = {

        }

        response = Response(request.post(path, data, options))
        return response.success
        
    @staticmethod
    def all(options = None):
        """Get all the invoices.
        Keyword argument:
		
        options -- Options for the request"""
        instance = ProcessOut.getDefault()
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices"
        data    = {

        }

        response = Response(request.get(path, data, options))
        a    = []
        body = response.body
        for v in body['invoices']:
            tmp = Invoice(instance)
            tmp.fillWithData(v)
            a.append(tmp)

        return a
        
    def create(self, options = None):
        """Create a new invoice.
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices"
        data    = {
			'name': self.name, 
			'amount': self.amount, 
			'currency': self.currency, 
			'metadata': self.metadata, 
			'request_email': self.requestEmail, 
			'request_shipping': self.requestShipping, 
			'return_url': self.returnUrl, 
			'cancel_url': self.cancelUrl
        }

        response = Response(request.post(path, data, options))
        body = response.body
        body = body["invoice"]
        return self.fillWithData(body)
        
    @staticmethod
    def find(invoiceId, options = None):
        """Find an invoice by its ID.
        Keyword argument:
		invoiceId -- ID of the invoice
        options -- Options for the request"""
        instance = ProcessOut.getDefault()
        request = RequestProcessoutPrivate(instance)
        path    = "/invoices/" + quote_plus(invoiceId) + ""
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["invoice"]
        obj = Invoice()
        return obj.fillWithData(body)
        
    
