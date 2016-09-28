class DartiumDetectionMiddleware:

    @staticmethod
    def process_request(request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if '(Dart)' in user_agent:
            request.is_dartium = True
        else:
            request.is_dartium = False
