# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from . import models


class PolyBuilderView(TemplateView):
    """Serve the index of the Polymer App"""
    template_name = 'index.html'

    def main_component(self):
        # TODO: Return None if DoesNo0tExist
        return models.Component.objects.get(is_main=True)


class SharedComponentsView(TemplateView):
    """Serve a bundle of all the components created in admin"""
    template_name = 'shared_components.html'

    def components(self):
        return models.Component.objects.filter(is_main=False)

    def dependencies(self):
        return models.Dependency.objects.all()
