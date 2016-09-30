ENVIRON_AUTH_TOKEN  = 'ZOHO_CRM_AUTH_TOKEN'
BASE_URL            = "https://crm.zoho."
API_PATH            = "/crm/private/json"
SCOPE               = 'crmapi'
MAX_PAGE_SIZE       = 200
REQUESTS_PER_SECOND = None

from .potentials.get_potential import get_potential  # noqa
from .accounts.get_account import get_account  # noqa
from .contacts.get_contact import get_contact  # noqa
from .leads.get_lead import get_lead  # noqa
from .get_record import get_record  # noqa

from .potentials.filter_potentials import filter_potentials  # noqa
from .accounts.filter_accounts import filter_accounts  # noqa
from .contacts.filter_contacts import filter_contacts  # noqa
from .leads.filter_leads import filter_leads  # noqa
from .filter_records import filter_records  # noqa

from .potentials.insert_potential import insert_potential  # noqa
from .accounts.insert_account import insert_account  # noqa
from .contacts.insert_contact import insert_contact  # noqa
from .leads.insert_lead import insert_lead  # noqa
from .insert_record import insert_record  # noqa

from .potentials.update_potential import update_potential  # noqa
from .accounts.update_account import update_account  # noqa
from .contacts.update_contacts import update_contact  # noqa
from .leads.update_lead import update_lead  # noqa
from .update_record import update_record  # noqa

from .potentials.delete_potential import delete_potential  # noqa
from .accounts.delete_account import delete_account  # noqa
from .contacts.delete_contact import delete_contact  # noqa
from .leads.delete_lead import delete_lead  # noqa
from .delete_record import delete_record  # noqa

from .upload_file import upload_file  # noqa

from .delete_file import delete_file  # noqa
