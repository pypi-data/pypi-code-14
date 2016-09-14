from __future__ import unicode_literals, absolute_import

import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from tri.form import Form
from tri.declarative import extract_subkeys, setdefaults_path
from tri.struct import Struct


def edit_object(
        request,
        instance,
        redirect_to=None,
        on_save=lambda **kwargs: None,
        render=render_to_response,
        redirect=lambda request, redirect_to, form: HttpResponseRedirect(redirect_to),
        **kwargs):
    assert 'is_create' not in kwargs
    assert 'model' not in kwargs
    assert instance is not None
    model = instance.__class__
    return create_or_edit_object(
        request,
        model,
        is_create=False,
        instance=instance,
        redirect_to=redirect_to,
        on_save=on_save,
        render=render,
        redirect=redirect,
        **kwargs)


def create_object(
        request,
        model,
        redirect_to=None,
        on_save=lambda **kwargs: None,
        render=render_to_response,
        redirect=lambda request, redirect_to, form: HttpResponseRedirect(redirect_to),
        **kwargs):
    assert 'is_create' not in kwargs
    return create_or_edit_object(
        request,
        model,
        is_create=True,
        redirect_to=redirect_to,
        on_save=on_save,
        render=render,
        redirect=redirect,
        **kwargs)


def create_or_edit_object(
        request,
        model,
        is_create,
        instance=None,
        redirect_to=None,
        on_save=lambda **kwargs: None,
        render=render_to_response,
        redirect=lambda request, redirect_to, form: HttpResponseRedirect(redirect_to),
        **kwargs):
    kwargs = setdefaults_path(
        Struct(),
        kwargs,
        template_name='tri_form/create_or_edit_object_block.html',
        form__class=Form.from_model,
        form__request=request,
        form__model=model,
        form__instance=instance,
        form__data=request.POST if request.method == 'POST' else None,
    )
    p = kwargs.form
    form = p.pop('class')(**p)

    for key, value in request.GET.items():
        if key.startswith('__'):
            remaining_key = key[2:]
            expected_prefix = form.endpoint_dispatch_prefix
            if expected_prefix is not None:
                parts = remaining_key.split('__', 1)
                prefix = parts.pop(0)
                if prefix != expected_prefix:
                    return
                remaining_key = parts[0] if parts else None
            data = form.endpoint_dispatch(key=remaining_key, value=value)
            if data:
                return HttpResponse(json.dumps(data), content_type='application/json')

    # noinspection PyProtectedMember
    model_verbose_name = kwargs.get('model_verbose_name', model._meta.verbose_name.replace('_', ' '))

    if request.method == 'POST' and form.is_valid():
        if is_create:
            assert instance is None
            instance = model()
            for field in form.fields:
                if not field.extra.get('django_related_field', False):
                    form.apply_field(field=field, instance=instance)

            instance.save()
        form.apply(instance)
        instance.save()

        kwargs['instance'] = instance
        on_save(**kwargs)

        return create_or_edit_object_redirect(is_create, redirect_to, request, redirect, form)

    c = {
        'form': form,
        'is_create': is_create,
        'object_name': model_verbose_name,
    }
    c.update(kwargs.get('render_context', {}))
    kwargs.pop('render_context', None)

    kwargs_for_render = extract_subkeys(kwargs, 'render', {
        'context_instance': RequestContext(request, c),
        'template_name': kwargs['template_name'],
    })
    return render(**kwargs_for_render)


def create_or_edit_object_redirect(is_create, redirect_to, request, redirect, form):
    if redirect_to is None:
        if is_create:
            redirect_to = "../"
        else:
            redirect_to = "../../"  # We guess here that the path ends with '<pk>/edit/' so this should end up at a good place
    return redirect(request=request, redirect_to=redirect_to, form=form)
