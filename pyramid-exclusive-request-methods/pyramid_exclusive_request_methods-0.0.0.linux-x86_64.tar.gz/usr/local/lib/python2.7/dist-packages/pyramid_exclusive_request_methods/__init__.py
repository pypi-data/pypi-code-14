from pyramid.config.predicates import RequestMethodPredicate
from pyramid.config.util import as_sorted_tuple
from pyramid.compat import string_types, text_type
from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.viewderivers import predicated_view, INGRESS

Everything = None

class EverythingType(object):
    def __contains__(self, item):
        return True

    def __new__(cls):
        if Everything is None:
            return super(EverythingType, cls).__new__(cls)
        return Everything

Everything = EverythingType()


class Exclusively(text_type):
    def __new__(cls, wrapped):
        if isinstance(wrapped, string_types):
            self = super(Exclusively, cls).__new__(cls, wrapped)
        else:
            self = super(Exclusively, cls).__new__(cls)
        self.wrapped = wrapped
        return self

    def __eq__(self, that):
        return self.wrapped == that

    def __gt__(self, that):
        return self.wrapped > that

    def __lt__(self, that):
        return self.wrapped < that

    def __contains__(self, item):
        return item in self.wrapped


def exclusive_request_method_view_deriver(view, info):
    request_method_pred = None
    for pred in info.predicates:
        if isinstance(pred, RequestMethodPredicate):
            request_method_pred = pred
            break
    if request_method_pred is not None:
        for x in request_method_pred.val:
            if isinstance(x, Exclusively):
                break
        else:
            x = None
        if x is not None:
            request_methods = as_sorted_tuple(x.wrapped)
            if 'GET' in request_methods and 'HEAD' not in request_methods:
                request_methods = as_sorted_tuple(request_methods + ('HEAD',))
            request_method_pred.val = Everything
            def wrapped_view(context, request):
                if request.method not in request_methods:
                    raise HTTPMethodNotAllowed(text=u'Predicate mismatch for view %s (request_method = %s)' % (getattr(view, '__name__', view), ','.join(request_methods)))
                return view(context, request)
            return wrapped_view
    return view

def includeme(config):
    config.add_view_deriver(exclusive_request_method_view_deriver, under=INGRESS)
