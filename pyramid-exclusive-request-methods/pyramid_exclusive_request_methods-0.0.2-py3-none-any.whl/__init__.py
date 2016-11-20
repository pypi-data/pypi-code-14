from zope.interface import implementedBy, Interface
from zope.interface.interfaces import IInterface
from pyramid.config.predicates import RequestMethodPredicate
from pyramid.config.util import as_sorted_tuple, MAX_ORDER
from pyramid.compat import string_types, text_type
from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.viewderivers import predicated_view, INGRESS
from pyramid.interfaces import IRequest, IRouteRequest, IView, IViewClassifier, ISecuredView, IMultiView
from pyramid.view import view_config


class ViewWrapper(object):
    def __init__(self, view, route_name, context, name):
        self.view = view
        self.route_name = route_name
        self.context = context
        self.name = name
        self.__name__ = getattr(view, '__name__')

    def __call__(self, context, request):
        return self.view(context, request)


class ExclusiveView(object):
    def __init__(self, wrapped, request_methods):
        self.wrapped = wrapped
        self.request_methods = request_methods

    def __call__(self, context, request):
        if request.method not in self.request_methods:
            raise HTTPMethodNotAllowed(text=u'Predicate mismatch for view %s (request_method = %s)' % (getattr(self.wrapped, '__name__', self.wrapped), ','.join(self.request_methods)))
        return self.wrapped(context, request)


def find_existing_views(registry, route_name, context, name):
    if route_name:
        request_iface = registry.queryUtility(IRouteRequest, name=route_name)
    else:
        request_iface = IRequest
    if context is None:
        context = Interface
    if not IInterface.providedBy(context):
        context = implementedBy(context)

    for view_type in (IView, ISecuredView, IMultiView):
        view = registry.adapters.registered(
            (IViewClassifier, request_iface, context),
            view_type,
            name
            )
        if view is not None:
            if view_type is IMultiView:
                return [view for view, _, _ in view.views]
            else:
                return [view]
    return []


def find_existing_exclusive_view(registry, route_name, context, name):
    views = find_existing_views(registry, route_name, context, name) 
    for view in views:
        while view is not None:
            if isinstance(view, ExclusiveView):
                return view
            view = getattr(view, '__wraps__', None)
    return None


def exclusive_request_method_view_deriver(view, info):
    request_method_pred = None
    for pred in info.predicates:
        if isinstance(pred, RequestMethodPredicate):
            request_method_pred = pred
            break
    if request_method_pred is not None:
        original_view = info.original_view
        if isinstance(original_view, ViewWrapper):
            old_view = find_existing_exclusive_view(info.registry, original_view.route_name, original_view.context, original_view.name)
            if old_view is None:
                request_methods = request_method_pred.val
                info.predicates.remove(request_method_pred)
                info.order = MAX_ORDER + 1 # make sure that the view has the lowest precedence.
                return ExclusiveView(view, request_methods)
    return view


def add_exclusive_view(
        config,
        view=None,
        name="",
        for_=None,
        permission=None,
        request_type=None,
        route_name=None,
        request_method=None,
        request_param=None,
        containment=None,
        attr=None,
        renderer=None,
        wrapper=None,
        xhr=None,
        accept=None,
        header=None,
        path_info=None,
        custom_predicates=(),
        context=None,
        decorator=None,
        mapper=None,
        http_cache=None,
        match_param=None,
        check_csrf=None,
        require_csrf=None,
        **view_options):
    config.add_view(
        ViewWrapper(view, route_name, context, name),
        name,
        for_,
        permission,
        request_type,
        route_name,
        request_method,
        request_param,
        containment,
        attr,
        renderer,
        wrapper,
        xhr,
        accept,
        header,
        path_info,
        custom_predicates,
        context,
        decorator,
        mapper,
        http_cache,
        match_param,
        check_csrf,
        require_csrf,
        **view_options
        )


# stolen from pyramid.view
class exclusive_view_config(view_config):
    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_exclusive_view(view=ob, **settings)

        info = self.venusian.attach(wrapped, callback, category='pyramid',
                                    depth=depth + 1)

        if info.scope == 'class':
            if settings.get('attr') is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo
        return wrapped


def includeme(config):
    config.add_view_deriver(exclusive_request_method_view_deriver, under=INGRESS)
    config.add_directive('add_exclusive_view', add_exclusive_view)
