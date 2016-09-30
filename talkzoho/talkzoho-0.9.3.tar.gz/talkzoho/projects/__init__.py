ENVIRON_AUTH_TOKEN  = 'ZOHO_PROJECTS_AUTH_TOKEN'
BASE_URL            = "https://projectsapi.zoho."
API_PATH            = "/restapi"
MAX_PAGE_SIZE       = 100
REQUESTS_PER_SECOND = None  # TODO: done per endpoint at 100 in two minutes


from .accounts.get_account import get_account  # noqa

from .projects.get_project import get_project  # noqa
from .projects.filter_projects import filter_projects  # noqa
