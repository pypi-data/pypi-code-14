import os

from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from wizards.wsgi import BaseApplication
import ioc
import yaml

from pvs.controllers import ConfirmationRequestController
from pvs.controllers import ConfirmPhonenumberController

urls = Map([
    Rule(
        '/phonenumbers/confirm/',
        endpoint='phonenumber:confirm:list'
    ),
    Rule(
        '/phonenumbers/token',
        endpoint='phonenumber:token:list'
    ),
])

handlers = {
    "phonenumber:confirm:list": ConfirmationRequestController.as_view(),
    "phonenumber:token:list": ConfirmPhonenumberController.as_view(),
}

PVS_STORAGE_IOC = 'etc/pvs-storage.ioc'
PVS_SERVICES_IOC = 'etc/pvs-services.ioc'
PVS_READMODEL_IOC = 'etc/pvs-readmodel.ioc'
PVS_CREDENTIALS_IOC = 'etc/pvs-credentials.ioc'
ioc.provide('APIController.response_class', Response)

with open(PVS_SERVICES_IOC) as f:
    ioc.load(yaml.safe_load(f.read()))
with open(PVS_STORAGE_IOC) as f:
    ioc.load(yaml.safe_load(f.read()))

with open(PVS_CREDENTIALS_IOC) as f:
    ioc.load(yaml.safe_load(f.read()))

class Application(BaseApplication):
    pass


application = Application(urls,
    handlers=handlers,
    debug=__name__=='__main__' or os.getenv('PVS_DEBUG'),
    content_types=["application/json"]
)

if __name__ == '__main__':
    application = DebuggedApplication(application)
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)
