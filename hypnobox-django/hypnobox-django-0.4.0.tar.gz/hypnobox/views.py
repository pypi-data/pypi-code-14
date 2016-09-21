# -*- coding: utf-8 -*-
from django.views.generic import CreateView

from .models import Lead
from .forms import LeadForm
from .specs import get_spec


class LeadCreateView(CreateView):
    form_class = LeadForm
    model = Lead

    def get_form_kwargs(self):
        kwargs = super(LeadCreateView, self).get_form_kwargs()
        initial = {
            'product_id': self.request.GET.get('product_id'),
            'description': self.request.GET.get('description'),
            'media': self.request.GET.get('media'),
        }
        kwargs['initial'] = initial
        return kwargs

    def get_success_url(self):
        spec = get_spec()
        return spec.get_chat_url(self.object)
