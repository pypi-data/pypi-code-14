"main testing module"
import os
import hashlib
if __name__ == '__main__': # pragma: no cover
    import django
    django.setup()
    THIS = os.path.split(__file__)[1].split('.')[0] # This files module name
    django.core.management.call_command('test', THIS)

from django.test import TestCase
from django.core.management import call_command
from django_g11n.models import Region, RegionChain
from django_g11n.tools import region

import requests

# Create your tests here.
class UpdateRegionTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(UpdateRegionTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        TestCase.setUp(self)
        self.call_command = call_command

    def tearDown(self):
        pass

    def test_001_insert(self):
        self.call_command('update_regions')

    def test_010_update(self):
        # Essentially calling the command twice
        self.call_command('update_regions')
        Region.objects.create(numeric=987, english='That')
        instance = Region.objects.get(numeric='001')
        instance.english = 'Changed'
        instance.save()
        self.assertEqual(str(instance), '001 Changed')
        RegionChain.objects.create(lower=instance, upper=instance)
        self.call_command('update_regions')
        instance = Region.objects.get(numeric='001')
        self.assertNotEqual(instance.english, 'Changed')

    def test_020_update_reference(self):
        self.call_command('update_countries')
        self.call_command('update_regions')
        instance = Region.objects.get(numeric='826')
        self.assertEqual(instance.reference.numeric, 826)

    def test_030_latest_version(self):
        # Just checking if the page has changed.
        got = requests.get(region.URL)
        text = got.text.lower().strip()
        text = text.split('<body')[1]
        text = text.split('</body')[0]
        digest = hashlib.md5(text.encode('utf-8')).hexdigest()
        self.assertEqual(region.HASH, digest)
