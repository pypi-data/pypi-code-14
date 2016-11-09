from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from ovp_uploads.models import UploadedImage
from ovp_uploads.serializers import UploadedImageSerializer
from ovp_users.models import User

from PIL import Image

from tempfile import NamedTemporaryFile


class UploadedImageSerializerTestCase(TestCase):
  def test_image_urls(self):
    """Assert that image object returns url"""
    user = User.objects.create_user('test_image_urls@test.com', 'validpassword')

    client = APIClient()
    client.force_authenticate(user=user)

    image = Image.new('RGB', (100, 100))
    tmp_file = NamedTemporaryFile()
    image.save(tmp_file, format="JPEG")
    tmp_file.seek(0) # otherwise we start reading at the end

    data = {
      'image': tmp_file
    }

    response = client.post(reverse('upload-images-list'), data, format="multipart")

    self.assertTrue(response.status_code == 201)

    img_id = response.data['id']
    img = UploadedImage.objects.get(pk=img_id)

    factory = APIRequestFactory()
    request = factory.post('/')
    serializer = UploadedImageSerializer(instance=img, context={'request': request})

    test_url = 'http://testserver/user-uploaded/images'

    self.assertTrue(test_url in serializer.get_image_url(img))
    self.assertTrue(test_url in serializer.get_image_small_url(img))
    self.assertTrue(test_url in serializer.get_image_medium_url(img))
    self.assertTrue(test_url in serializer.get_image_large_url(img))

    self.assertTrue(img.uuid in serializer.get_image_url(img))
    self.assertTrue(img.uuid in serializer.get_image_small_url(img))
    self.assertTrue(img.uuid in serializer.get_image_medium_url(img))
    self.assertTrue(img.uuid in serializer.get_image_large_url(img))
