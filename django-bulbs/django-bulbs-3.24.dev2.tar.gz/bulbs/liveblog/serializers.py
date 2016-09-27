from django.contrib.auth import get_user_model
from rest_framework import serializers

from bulbs.content.models import Content
from bulbs.content.serializers import AUTHOR_FILTER, AuthorField

from .models import LiveBlogEntry, LiveBlogResponse
from .utils import get_liveblog_author_model


User = get_user_model()
LIVEBLOG_MODEL = get_liveblog_author_model()


class LiveBlogSerializerMixin(serializers.Serializer):

    recirc_content = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                        queryset=Content.objects.all())

    class Meta:
        abstract = True


class LiveBlogResponseSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=LIVEBLOG_MODEL.objects.all())

    class Meta:
        model = LiveBlogResponse
        fields = ('author', 'body', 'internal_name')


class LiveBlogEntrySerializer(serializers.ModelSerializer):

    created_by = AuthorField(allow_null=True, required=False,
                             queryset=User.objects.filter(**AUTHOR_FILTER))

    updated_by = AuthorField(allow_null=True, required=False,
                             queryset=User.objects.filter(**AUTHOR_FILTER))

    responses = LiveBlogResponseSerializer(many=True, required=False)

    authors = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                 queryset=LIVEBLOG_MODEL.objects.all())

    recirc_content = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                        queryset=Content.objects.all())

    class Meta:
        model = LiveBlogEntry

    def create(self, validated_data):
        responses = validated_data.pop('responses', [])

        entry = super(LiveBlogEntrySerializer, self).create(validated_data)

        # Create nested responses
        for idx, response in enumerate(responses):
            LiveBlogResponse.objects.create(entry=entry, ordering=idx, **response)

        return entry

    def update(self, instance, validated_data):
        responses = validated_data.pop('responses', [])

        entry = super(LiveBlogEntrySerializer, self).update(instance, validated_data)

        # Swap in brand new list of responses (easier than trying to match up)
        entry.responses.all().delete()
        for idx, response in enumerate(responses):
            LiveBlogResponse.objects.create(entry=entry, ordering=idx, **response)

        return entry
