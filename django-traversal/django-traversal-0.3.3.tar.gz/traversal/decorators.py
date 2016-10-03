# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse


class render_with_context(object):
    """
    Декоратор для view, позволяющий вместо того, чтобы каждый раз писать render_to_response возвращать
    только список переменных в контексте. Кроме того, в отличие от других подобных декораторов,
    обязательно сам передаёт в шаблон переменную context, с текущим рессурсом
    """
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):

        # our decorated function
        def _render_with_context(request, context, *args, **kwargs):
            context_or_response = func(request, context, *args, **kwargs)
            if isinstance(context_or_response, HttpResponse):
                # it's already a response, just return it
                return context_or_response
            else:
                context_or_response['context'] = context
            # it's a context
            return render(request, self.template_name, context_or_response)

        _render_with_context.__doc__ = func.__doc__
        _render_with_context.__name__ = func.__name__
        _render_with_context.__module__ = func.__module__

        return _render_with_context


class respounse_or_redirect(object):
    """
    Декоратор для traversal api. Возвращает редирект, если в GET есть редирект, иначе HttpRespounse
    """

    def __call__(self, api_func):

        # our decorated api_function
        def _render_with_context(request, *args, **kwargs):
            new_url = api_func(request, *args, **kwargs)
            if 'redirect' in request.GET:
                return redirect(new_url)
            else:
                return HttpResponse(new_url)

        _render_with_context.__doc__ = api_func.__doc__
        _render_with_context.__name__ = api_func.__name__
        _render_with_context.__module__ = api_func.__module__

        return _render_with_context


def resource_register():
    """
    Декоратор для классов ресурсов. регистрирует ресурсы в регистраторе, чтобы другие ресурсы могли получить к ним доступ
    """
    from traversal.resource import resource_registrator, Resource

    def _resource_class_wrapper(resource_class):

        # if not isinstance(resource_class, Resource):
        #     raise ValueError(u'Ресурc должен быть потомком класса Resource')

        resource_registrator.register(resource_class)

        return resource_class
    return _resource_class_wrapper

