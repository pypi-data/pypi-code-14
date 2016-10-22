from django.utils.module_loading import import_string

from django.shortcuts import Http404

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class EditableContentView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        model = request.query_params.get('model')
        pk = request.query_params.get('pk')
        field = request.query_params.get('field')
        if not model or not pk or not field:
            raise Http404
        try:
            obj = import_string(model).objects.get(pk=pk)
            fields = []
            for f in obj._meta.get_fields():
                if not f.many_to_one and f.related_model is None:
                    fields.append(f.name)
            if field not in fields:
                raise Http404
            content = getattr(obj, field)
            return Response(
                status=status.HTTP_200_OK,
                data={'content': content}
            )
        except (ImportError, AttributeError, ValueError) as e:
            print(e)
            raise Http404

    def patch(self, request):
        model = request.data.get('model')
        pk = request.data.get('pk')
        field = request.data.get('field')
        content = request.data.get('content')
        if not model or not pk or not field:
            raise Http404
        try:
            obj = import_string(model).objects.get(pk=pk)
            fields = []
            for f in obj._meta.get_fields():
                if not f.many_to_one and f.related_model is None:
                    fields.append(f.name)
            if field not in fields:
                raise Http404
            setattr(obj, field, content)
            obj.save()
            return Response(
                status=status.HTTP_200_OK
            )
        except (ImportError, AttributeError, ValueError):
            raise Http404
