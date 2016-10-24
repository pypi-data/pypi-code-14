class CampaignMiddleware(object):
    """
    Middleware that persists Google Analytics UTM parameters in user session.

    Note:
        The 'campaign' dict aims to be compatible with Segment context attributes,
        see: https://segment.com/docs/spec/common/#context
    """
    params = {
        'name': 'utm_campaign',
        'source': 'utm_source',
        'medium': 'utm_medium',
        'term': 'utm_term',
        'content': 'utm_content',
    }

    def process_request(self, request):
        campaign = {}

        for k, v in self.params.items():
            if request.GET.get(v):
                campaign[k] = request.GET.get(v)

        if campaign:
            request.session.update({'campaign': campaign})
