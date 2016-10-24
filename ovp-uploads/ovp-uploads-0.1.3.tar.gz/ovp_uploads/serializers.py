from ovp_uploads.models import UploadedImage

from rest_framework import serializers

class UploadedImageSerializer(serializers.ModelSerializer):
  image_url = serializers.CharField(source="get_image_url", required=False, read_only=True)
  image_small_url = serializers.CharField(source="get_image_small_url", required=False, read_only=True)
  image_medium_url = serializers.CharField(source="get_image_medium_url", required=False, read_only=True)
  image_large_url = serializers.CharField(source="get_image_large_url", required=False, read_only=True)

  class Meta:
    model = UploadedImage
    fields = ('id', 'user', 'image', 'image_url', 'image_small_url', 'image_medium_url', 'image_large_url')
    read_only_fields = ('image_small', 'image_medium', 'image_large')
