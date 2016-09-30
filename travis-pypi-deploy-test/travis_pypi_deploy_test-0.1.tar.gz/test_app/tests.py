from django.test import TestCase
from views import sample_view
# Create your tests here.


class ViewTest(TestCase):
    def test_sample_view(self):
        output = sample_view("test")
        self.assertEqual(output, "test")
