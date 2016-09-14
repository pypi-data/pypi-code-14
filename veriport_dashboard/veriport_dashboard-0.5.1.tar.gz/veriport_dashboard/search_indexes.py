import datetime
from haystack import indexes

from .utils import get_report_model


class ReportIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    account = indexes.CharField(model_attr="account__name")
    account_type = indexes.CharField(model_attr="account__account_type")
    mro_verification = indexes.CharField(model_attr="mro_verification")

    def get_model(self):
        return get_report_model()

    def prepare_account_type(self, obj):
        if obj.account:
            return obj.account.get_account_type_display()
        return ""

    def prepare_mro_verification(self, obj):
        return obj.get_mro_verification_display()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(datetime_report_released__isnull=False)
