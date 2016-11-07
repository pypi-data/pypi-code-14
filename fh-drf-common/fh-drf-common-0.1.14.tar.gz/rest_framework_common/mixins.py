

class MeaspkViewSetMixin(object):

    def initial(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            kwargs['pk'] = request.user.pk

        for k, v in kwargs.items():
            if k.startswith('parent_lookup_') and v == 'me':
                kwargs[k] = request.user.pk

        self.kwargs = kwargs

        super(MeaspkViewSetMixin, self).initial(request, *args, **kwargs)
