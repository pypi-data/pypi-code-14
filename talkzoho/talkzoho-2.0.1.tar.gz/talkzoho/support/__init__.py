ENVIRON_AUTH_TOKEN  = 'ZOHO_SUPPORT_AUTH_TOKEN'
BASE_URL            = "https://support.zoho."
API_PATH            = "/api/json"
MAX_PAGE_SIZE       = 200
REQUESTS_PER_SECOND = None  # TODO: done per endpoint at 100 in two minutes


from .accounts.get_account import get_account  # noqa
from .accounts.filter_accounts import filter_accounts  # noqa
