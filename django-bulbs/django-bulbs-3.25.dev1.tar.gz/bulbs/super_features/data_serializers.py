from rest_framework import serializers

from djbetty.serializers import ImageFieldSerializer

from bulbs.utils.fields import RichTextField
from bulbs.utils.data_serializers import BaseEntrySerializer, CopySerializer


class GuideToEntrySerializer(BaseEntrySerializer, CopySerializer):
    image = ImageFieldSerializer(required=False, default=None, allow_null=True)


class GuideToChildSerializer(serializers.Serializer):
    og_image_url = serializers.CharField(required=False)
    entries = GuideToEntrySerializer(many=True, required=False, child_label="entry")


class GuideToParentSerializer(serializers.Serializer):
    copy = RichTextField(required=False, field_size="long")
    og_image_url = serializers.CharField(required=False)
    og_description = serializers.CharField(required=False)
