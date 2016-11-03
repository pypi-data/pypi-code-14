from ovp_uploads.models import UploadedImage

from rest_framework import serializers

class UploadedImageSerializer(serializers.ModelSerializer):
  image_url = serializers.SerializerMethodField()
  image_small_url = serializers.SerializerMethodField()
  image_medium_url = serializers.SerializerMethodField()
  image_large_url = serializers.SerializerMethodField()

  class Meta:
    model = UploadedImage
    fields = ('id', 'user', 'image', 'image_url', 'image_small_url', 'image_medium_url', 'image_large_url')
    read_only_fields = ('image_small', 'image_medium', 'image_large')
    extra_kwargs = {'image': {'write_only': True}}

  def get_image_url(self, obj):
    return self.context['request'].build_absolute_uri(obj.image.url)

  def get_image_small_url(self, obj):
    return self.context['request'].build_absolute_uri(obj.image_small.url)

  def get_image_medium_url(self, obj):
    return self.context['request'].build_absolute_uri(obj.image_medium.url)

  def get_image_large_url(self, obj):
    return self.context['request'].build_absolute_uri(obj.image_large.url)
