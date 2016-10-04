from django.conf.urls import url
from django.contrib import admin, messages
from django.db import models
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from publishing.models import PublishingLanguage, PublishingCountry
from publishing.utils import clone_fields

# django url reverse
try:
    # django > 1.8
    from django.urls.base import reverse
except:
    # django <= 1.8
    from django.urls import reverse


# COUNTRY
class LanguageModelMixin(models.Model):
    language = models.ForeignKey(PublishingLanguage, verbose_name=_(u"Language"),
                                 related_name="%(app_label)s_%(class)s_contents", null=True, )
    translation_of = models.ForeignKey('self', blank=True, null=True, related_name='translations',
                                       on_delete=models.SET_NULL, verbose_name=_(u"Translation of"), )

    class Meta:
        abstract = True


# LANGUAGE
class CountryModelMixin(models.Model):
    countries = models.ManyToManyField(PublishingCountry, verbose_name=_(u"Available Countries"), )

    class Meta:
        abstract = True


# REGION
class PublishingRegionAdminMixin(object):

    @staticmethod
    def get_request_user_countries(request):
        return

    @staticmethod
    def get_request_user_languages(request):
        return

    def get_queryset(self, request):
        """
        filters queryset on the users editorial
        regions languages and countries.

        :param request:
        :return:
        """

        qs = super(PublishingRegionAdminMixin, self).get_queryset(request)
        # concat countries and languages for user
        regions = request.user.profile.editorial_regions.all()
        countries = concat_countries_of_regions(regions)
        languages = concat_languages_of_regions(regions)

        include_pks = []
        for item in qs:
            for country in countries:
                if country in item.countries.all():
                    include_pks.append(item.pk)

        return qs.filter(pk__in=include_pks, language__in=languages)

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == "countries" or db_field.name == "language":
            regions = request.user.profile.editorial_regions.all()
            if db_field.name == "language":
                languages = concat_languages_of_regions(regions)
                iso_codes = [l.iso_code for l in languages]
                return db_field.remote_field.model._default_manager.filter(iso_code__in=iso_codes)

            if db_field.name == "countries":
                countries = concat_countries_of_regions(regions)
                iso_codes = [c.iso_code for c in countries]
                return db_field.remote_field.model._default_manager.filter(iso_code__in=iso_codes)

        super().get_field_queryset(db, db_field, request)


def concat_countries_of_regions(regions):
    countries = []
    for region in regions:
        for country in region.countries.all():
            if not country in countries:
                countries.append(country)

    return countries


def concat_languages_of_regions(regions):
    languages = []
    for region in regions:
        for language in region.languages.all():
            if not language in languages:
                languages.append(language)

    return languages


# PUBLISHING
PUBLISHING_STATES = (
    ('new', _(u"New")),
    ('published', _(u"Published")),
    ('edited', _(u"Being edited")),
    ('draft', _(u"Draft")),
)


class PublishingStateFilter(admin.SimpleListFilter):
    title = _(u"Publishing State")
    parameter_name = 'publishing_state'

    def lookups(self, request, model_admin):
        return PUBLISHING_STATES

    def queryset(self, request, queryset):
        if self.value():
            value = self.value()
            if value == "new":
                return queryset.filter(is_draft=True, draft_of__isnull=True, )
            if value == "edited":
                return queryset.filter(is_draft=False, has_draft=True, )
            if value == "published":
                return queryset.filter(is_draft=False, has_draft=False, )
            if value == "draft":
                return queryset.filter(is_draft=True, draft_of=True, )
            return queryset
        else:
            return queryset


class PublishingModelManager(models.Manager):
    pass


class PublishingModelMixin(models.Model):
    is_draft = models.BooleanField(_("Is draft"), default=False, )
    has_draft = models.BooleanField(_("Has draft"), default=False, )
    draft_of = models.ForeignKey("self", related_name="draft", null=True, blank=True, )

    objects = [PublishingModelManager, ]

    def __str__(self):
        if self.is_draft:
            string = super(PublishingModelMixin, self).__str__()
            return u"%s -- DRAFT" % string
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        # set as draft when created
        if not self.pk:
            self.is_draft = True
        super(PublishingModelMixin, self).save(*args, **kwargs)


    def has_draft_instance(self):
        # filter for drafts of the instance
        if self.__class__.objects.filter(is_draft=True, draft_of=self).count() > 0:
            return True
        return False

    def get_draft_instance(self):
        if not self.has_draft_instance():
            return False
        return self.__class__.objects.filter(is_draft=True, draft_of=self)[0]

    def validate_create_draft(self):
        # do not create draft if the instance is a draft itself
        if self.is_draft:
            print("Can not create draft, %s (%s) is a draft." % (self, self.__class__.__name__))
            return False
        # check for existing draft of this instance
        if self.has_draft_instance():
            print("Can not create draft, %s (%s) has already a draft." % (self, self.__class__.__name__))
            return False
        return True

    def get_publishing_state(self):
        if self.is_draft and self.draft_of:
            return dict(PUBLISHING_STATES)['draft']

        if self.is_draft:
            return dict(PUBLISHING_STATES)['new']

        if self.has_draft_instance():
            return dict(PUBLISHING_STATES)['edited']

        return dict(PUBLISHING_STATES)['published']

    class Meta:
        abstract = True


