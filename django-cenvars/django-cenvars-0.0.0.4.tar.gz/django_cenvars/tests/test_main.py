"""
Then main unit tests.
"""
from io import StringIO
import os
from django.conf import settings
from django.test import TestCase
from django.core.management import call_command

from django_cenvars import models
from django_cenvars.tools import codec

settings.RSA_KEYSIZE = 512 # For testing purposes, make it a bit faster.

# pylint: disable=no-member
class TestMain(TestCase):
    "Main testing."
    def _create_environments(self):
        "Create some data"
        gen1 = models.Environment.objects.create(label='gen1')
        gen2 = models.Environment.objects.create(label='gen2')
        gen3 = models.Environment.objects.create(label='gen3')
        gen4 = models.Environment.objects.create(label='gen4')
        self.assertIn('| gen1', str(gen1))
        return gen1, gen2, gen3, gen4

    def _create_inheritance(self, gen1, gen2, gen3, gen4):
        "Create inheritance."
        g1_2 = models.Inheritance.objects.create(offspring=gen2, ascendant=gen1)
        g2_3 = models.Inheritance.objects.create(offspring=gen3, ascendant=gen2)
        g3_4 = models.Inheritance.objects.create(offspring=gen4, ascendant=gen3)
        self.assertIn('gen2<gen1', str(g1_2))
        return g1_2, g2_3, g3_4

    def _create_variabels(self, gen1, gen2, gen3, gen4):
        "Create the variables."
        vg1 = gen1.add_variable('gen1k', 'gen1_value')
        vg2 = gen2.add_variable('gen2k', 'gen2_value')
        vg3 = gen3.add_variable('gen3k', 'gen3_value')
        vg4 = gen4.add_variable('gen4k', 'gen4_value')
        self.assertIn('gen1k', str(vg1[0]))
        self.assertIn('gen1 | gen1k | gen1_value', str(vg1[1]))
        return vg1, vg2, vg3, vg4


    def test_001_smoke(self):
        "models.environment"
        environ = models.Environment.objects.create(label='test')
        self.assertTrue(environ.envar is not None)
        data = os.environ.copy()
        _, rsa_key = codec.decode_key(environ.envar)
        encrypted = codec.encrypt(rsa_key, data)
        decrypted = codec.decrypt(rsa_key, encrypted)
        self.assertEqual(data, decrypted)

    def test_002_inheritance(self):
        "Test the inheritance"
        gen1, gen2, gen3, gen4 = self._create_environments()
        self._create_inheritance(gen1, gen2, gen3, gen4)

        expected = [gen4, gen3, gen2, gen1]
        expected = [str(item) for item in expected]
        returned = gen4.resolve_inheritance()
        returned = [str(item) for item in returned]
        self.assertEqual(expected, returned)

        # Add a recursion in it
        models.Inheritance.objects.create(offspring=gen1, ascendant=gen4)
        returned = gen4.resolve_inheritance()
        returned = [str(item) for item in returned]
        self.assertEqual(expected, returned)

    def test_003_variables(self):
        "Test retrieving variables"
        gen1, gen2, gen3, gen4  = self._create_environments()
        self._create_inheritance(gen1, gen2, gen3, gen4)
        self._create_variabels(gen1, gen2, gen3, gen4)
        gen1.add_variable('gen1_override', 'first')
        gen4.add_variable('gen1_override', 'override')

        self.assertEqual(gen4.get_variables()['gen1_override'], 'override')
        self.assertEqual(gen3.get_variables()['gen1_override'], 'first')

    def test_004_fetch_via_request(self):
        "Implement the fetching of the data via the get request."
        gen1, gen2, gen3, gen4  = self._create_environments()
        self._create_inheritance(gen1, gen2, gen3, gen4)
        self._create_variabels(gen1, gen2, gen3, gen4)
        encrypted = self.client.get('/cenvars/%s/' % gen4.ident).content
        rsa_key = codec.decode_key(gen4.envar)[1]
        data = codec.decrypt(rsa_key, encrypted)
        self.assertEqual(gen4.get_variables(), data)

    def test_005_models_save(self):
        "test if we can set the label without regenerating a key."
        gen1 = self._create_environments()[0]
        old = gen1.ident[::]
        gen1.label = 'Generation 1'
        gen1.save()
        self.assertEqual(gen1.ident, old)

    def test_006_command(self):
        "test if the command has output."
        stdout = StringIO()
        call_command('cenvars_newkey', stdout=stdout)
        self.assertTrue(len(stdout.getvalue()) > 0)

    def test_007_codec(self):
        "test the codecs"
        rsa_key = codec.decode_key(settings.CENVARS_KEY)[1]
        data = 'test'
        cypher = codec.encrypt(rsa_key, data)
        plain = codec.decrypt(rsa_key, cypher)
        self.assertEqual(data, plain)

    def test_008_save_load(self):
        "test if the data is persistent saved and restored"
        self._create_environments()
        from ..models import Environment
        environments = Environment.objects.all()
        self.assertTrue(environments.exists())

        from django_memdb.models import PersistentStorage
        query = list(PersistentStorage.objects.all())
        environments.delete()
        self.assertFalse(Environment.objects.all().exists())

        settings.MEMDB_RESTORED = False
        from django_memdb.tools.restore import restore
        restore(query)

        self.assertTrue(Environment.objects.all().exists())
