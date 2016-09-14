import csv

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count, Q
from django.http import (HttpResponseRedirect, Http404, JsonResponse,
    HttpResponse)
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView, View

from haystack.query import SearchQuerySet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .constants import DURATION_LOOKUP, POSITIVE
from .forms import ReportFilterForm
from .mixins import DashboardAccessMixin
from .models import ReportFilter, SystemMessage
from .templatetags.veriport_dashboard_tags import get_duration_field
from .utils import generate_queryset_ids, get_report_model, get_account_model

Report = get_report_model()
Account = get_account_model()
User = get_user_model()


class Dashboard(DashboardAccessMixin, TemplateView):
    """
    Displays dashboard reporting
    """
    template_name = "veriport_dashboard/dashboard.html"

    def get_average_types(self):
        return [
            "ccf",
            "review",
            "release",
            "interview",
            "positive-non-dot",
            "positive-dot"
        ]

    def get_system_message(self):
        return SystemMessage.objects.order_by("-date_created")[:10]

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context["system_messages"] = self.get_system_message()
        context["average_types"] = self.get_average_types()
        return context


class AccountList(DashboardAccessMixin, ListView):
    """
    Displays list of :model:'veriport_dashboard.Account'
    """
    model = Account
    template_name = "veriport_dashboard/accounts/list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        user = self.request.user
        if user.is_tpa:
            return Account.objects.filter(Q(id=user.account.id) |
                Q(parent=user.account))
        return super(AccountList, self).get_queryset()


class Profile(DashboardAccessMixin, DetailView):
    """
    Displays profile page of the given user. Defaults to logged in user.
    """
    model = get_user_model()
    template_name = "veriport_dashboard/profile.html"

    def get_object(self):
        try:
            obj = self.model.objects.get(id=self.kwargs.get("pk"))
        except ObjectDoesNotExist:
            obj = self.request.user
        return obj


class RemoveFilter(DashboardAccessMixin, View):
    """
    Handles the removal/deletion of :model:'veriport_dashboard.ReportFilter'
    """

    def get_object(self):
        obj = get_object_or_404(ReportFilter, id=self.kwargs.get("pk"))
        if obj.user == self.request.user:
            return obj
        raise Http404

    def get_success_url(self):
        return reverse("dashboard:reports")

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.success(request, _("Object successfully removed."))
        return HttpResponseRedirect(self.get_success_url())


