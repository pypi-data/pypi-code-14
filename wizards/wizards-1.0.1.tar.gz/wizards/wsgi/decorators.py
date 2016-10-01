import functools


def serializable_response(func):
    """Decorate a controller method that returns a tuple consisting
    of a :class:`~wizards.wsgi.responsepayload.ResponsePayload` object,
    integer specifying the status (optional), dictionary holding the
    headers (optional).
    """

    @functools.wraps(func)
    def wrapped(self, request, **kwargs):
        payload, *args = func(self, request, **kwargs)
        return self.render_to_response(
            payload=payload.serialize(self.serializer.serialize),
            content_type=self.serializer.content_type,
            **dict(zip(['status','headers'], args))
        )

    return wrapped
