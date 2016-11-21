from datetime import datetime
from django.conf import settings
from django.http import HttpRequest
import requests

class PerfMiddleware(object):
    PERF_INGEST_URL = "https://data.perf.sh/ingest"

    def process_request(self, request):
        request._perf_request_time = datetime.now()

    def process_template_response(self, request, response):
        api_key = self.get_api_key()
        if api_key != None:
            response_time = datetime.now() - request._perf_request_time
            payload = [{
                "request_url": request.build_absolute_uri(),
                "request_method": request.method,
                "status_code": response.status_code,
                "time_in_millis": round(response_time.microseconds / 1000, 0),
                "normalized_uri": request.build_absolute_uri()
            }]
            headers = {
                "X-Perf-Public-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "PerfAgent-Django/0.1.0"
            }
            r = requests.post(PerfMiddleware.PERF_INGEST_URL, json=payload, headers=headers)
        return response

    def get_api_key(_):
        perf_settings = getattr(settings, "PERF_CONFIG", None)
        if perf_settings != None:
            return perf_settings.get("api_key", None)
        return None
