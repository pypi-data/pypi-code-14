from models import ScheduledReport
from django.forms import ModelForm, ValidationError
from croniter import croniter
from datetime import datetime

class ScheduledReportForm(ModelForm):
    class Meta:
        model = ScheduledReport
        fields = ['report', 'email_subject', 'cron_expression']


    def clean(self):
        cleaned_data = super(ScheduledReportForm, self).clean()
        cron_expression = cleaned_data.get("cron_expression")
        try:
         iter = croniter(cron_expression, datetime.now())
        except:
            raise ValidationError("Incorrect cron expression")
        return cleaned_data