class ReportList(DashboardAccessMixin, ListView):
    """
    Displays list of :model:'veriport_dashboard.Report' based on the given
    filters/parameters.
    """
    model = Report
    template_name = "veriport_dashboard/reports/list.html"
    context_object_name = "reports"

    def get_report_filters(self):
        return self.request.user.saved_filters.order_by("-date_created")[:5]

    def _get_duration_type(self):
        duration = self.request.GET.get("duration")
        if duration in DURATION_LOOKUP:
            return DURATION_LOOKUP[duration]
        return ""

    def get_current_filter(self):
        filter_id = self.request.GET.get("filters", 0)
        try:
            saved_report = ReportFilter.objects.get(id=filter_id)
        except ReportFilter.DoesNotExist:
            saved_report = None
        return saved_report

    def _get_filter_form(self):
        if self.request.POST:
            return ReportFilterForm(self.request.POST)

        saved_report = self.get_current_filter()

        if saved_report:
            return ReportFilterForm(initial=saved_report.data)
        return ReportFilterForm()

    def get_context_data(self, **kwargs):
        context = super(ReportList, self).get_context_data(**kwargs)
        context["duration_type"] = self._get_duration_type()
        context["report_filters"] = self.get_report_filters()
        context["current_filter"] = self.get_current_filter()
        context["form"] = self._get_filter_form()
        return context

    def get_success_url(self):
        return reverse("dashboard:reports")

    def post(self, request, *args, **kwargs):
        form = self._get_filter_form()

        if form.is_valid():
            filter_name = form.cleaned_data.pop("filter_name")
            start_date = form.cleaned_data.pop("start_date")
            end_date = form.cleaned_data.pop("end_date")

            data = form.cleaned_data
            report_filter = ReportFilter.objects.create(
                user=request.user,
                name=filter_name,
                start_date=start_date,
                end_date=end_date,
                data=data
            )
            context = {
                "url": self.get_success_url(),
                "id": report_filter.id,
            }
            return HttpResponseRedirect("{url}?filters={id}".format(**context))

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class ReportListAjax(DashboardAccessMixin, View):
    """
    Returns list of :model:'veriport_dashboard.Report' via aJax
    """

    def get_all_reports(self):
        return Report.objects.all()

    def get_queryset(self):
        filters = {}
        regulated_test = 0
        account = 1
        mro_verification = 2
        ccf_date = 3
        released_date = 4
        account_type = 5
        datetime_imported = 6

        if self.request.GET.get("sSearch"):
            
            objects = SearchQuerySet().filter(
                content=self.request.GET.get("sSearch")).values_list("object",
                flat=True)
            filters["id__in"] = generate_queryset_ids(objects)

        if self.request.GET.get("sSearch_%s" % (regulated_test, )):
            value = self.request.GET.get("sSearch_%s" % (regulated_test, ))
            if value == "dot":
                filters["regulated_test"] = True
            elif value == "non-dot":
                filters["regulated_test"] = False

        if self.request.GET.get("sSearch_%s" % (account_type, )):
            value = self.request.GET.get("sSearch_%s" % (account_type, ))
            if value != "all":
                filters["account__account_type"] = value

        if self.request.GET.get("sSearch_%s" % (datetime_imported, )):
            value = self.request.GET.get("sSearch_%s" % (datetime_imported, ))
            sdate, edate = value.split("---")
            start_date = datetime.strptime(sdate, "%m/%d/%Y")
            end_date = datetime.strptime(edate, "%m/%d/%Y")
            filters["datetime_imported__gte"] = start_date
            filters["datetime_imported__lte"] = end_date

        if filters:
            return Report.objects.filter(**filters)
        return self.get_all_reports()

    def generate_reports(self):
        duration = self.request.GET.get("duration")
        if duration:
            data = [
                [
                    report.regulated_test,
                    report.account.name,
                    report.get_mro_verification_display(),
                    report.datetime_ccf_matched.strftime("%m/%d/%Y") if report.datetime_ccf_matched else "",
                    report.datetime_report_released.strftime("%m/%d/%Y") if report.datetime_report_released else "",
                    report.account.get_account_type_display(),
                    report.datetime_imported.strftime("%m/%d/%Y") if report.datetime_imported else "",
                    get_duration_field(report, duration)
                ]
            for report in self.paginate_reports()]
        else:
            data = [
                [
                    report.regulated_test,
                    report.account.name,
                    report.get_mro_verification_display(),
                    report.datetime_ccf_matched.strftime("%m/%d/%Y") if report.datetime_ccf_matched else "",
                    report.datetime_report_released.strftime("%m/%d/%Y") if report.datetime_report_released else "",
                    report.account.get_account_type_display(),
                    report.datetime_imported.strftime("%m/%d/%Y") if report.datetime_imported else ""
                ]
            for report in self.paginate_reports()]
        return data

    def paginate_reports(self):
        reports = self.get_queryset()        
        start = self.request.GET.get("iDisplayStart")
        end = int(start) + int(self.request.GET.get("iDisplayLength"))
        return reports[start:end]

    def get(self, request, *args, **kwargs):
        reports = self.generate_reports()
        reports_total = self.get_all_reports().count()
        reports_filtered = self.get_queryset().count()
        context = {
            "recordsTotal": reports_total,
            "recordsFiltered": reports_filtered,
            "data": reports
        }
        return JsonResponse(context)


class TopAccounts(DashboardAccessMixin, View):
    """
    Returns data to be used in plotting the points in Chart graph
    """

    def get_queryset(self):
        reports = Report.objects.filter(datetime_report_released__isnull=False)
        user = self.request.user

        if user.is_tpa:
            accounts = Account.objects.filter(Q(id=user.account.id) |
                Q(parent=user.account))
        else:
            accounts = Account.objects.all()

        return accounts.filter(reports__in=reports).annotate(
            num_reports=Count("reports")).order_by("-num_reports").distinct()[:10]

    def generate_data(self):
        accounts = self.get_queryset()
        labels = []
        data = []

        for account in accounts:
            labels.append(account.name)
            data.append(account.num_reports)

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Reports Released",
                    "backgroundColor": "#00a65a",
                    "strokeColor": "#00a65a",
                    "pointColor": "#00a65a",
                    "pointStrokeColor": "#c1c7d1",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": data
                }
            ]
        }

    def get(self, request, *args, **kwargs):
        data = self.generate_data()
        context = {
            "chart_data": data
        }
        return JsonResponse(context)


