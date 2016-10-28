from flask import after_this_request, jsonify, redirect, render_template, request, Response, send_file, url_for
from flask.views import MethodView


def url_rule(app, rule, *args, **kwargs):
    """A class decorator for generic views, which provides the same feel of the @app.route
    decorator on normal function views.

    :param cls: A pluggable view to decorate
    :return: The pluggable view
    """
    def decorator(cls):
        add_url_rule = cls.add_url_rule \
                if isinstance(rule, basestring) \
                else cls.add_url_rules

        add_url_rule(app, rule, *args, **kwargs)

        return cls

    return decorator


class GenericView(MethodView):
    """The base generic view class.
    """
    def dispatch_request(self, *args, **kwargs):
        """Sets self.args and self.kwargs from the request for convenience, in
        case there is a context in the code where the data is not directly
        passed in, but you need access to it.
        """
        self.args = args
        self.kwargs = kwargs
        return super(GenericView, self).dispatch_request(*args, **kwargs)

    @classmethod
    def add_url_rule(cls, app, rule, endpoint, view_func=None, **options):
        """Convenience for registering this view on an app or blueprint,
        responding to the provided rule and given the specified endpoint name.

        :param app: A flask app or blueprint
        :param rule: The url pattern to match
        :param endpoint: The name of this route, for use with :func:`~flask.url_for`
        :param view_func: A reference to the previous view func, if matching multiple routes
        :param options: Optional arguments passed directly into :meth:`Flask.add_url_rule` or
                        :meth:`Blueprint.add_url_rule` depending on if `app` is a Flask or
                        Blueprint instance
        """
        if not view_func:
            view_func = cls.as_view(endpoint)

        app.add_url_rule(rule, view_func=view_func, **options)

        return view_func

    @classmethod
    def add_url_rules(cls, app, rules, endpoint, view_func=None, **options):
        """If there needs to be multiple endpoints mapped to a single view, this class-method
        should be used in order to guarantee the view_func is the same. Takes the same arguments as
        :meth:`add_url_rule`, with the only exception being that `rules` is a list of patterns.

        :param rules: A list of url patterns to match
        """
        for rule in rules:
            view_func = cls.add_url_rule(app, rule, endpoint, view_func, **options)

        return view_func


class ResponseMixin(object):
    def render_response(self, **context):
        """Renders a response, optionally with the provided context.

        :param context: An optional dict for use in a rendered response.
        """
        raise NotImplementedError


class ContextMixin(object):
    def get_context_data(self, **context):
        """Constructs and returns a dict for use as context in a rendered response. This method
        should only be used when directly providing context intended to be used in a response.
        There should be no side-effects introduced here.
        
        If you need to provide a class-member set of shared context for use in an inherited mixin
        chain, then you should override :meth:`~GenericView.dispatch_request` and assign that
        shared context before calling the `super` implementation of that method.

        :param context: An optional dict for use in a rendered response.
        :return: A dict
        """
        return context


class RedirectMixin(object):
    redirect_endpoint = None

    def redirect(self, **context):
        """Redirect to another URL with the provided context getting passed to url_for
        """
        url = self.get_redirect_url(**context)
        return redirect(url)

    def get_redirect_url(self, **context):
        """Returns a URL that the view will redirect to by default when the
        form is validated.
        """
        redirect_endpoint = self.get_redirect_endpoint(**context)
        if redirect_endpoint:
            return url_for(redirect_endpoint, **context)

        return request.url

    def get_redirect_endpoint(self, **context):
        """Returns the endpoint to redirect to with the provided context.
        """
        return self.redirect_endpoint


class RedirectView(ContextMixin, RedirectMixin, GenericView):
    def get(self, *args, **kwargs):
        """Adds a generic view for redirecting to another endpoint.
        """
        context = self.get_context_data(**kwargs)
        return self.redirect(**context)


class TemplateResponseMixin(ResponseMixin):
    """A mixin for rendering a template.
    """
    #: The name of the template to render
    template_name = None

    def get_template(self, **context):
        """Gets the template that needs to be rendered.
        """
        return self.template_name

    def render_response(self, **context):
        """Renders a template with the provided context. If a pjax template is
        defined, it will attempt to serve it if the request headers indicated
        that a PJAX response is needed.
        """
        template = self.get_template(**context)
        return render_template(template, **context)


class TemplateMixin(ContextMixin, TemplateResponseMixin):
    """A template response with context.
    """


