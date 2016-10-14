from .product import ApplauseProduct
from . import settings
from .utils import get_emails


class ApplauseBETA(ApplauseProduct):
    """
    Applause MBM API wrapper
    """
    BASE_URL = settings.MBM_BASE_URL
    INSTALLER_STORE_URL = settings.MBM_INSTALLER_STORE_URL
    DISTRIBUTE_URL = settings.MBM_DISTRIBUTE_URL

    @staticmethod
    def validate(groups, emails):
        if not groups and not emails:
            raise Exception("Please provide at least one group or email")

    def distribute(self, app_id, path, groups=None, changelog=None, emails=None, sent_from=None, set_as_current=False):
        emails = get_emails(emails)

        installer_id = self.upload(app_id, path, changelog, set_as_current)

        json = {
            "installer": installer_id,
            "individuals": emails,
            "group_names": groups,
            "locale": "en"
        }

        # Sending empty e-mails causes error
        if sent_from:
            json["sent_from"] = sent_from

        self.session.post(self.DISTRIBUTE_URL.format(app_id=app_id), json=json).raise_for_status()
