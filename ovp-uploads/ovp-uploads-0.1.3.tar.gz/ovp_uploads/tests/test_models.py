from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_uploads.models import UploadedImage
from ovp_users.models import User

from uuid import UUID

from PIL import Image

from tempfile import NamedTemporaryFile


def is_valid_uuid(uuid_to_test, version=4):
  try:
    uuid_obj = UUID(uuid_to_test, version=version)
  except: # pragma: no cover
    return False

  return str(uuid_obj) == uuid_to_test

class UploadedImageModelTestCase(TestCase):
  def test_str_return_uuid(self):
    """Assert that image model __str__ method returns uuid"""
    img = UploadedImage()
    img.save()

    uuid = img.__str__()

    self.assertTrue(is_valid_uuid(uuid))

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

    self.assertTrue(img.get_image_url())
    self.assertTrue(img.get_image_small_url())
    self.assertTrue(img.get_image_medium_url())
    self.assertTrue(img.get_image_large_url())