class PjaxResponseMixin(object):
    """A mixin for rendering a PJAX response.
    """
    pjax_template_name = None

    @property
    def is_pjax_request(self):
        """Returns True if it's a PJAX request, False otherwise.
        """
        return 'X-PJAX' in request.headers

    def get_template(self, **context):
        """Renders a PJAX-friendly response.
        """
        if self.is_pjax_request:
            pjax_template_name = self.get_pjax_template_name(**context)

            if pjax_template_name:
                return pjax_template_name

        return super(PjaxResponseMixin, self).get_template(**context)

    def get_context_data(self, **context):
        """Adds PJAX information to the context, for use in rendered templates.
        """
        context = super(PjaxResponseMixin, self).get_context_data(**context)

        if self.is_pjax_request:
            context['pjax_container'] = request.headers.get('X-Pjax-Container')

            pjax_template_name = self.get_pjax_template_name(**context)
            if pjax_template_name:
                context['pjax_template'] = pjax_template_name

        return context

    def get_pjax_template_name(self, **context):
        """Gets the PJAX-friendly template that could potentially be rendered.
        """
        return self.pjax_template_name


class PjaxTemplateMixin(PjaxResponseMixin, TemplateMixin):
    """A PJAX-friendly template response.
    """


class TemplateView(PjaxTemplateMixin, GenericView):
    """A view that renders a template on a GET request.
    """
    def get(self, *args, **kwargs):
        """Gets the context data and renders a template with it.
        """
        context = self.get_context_data(**kwargs)
        return self.render_response(**context)


class FormMixin(ResponseMixin):
    """A mixin for processing a form.
    """
    #: A form class used to process POST data. Must inherit from flask-wtf form
    form_cls = None

    def process_form(self):
        """Workflow for processing a form, from flask-wtf. If the request method is POST and the
        form is validated, it returns the result of `self.form_valid(form)`. If the form data is
        invalid, or the request method is GET, it returns the result of `self.form_invalid(form)`.
        """
        form = self.get_form()

        if form.validate_on_submit():
            return self.form_valid(form)

        return self.form_invalid(form)

    def get_form(self):
        """Instantiates a new form from the form class and any arguments that
        are defined for its constructor through self.get_form_kwargs()
        """
        form_cls = self.get_form_cls()
        form_kwargs = self.get_form_kwargs()
        return form_cls(**form_kwargs)

    def get_form_cls(self):
        """Default behavior is to return the form_cls defined on this instance.
        """
        return self.form_cls

    def get_form_kwargs(self):
        """Any arguments that need to be passed to the form class constructor
        should be defined here and returned as a dict.
        """
        form_kwargs = {}
        form_obj = self.get_form_obj()
        if form_obj:
            form_kwargs['obj'] = form_obj
        return form_kwargs

    def get_form_obj(self):
        """ The form object to pre-populate the form with.
        """

    def form_valid(self, form, **context):
        """Default behavior on form validation is to simply redirect to the URL
        returned from self.get_success_url()
        """
        context = self.get_context_data(form=form, **context)
        return self.render_response(**context)

    def form_invalid(self, form, **context):
        """If a form is not valid, the default behavior is to render the
        template and including the form as context.
        """
        context = self.get_context_data(form=form, **context)
        return self.render_response(**context)


class ProcessFormView(FormMixin, GenericView):
    def post(self, *args, **kwargs):
        """Creates a form and validates it. If validation is successful, it
        will call self.form_valid(form). Otherwise, it will call
        self.form_invalid(form). The default behavior for each of these methods
        is documented in the FormMixin class.
        """
        return self.process_form()

        
class FormView(PjaxTemplateMixin, RedirectMixin, ProcessFormView):
    def get(self, *args, **kwargs):
        """Creates a form and includes it as context to a template that will be
        rendered.
        """
        form = self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_response(**context)

    def form_valid(self, form, **context):
        """Default behavior on form validation is to simply redirect to the URL
        returned from self.get_success_url()
        """
        return self.redirect(**context)


class JsonResponseMixin(ResponseMixin):
    def render_response(self, **context):
        """Returns a JSON response with the provided context.
        """
        return jsonify(**context)


class JsonMixin(ContextMixin, JsonResponseMixin):
    """A json response with context.
    """


class AjaxView(JsonMixin, GenericView):
    def get(self, *args, **kwargs):
        """Sends a jsonified response from a GET request.
        """
        context = self.get_context_data()
        return self.render_response(**context)


class AjaxFormView(JsonMixin, ProcessFormView):
    """Processes an AJAX form.
    """
    def form_invalid(self, form, **context):
        context.setdefault('errors', form.errors)
        context = self.get_context_data(form=form, **context)

        response = self.render_response(**context)
        response.status_code = 400
        return response

    def get_context_data(self, form=None, **context):
        return super(AjaxFormView, self).get_context_data(**context)


class CustomResponseMixin(object):
    response_cls = Response

    def dispatch_request(self, *args, **kwargs):
        """Returns a custom Response object, using the result of the response from the dispatched
        request as well as any custom response parameters.
        """
        response = super(CustomResponseMixin, self).dispatch_request(*args, **kwargs)
        response_cls = self.get_response_cls()
        response_kwargs = self.get_response_kwargs(response)
        return response_cls(response=response, **response_kwargs)

    def get_response_cls(self):
        """Returns a Response class.
        """
        return self.response_cls

    def get_response_kwargs(self, response):
        """Returns a dict of kwargs passed into the constructor of the response class returned from
        self.get_response_cls()
        """
        return {}