class ReportsReleased(DashboardAccessMixin, View):
    """
    Returns chart data about reports released
    """

    def generate_data(self):
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        labels = []
        data_30 = []
        data_60 = []
        
        for day in range(1, 31):
            if day == 1:
                labels.append("{0} day".format(day))
            else:
                labels.append("{0} days".format(day))
            released_date_30 = now - timedelta(days=day)
            released_date_60 = last_30 - timedelta(days=day)
            reports_30 = Report.objects.filter(
                datetime_report_released__date=released_date_30).count()
            reports_60 = Report.objects.filter(
                datetime_report_released__date=released_date_60).count()

            data_30.append(reports_30)
            data_60.append(reports_60)

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Last 30 Days",
                    "backgroundColor": "#00a65a",
                    "strokeColor": "#00a65a",
                    "pointColor": "#00a65a",
                    "pointStrokeColor": "#c1c7d1",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": data_30
                },
                {
                    "label": "30 days before last 30",
                    "backgroundColor": "#3b8bba",
                    "strokeColor": "#3b8bba",
                    "pointColor": "#3b8bba",
                    "pointStrokeColor": "#c1c7d1",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": data_60
                }
            ]
        }

    def get(self, request, *args, **kwargs):
        data = self.generate_data()
        context = {
            "chart_data": data
        }
        return JsonResponse(context)


class DashboardAverage(DashboardAccessMixin, View):
    """
    Returns average depending on the given report type
    """

    def check_average_type(self, average_type):
        lookup = [
            "positive-dot",
            "positive-non-dot",
            "review",
            "ccf",
            "release",
            "interview"
        ]
        if average_type not in lookup:
            raise Http404
        pass

    def get_reports(self):
        daterange = self.request.GET.get("range", None)
        now = timezone.now()
        end_date = now
        start_date = now - timedelta(days=30)
        if daterange == "last7":
            start_date = now - timedelta(days=7)
        elif daterange == "thismonth":
            start_date = datetime(now.year, now.month, 1)
        
        return Report.objects.filter(datetime_imported__gte=start_date,
            datetime_imported__lte=end_date)
        # return Report.objects.all()

    def get_average_dot(self):
        average = 0
        reports = self.get_reports()
        dot = reports.filter(datetime_report_released__isnull=False,
            mro_verification=POSITIVE, regulated_test=True)
        all_dot = reports.filter(datetime_report_released__isnull=False,
            regulated_test=True)
        if all_dot.exists():
            average = dot.count() / all_dot.count()
        return average

    def get_average_non_dot(self):
        average = 0
        reports = self.get_reports()
        non_dot = reports.filter(datetime_report_released__isnull=False,
            mro_verification=POSITIVE, regulated_test=False)
        all_non_dot = reports.filter(datetime_report_released__isnull=False,
            regulated_test=True)
        if all_non_dot.exists():
            average = non_dot.count() / all_non_dot.count()
        return average

    def get_average_duration(self, duration_type):
        reports = self.get_reports()
        duration_reports = reports.values_list(
            "durations__{0}".format(duration_type), flat=True)
        average = 0
        if duration_reports.exists():
            average_seconds = sum(duration_reports) / reports.count()
            average_time = timedelta(seconds=average_seconds)
            average = average_time.days
        return average

    def get(self, request, *args, **kwargs):
        average_type = self.kwargs.get("average_type")
        self.check_average_type(average_type)
        if average_type == "positive-dot":
            average = self.get_average_dot()
        elif average_type == "positive-non-dot":
            average = self.get_average_non_dot()
        else:
            average = self.get_average_duration(average_type)
        context = {
            "average": average
        }
        return JsonResponse(context)


