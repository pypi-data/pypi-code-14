# encoding: utf-8
from django.db import connections
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import ResolverMatch

import time

from .models import Request, SQLEntry


class SQLAnalysisMiddleware(object):
    """
    Analysis SQL
    """

    def __init__(self):
        self.__start = None

    def process_request(self, request):
        self.__start = time.time()

    def process_response(self, request, response):
        if not settings.DEBUG or request.path.startswith('/analysis/'):
            return response
        sql_list = []
        sql_used = 0
        sql_times = 0
        view_func_path = request.resolver_match._func_path if isinstance(request.resolver_match,
                                                                         ResolverMatch) else 'N/A'
        for db_alias, db_info in settings.DATABASES.items():
            for query in connections[db_alias].queries:
                if 'SQL_AUTO_IS_NULL' in query['sql']:
                    continue
                sql_list.append({'sql': query['sql'], 'time': query['time'], 'db': db_info.get('NAME', 'N/A')})
                sql_used += float(query['time'])
                sql_times += 1
        if len(sql_list) < 1:
            return response
        req = Request.objects.using('analysis_sqlite3').create(
            view_func_path=view_func_path,
            url=request.path,
            method=request.method,
            date=timezone.now(),
            sql_times=sql_times,
            sql_used=sql_used,
            request_used=time.time() - self.__start
        )
        SQLEntry.objects.using('analysis_sqlite3').bulk_create(
            [SQLEntry(request=req, sql=query['sql'], time=query['time'], db=query['db']) for query in sql_list])
        return response
