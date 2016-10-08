# coding: utf-8

from functools import wraps
import logging

from django.conf import settings
from django.conf.urls import url as django_url
from django.http import HttpResponse
from typeddict import fields as f
from typeddict import TypedDict
from typeddict.validators import DummyValidator, ValidationError
from typeddict.api import opt
import ujson


logger = logging.getLogger(__name__)


class TdSimplifier(object):
    @staticmethod
    def serialize(data):
        return data.simplify()


class TdField(f.FieldAsIs):
    simplifier = staticmethod(TdSimplifier)
    validator = staticmethod(DummyValidator)


class BaseError(TypedDict, Exception):

    ERROR_AUTH = "api:auth"
    ERROR_BAD_JSON = "api:bad_json"
    ERROR_EMPTY_REQUEST = "api:empty_request"
    ERROR_REQUEST_NOT_DICT = "api:request_data_not_dict"
    ERROR_UNKNOWN = "api:unknown"
    ERROR_UNKNOWN_ACCEPT = "api:unknown_accept"
    ERROR_VALIDATION = "api:validation"

    code = f.StringNotEmpty(required=False, choices=[
        ERROR_AUTH,
        ERROR_BAD_JSON,
        ERROR_EMPTY_REQUEST,
        ERROR_REQUEST_NOT_DICT,
        ERROR_UNKNOWN,
        ERROR_UNKNOWN_ACCEPT,
        ERROR_VALIDATION,
    ])
    message = opt(f.String)


class BaseResult(TypedDict):
    data = opt(TdField)
    error = opt(TdField)


def unknown_error():
    return BaseError(code=BaseError.ERROR_UNKNOWN)


class Endpoint(object):

    ACCEPT_JSON = "application/json"
    ACCEPTED_FORMATS = (
        ACCEPT_JSON,
    )

    def __init__(
        self,
        data_spec=None,
        error_spec=None,
        result_spec=None,
        slug=None,
        url=None,
    ):
        self.data = None
        self.data_spec = data_spec
        if error_spec and not issubclass(error_spec, BaseError):
            raise ValueError("error_spec should inherit from BaseError")
        self.error_spec = error_spec

        self.result_spec = result_spec
        self.slug = slug
        self.url = url

    def __call__(self, f):

        self.slug = self.slug or f.__name__
        self.f = f

        @wraps(f)
        def wrapped_f(request, *args, **kwargs):
            self.request = request
            view_result = error = None
            self.request_id = request.META.get("HTTP_REQUEST_ID")
            self.format = request.META.get("HTTP_ACCEPT")
            try:
                if self.format not in self.ACCEPTED_FORMATS:
                    raise BaseError(code=BaseError.ERROR_UNKNOWN_ACCEPT)

                self.auth_check()
                self._get_data()
                self._validate_data()

                kwargs["request"] = request

                view_result = f(self.data, *args, **kwargs)
            except BaseError as e:
                error = e
            except Exception as e:
                self._log_error(msg=str(e))
                error = unknown_error()

            if error:
                result = BaseResult(error=error)
                status = 500
            else:
                status = 200
                if isinstance(view_result, HttpResponse):
                    return view_result
                result = BaseResult(data=view_result)

            body = result.dumps(result)

            if self.format == self.ACCEPT_JSON:
                return HttpResponse(body, status=status, content_type=self.format)
            else:
                return HttpResponse(body, status=status, content_type=self.ACCEPT_JSON)

        if self.url:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
            url = django_url(self.url, wrapped_f, name=self.slug)
            urlconf.urlpatterns.append(url)

        return wrapped_f

    def _log_error(self, msg):
        logger.error(
            "request_id: {}, message: {}".format(self.request_id, msg),
            exc_info=True,
        )

    def auth_check(self):
        pass

    def _get_data(self):
        if self.request.method == "POST":
            content_type = self.request.META.get("CONTENT_TYPE", "")
            content_type = content_type.split(";")[0]
            if content_type == "application/json":
                if not self.request.body:
                    raise BaseError(code=BaseError.ERROR_EMPTY_REQUEST)

                try:
                    data = ujson.loads(self.request.body)
                except ValueError as e:
                    self._log_error(msg=str(e))
                    raise BaseError(code=BaseError.ERROR_BAD_JSON)
            else:
                data = self.request.POST.dict()

        elif self.request.method == 'GET':
            data = self.request.GET.dict()
        else:
            raise unknown_error()
        self.raw_data = data

    def _validate_data(self):
        if self.data_spec is not None:
            if self.raw_data is None:
                raise BaseError(code=BaseError.ERROR_EMPTY_REQUEST)
            elif not isinstance(self.raw_data, dict):
                raise BaseError(code=BaseError.ERROR_REQUEST_NOT_DICT)

            try:
                self.data = self.data_spec(**self.raw_data)
            except ValidationError as e:
                self._log_error(msg=str(e))
                raise BaseError(code=BaseError.ERROR_VALIDATION)