class ExportReports(DashboardAccessMixin, View):
    """
    Export the resulting :model:'veriport_dashboard.Report' to CSV/PDF
    depending on the given type.
    """

    def generate_pdf_data(self, data):
        reports = data["reports"]
        table_data = []
        headers = []
        if data["account"]:
            headers.append(_("Account"))
        if data["mro_verification"]:
            headers.append(_("MRO Verification"))
        if data["date_ccf_matched"]:
            headers.append(_("Date CCF Matched"))
        if data["date_released"]:
            headers.append(_("Date Released"))
        table_data.append(headers)

        for report in reports:
            row = []
            if data["account"]:
                row.append(report.account.name)
            if data["mro_verification"]:
                row.append(report.get_mro_verification_display())
            if data["date_ccf_matched"]:
                row.append(report.datetime_ccf_matched.strftime("%m/%d/%Y") if report.datetime_ccf_matched else "")
            if data["date_released"]:
                row.append(report.datetime_report_released.strftime("%m/%d/%Y") if report.datetime_report_released else "")
            table_data.append(row)
        return table_data

    def _generate_table(self, table_data):
        table = Table(data=table_data)
        table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        return table

    def pdf_response(self, data):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="export_reports.pdf"'

        table_data = self.generate_pdf_data(data)

        doc = SimpleDocTemplate(response)
        elements = []
        table = self._generate_table(table_data)
        elements.append(table)
        doc.build(elements)
        return response

    def get_queryset(self):
        account_type = self.request.POST.get("account_type")
        regulated_testing = self.request.POST.get("regulated_testing")
        tpa_reports = self.request.POST.get("tpa_reports")
        mro_reports = self.request.POST.get("mro_reports")
        sdate = self.request.POST.get("start_date")
        edate = self.request.POST.get("end_date")

        start_date = datetime.strptime(sdate, "%m/%d/%Y")
        end_date = datetime.strptime(edate, "%m/%d/%Y")
        filters = {
            "datetime_imported__lte": end_date,
            "datetime_imported__gte": start_date,
        }

        if regulated_testing != "all":
            filters["regulated_test"] = True if regulated_testing == "dot"\
                else False

        if account_type != "all":
            filters["account__account_type"] = account_type

        return Report.objects.filter(**filters)

    def csv_response(self, data):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_reports.csv"'

        writer = csv.writer(response, quoting=csv.QUOTE_ALL)

        reports = data["reports"]

        header_row = []
        if data["account"]:
            header_row.append(_("Account"))
        if data["mro_verification"]:
            header_row.append(_("MRO Verification"))
        if data["date_ccf_matched"]:
            header_row.append(_("Date CCF Matched"))
        if data["date_released"]:
            header_row.append(_("Date Released"))
        writer.writerow(header_row)

        for report in reports:
            row = []
            if data["account"]:
                row.append(report.account.name)
            if data["mro_verification"]:
                row.append(report.get_mro_verification_display())
            if data["date_ccf_matched"]:
                row.append(report.datetime_ccf_matched.strftime("%m/%d/%Y") if report.datetime_ccf_matched else "")
            if data["date_released"]:
                row.append(report.datetime_report_released.strftime("%m/%d/%Y") if report.datetime_report_released else "")

            writer.writerow(row)
        return response

    def post(self, request, *args, **kwargs):
        account = request.POST.get("account", False)
        mro_verification = request.POST.get("mro_verification", False)
        date_ccf_matched = request.POST.get("date_ccf_matched", False)
        date_released = request.POST.get("date_released", False)
        
        reports = self.get_queryset()
        data = {
            "account": account,
            "mro_verification": mro_verification,
            "date_ccf_matched": date_ccf_matched,
            "date_released": date_released,
            "reports": reports
        }
        export_type = self.kwargs.get("export_type")
        if export_type == "pdf":
            return self.pdf_response(data)
        if export_type == "csv":
            return self.csv_response(data)

        # return HttpResponseRedirect(reverse("dashboard:reports"))


class UsersList(DashboardAccessMixin, ListView):
    """
    Displays list of users belong to child account
    """
    template_name = "veriport_dashboard/users/list.html"
    context_object_name = "users"

    def get_queryset(self):
        parents_list = ["TPA", "COMP", "EMPL"]
        account = self.request.user.account
        if account.account_type == "MRO":
            user_ids = account.mro_account.values_list("users",
                flat=True).distinct()
        elif account.account_type in parents_list:
            user_ids = account.account_set.values_list("users",
                flat=True).distinct()

        return User.objects.filter(id__in=user_ids)