class PublishAdminMixin(object):
    change_list_template = 'admin/publish_change_list.html'
    change_form_template = 'admin/publish_change_form.html'

    def get_list_filter(self, request):
        fields = list(super(PublishAdminMixin, self).get_list_filter(request))
        if 'publishing_state' not in fields:
            fields.insert(0, PublishingStateFilter)
        return fields

    def get_urls(self):
        """
        Add publish and unpublish urls to model admins.
        :return:
        """
        app_label = self.model._meta
        model_class = self.model.__name__.lower()

        urls = super(PublishAdminMixin, self).get_urls()
        admin_urls = [
            url(r'^publish/(?P<pk>[0-9]+)/$', self.publish_obj, name='publish',),
            url(r'^unpublish/(?P<pk>[0-9]+)/$', self.unpublish_obj, name='unpublish'),
            url(r'^create_draft/(?P<pk>[0-9]+)/$', self.create_obj, name='create_draft'),

            url(r'^publish/(?P<pk>[0-9]+)/$', self.publish_obj, name='publish_%s' % model_class),
            url(r'^unpublish/(?P<pk>[0-9]+)/$', self.unpublish_obj, name='unpublish_%s' % model_class),
            url(r'^create_draft/(?P<pk>[0-9]+)/$', self.create_obj, name='create_draft_%s' % model_class),
        ]

        return admin_urls + urls

    def create_obj(self, request, pk):
        model = self.model
        original = model.objects.get(pk=pk)

        # copy original and create draft
        if original.validate_create_draft():
            draft = original.__class__()
            draft.pk = None
            draft = clone_fields(draft, original)
            draft.is_draft = True
            draft.draft_of = original
            draft.save()

            # admin message
            messages.success(request, _(u'Your %s draft has been successfully created.' %
                                        model._meta.model_name ))

            # redirect to original version
            return HttpResponseRedirect(
                reverse("admin:%s_%s_change" %
                        (model._meta.app_label, model._meta.model_name), args=(draft.pk,))
            )

        # error - redirect to original version
        messages.error(request, _(u'Draft %s could not be created. Please try again.' %
                                    model._meta.model_name))
        return HttpResponseRedirect(
            reverse("admin:%s_%s_change" %
                    (model._meta.app_label, model._meta.model_name), args=(original.pk,))
        )

    def publish_obj(self, request, pk):
        model = self.model
        draft = model.objects.get(pk=pk)

        # copy draft version to original, when published version exists
        if draft.draft_of:
            original = clone_fields(draft.draft_of, draft)
            draft.delete()
            redirect_pk = original.pk
        else:
            draft.is_draft = False
            draft.save()
            redirect_pk = draft.pk

        # admin message
        messages.success(request, _(u'Your %s has been successfully been published.' %
                                    model._meta.model_name ))

        # redirect to original version
        return HttpResponseRedirect(
            reverse("admin:%s_%s_change" %
                    (model._meta.app_label, model._meta.model_name), args=(redirect_pk,))
        )

    def unpublish_obj(self, request, pk):
        model = self.model
        draft = model.objects.get(pk=pk)
        original = draft.draft_of

        # delete draft
        draft.delete()

        # admin message
        messages.success(request, _(u'Your %s has been successfully been deleted.' %
                                    model._meta.model_name))

        # redirect to original version
        return HttpResponseRedirect(
            reverse("admin:%s_%s_change" %
                    (model._meta.app_label, model._meta.model_name), args=(original.pk,))
        )

    @staticmethod
    def is_draft(request):
        """
        Check if the view has been set to show drafts.

        :param request:
        :return:
        """
        if request.GET.get('is_draft__exact', None):
            return True
        return False

    def get_list_display(self, request):
        """
        Add the column 'draft_of' if unpublished versions are selected.

        :param request:
        :return:
        """
        list_display = super(PublishAdminMixin, self).get_list_display(request)
        # if not type(list_display) is not tuple:
        #     list_display = tuple()

        if self.is_draft(request):
            if 'draft_of' not in list_display:
                if self.is_draft(request):
                    try:
                        if '_reorder' in list_display:
                            list_display.insert(98, 'draft_of')
                        else:
                            list_display.insert(98, 'draft_of')
                    except AttributeError:
                        list_display = ('draft_of', )

            if 'get_draft_instance' in list_display:
                list_display.remove('get_draft_instance')
        else:
            if 'draft_of' in list_display:
                list_display.remove('draft_of')

            if 'get_draft_instance' not in list_display:
                list_display.insert(99, 'get_draft_instance')

        return list_display

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.has_draft_instance():
                return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def changelist_view(self, request, extra_context=None):
        """
        Default queryset should be filtered to only show published versions.
        When drafts should be shown we filter queryset to show draft versions.

        :param request:
        :param extra_context:
        :return:
        """
        q = request.GET.copy()
        if len(request.GET) == 0:
            q['is_draft__exact'] = 0
        else:
            if request.GET.get('is_draft__exact'):
                q['is_draft__exact'] = 1
        request.GET = q
        request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(PublishAdminMixin, self).changelist_view(request, extra_context=extra_context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PublishAdminMixin, self).get_fieldsets(request, obj)
        # if obj.is_draft:
        #     fieldsets[0][1]['fields'] += ('draft_of', )
        return fieldsets