class MimeTypeMixin(object):
    mimetype = None

    def get_mimetype(self):
        """Returns a mimetype.
        """
        return self.mimetype


class MimeTypeResponseMixin(MimeTypeMixin, CustomResponseMixin):
    def get_response_kwargs(self, response):
        """If a mimetype is specified, include it when instantiating the Response instance.
        """
        response_kwargs = super(MimeTypeResponseMixin, self).get_response_kwargs(response)
        response_kwargs.setdefault('mimetype', self.get_mimetype())
        return response_kwargs


class SendFileMixin(MimeTypeMixin):
    #: A file pointer of path to a file
    filename_or_fp = None

    #: By default, use Content-Disposition: attachment
    as_attachment = True

    #: The filename of the attachment
    attachment_filename = None

    def get_filename_or_fp(self):
        """Returns a filename or file pointer.
        """
        return self.filename_or_fp

    def get_as_attachment(self):
        """Returns True if the file should be served as an attachment, False otherwise.
        """
        return self.as_attachment

    def get_attachment_filename(self):
        """Returns the filename for the attachment.
        """
        return self.attachment_filename

    def get_sendfile_kwargs(self):
        """Returns a dict of arguments to be passed to :func:`~flask.send_file`.
        """
        return {}

    def send_file(self):
        """Returns the result of :func:`~flask.send_file`
        """
        send_file_kwargs = self.get_sendfile_kwargs()
        send_file_kwargs.setdefault('filename_or_fp', self.get_filename_or_fp())
        send_file_kwargs.setdefault('mimetype', self.get_mimetype())
        send_file_kwargs.setdefault('as_attachment', self.get_as_attachment())
        send_file_kwargs.setdefault('attachment_filename', self.get_attachment_filename())
        return send_file(**send_file_kwargs)


class SendFileView(SendFileMixin, GenericView):
    def get(self, *args, **kwargs):
        """Returns the response from :func:`~flask.send_file`.
        """
        return self.send_file()


class SetCookiesMixin(object):

    def dispatch_request(self, *args, **kwargs):
        after_this_request(self.add_response_cookies)
        return super(SetCookiesMixin, self).dispatch_request(*args, **kwargs)

    def add_response_cookies(self, response):
        """Sets cookies on the response object.
        """
        for cookie_context in self.get_response_cookies(response):
            response.set_cookie(**cookie_context)
        return response

    def get_response_cookies(self, response):
        return []


class JsonFormMixin(object):
    """ Mixin to process forms using the from_json api. Please note: this mixin requires wtforms-json to be installed.
    """

    skip_unknown_keys = True
    form_json = None
    csrf_enabled = False

    def get_form(self):
        form_cls = self.get_form_cls()
        form_kwargs = self.get_form_kwargs()
        return form_cls.from_json(**form_kwargs) if 'formdata' in form_kwargs else form_cls(**form_kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(JsonFormMixin, self).get_form_kwargs()
        self.form_json = self.get_form_json()
        if 'formdata' not in form_kwargs and self.form_json:
            form_kwargs['formdata'] = self.form_json
            form_kwargs.setdefault('skip_unknown_keys', self.skip_unknown_keys)
            form_kwargs.setdefault('csrf_enabled', self.get_csrf_enabled())
        return form_kwargs

    def get_form_json(self):
        return request.get_json()

    def get_csrf_enabled(self):
        return self.csrf_enabled


class JsonFormView(JsonFormMixin, AjaxFormView):
    """ View to process forms using the from_json api.
    """
    def get_context_data(self, form=None, **context):
        context = super(JsonFormView, self).get_context_data(form=form, **context)
        context.setdefault('status', 'error' if context.get('errors') else 'success')
        return context


class CORSMixin(object):
    """ Mixin to add CORS response headers.
    """

    cors_allow_origin = '*'
    cors_allow_credentials = True
    cors_allow_methods = None

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view_func = super(CORSMixin, cls).as_view(name, *class_args, **class_kwargs)
        view_func.provide_automatic_options = False
        if view_func.methods and 'OPTIONS' not in view_func.methods:
            view_func.methods.append('OPTIONS')
        return view_func
    
    def dispatch_request(self, *args, **kwargs):
        after_this_request(self.add_cors_response_headers)
        return super(CORSMixin, self).dispatch_request(*args, **kwargs)

    def options(self, *args, **kwargs):
        return ''

    def add_cors_response_headers(self, response):
        response.headers['Access-Control-Allow-Origin'] = self.get_cors_allow_origin()
        response.headers['Access-Control-Allow-Credentials'] = 'true' if self.get_cors_allow_credentials() else 'false'
        response.headers['Access-Control-Allow-Methods'] = ', '.join(self.get_cors_allow_methods())
        return response

    def get_cors_allow_origin(self):
        return self.cors_allow_origin

    def get_cors_allow_credentials(self):
        return self.cors_allow_credentials

    def get_cors_allow_methods(self):
        return self.cors_allow_methods or self.methods
