#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

from bs4 import BeautifulSoup as Soup

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.base import File as DjangoFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.test.client import Client

from ishtar_common import models

"""
from django.conf import settings
import tempfile, datetime
from zipfile import ZipFile, ZIP_DEFLATED

from oook_replace.oook_replace import oook_replace

class OOOGenerationTest(TestCase):
    def testGeneration(self):
        context = {'test_var':u"Testé", 'test_var2':u"",
                   "test_date":datetime.date(2015, 1, 1)}
        tmp = tempfile.TemporaryFile()
        oook_replace("../ishtar_common/tests/test-file.odt", tmp, context)
        inzip = ZipFile(tmp, 'r', ZIP_DEFLATED)
        value = inzip.read('content.xml')
        self.assertTrue(u"Testé" in value or "Test&#233;" in value)
        self.assertTrue("testé 2" not in value and "test&#233; 2" not in value)
        self.assertTrue("2015" in value)
        lg, ct = settings.LANGUAGE_CODE.split('-')
        if lg == 'fr':
            self.assertTrue('janvier' in value)
        if lg == 'en':
            self.assertTrue('january' in value)
"""


def create_superuser():
    username = 'username4277'
    password = 'dcbqj756456!@%'
    user = User.objects.create_superuser(username, "nomail@nomail.com",
                                         password)
    return username, password, user


def create_user():
    username = 'username678'
    password = 'dcbqj756456!@%'
    user = User.objects.create_user(username, email="nomail2@nomail.com")
    user.set_password(password)
    user.save()
    return username, password, user


class WizardTest(object):
    url_name = None
    wizard_name = ''
    steps = None
    condition_dict = None
    form_datas = []

    def setUp(self):
        self.username, self.password, self.user = create_superuser()

    def pre_wizard(self):
        self.client.login(**{'username': self.username,
                             'password': self.password})

    def post_wizard(self):
        pass

    def test_wizard(self):
        url = reverse(self.url_name)
        self.pre_wizard()
        for form_data, ignored in self.form_datas:
            for idx, step in enumerate(self.steps):
                current_step, current_form = step
                if current_step in ignored:
                    continue
                data = {
                    '{}{}-current_step'.format(self.url_name,
                                               self.wizard_name):
                    [current_step],
                }
                if current_step in form_data:
                    d = form_data[current_step]
                    for k in d:
                        data['{}-{}'.format(current_step, k)] = d[k]

                next_idx, next_form = idx + 1, None
                while len(self.steps) > next_idx:
                    if self.steps[idx + 1][0] not in ignored:
                        next_form = self.steps[idx + 1][0]
                        break
                    next_idx = next_idx + 1

                if next_form:
                    try:
                        response = self.client.post(url, data)
                    except ValidationError as e:
                        raise ValidationError(u"Errors: {} on {}.".format(
                            u" - ".join(e.messages), current_step))
                    if "errorlist" in response.content:
                        soup = Soup(response.content)
                        errorlist = soup.findAll(
                            "ul", {"class": "errorlist"})
                        errors = []
                        for li in errorlist:
                            lbl = li.findParent().findParent().findChild().text
                            errors.append(u"{} - {}".format(lbl, li.text))
                        raise ValidationError(u"Errors: {} on {}.".format(
                            u" ".join(errors), current_step))
                    self.assertRedirects(
                        response,
                        '/{}/{}'.format(self.url_name, next_form))
                else:
                    response = self.client.post(url, data, follow=True)
        self.post_wizard()


class CacheTest(TestCase):
    def testAdd(self):
        models.OrganizationType.refresh_cache()
        cached = models.OrganizationType.get_cache('test')
        self.assertEqual(cached, None)
        orga = models.OrganizationType.objects.create(
            txt_idx='test', label='testy')
        cached = models.OrganizationType.get_cache('test')
        self.assertEqual(cached.pk, orga.pk)
        orga.txt_idx = 'testy'
        orga.save()
        cached = models.OrganizationType.get_cache('testy')
        self.assertEqual(cached.pk, orga.pk)

    def testList(self):
        models.OrganizationType.refresh_cache()
        types = models.OrganizationType.get_types()
        # only empty
        self.assertTrue(len(types), 1)
        org = models.OrganizationType.objects.create(
            txt_idx='test', label='testy')
        types = [
            unicode(lbl) for idx, lbl in models.OrganizationType.get_types()]
        self.assertTrue('testy' in types)
        org.delete()
        types = [
            unicode(lbl) for idx, lbl in models.OrganizationType.get_types()]
        self.assertFalse('testy' in types)


class MergeTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='username')
        self.organisation_types = \
            models.OrganizationType.create_default_for_test()

        self.person_types = [models.PersonType.objects.create(label='Admin'),
                             models.PersonType.objects.create(label='User')]
        self.author_types = [models.AuthorType.objects.create(label='1'),
                             models.AuthorType.objects.create(label='2')]

        self.company_1 = models.Organization.objects.create(
            history_modifier=self.user, name='Franquin Comp.',
            organization_type=self.organisation_types[0])
        self.person_1 = models.Person.objects.create(
            name='Boule', surname=' ', history_modifier=self.user,
            attached_to=self.company_1)
        self.person_1.person_types.add(self.person_types[0])
        self.author_1_pk = models.Author.objects.create(
            person=self.person_1, author_type=self.author_types[0]).pk

        self.title = models.TitleType.objects.create(label='Test')

        self.company_2 = models.Organization.objects.create(
            history_modifier=self.user, name='Goscinny Corp.',
            organization_type=self.organisation_types[1])
        self.person_2 = models.Person.objects.create(
            name='Bill', history_modifier=self.user, surname='Peyo',
            title=self.title, attached_to=self.company_2)
        self.person_2.person_types.add(self.person_types[1])
        self.author_2_pk = models.Author.objects.create(
            person=self.person_2, author_type=self.author_types[1]).pk
        self.person_3 = models.Person.objects.create(
            name='George', history_modifier=self.user,
            attached_to=self.company_1)

    def testPersonMerge(self):
        self.person_1.merge(self.person_2)
        # preserve existing fields
        self.assertEqual(self.person_1.name, 'Boule')
        # fill missing fields
        self.assertEqual(self.person_1.title, self.title)
        # string field with only spaces is an empty field
        self.assertEqual(self.person_1.surname, 'Peyo')
        # preserve existing foreign key
        self.assertEqual(self.person_1.attached_to, self.company_1)
        # preserve existing many to many
        self.assertTrue(self.person_types[0]
                        in self.person_1.person_types.all())
        # add new many to many
        self.assertTrue(self.person_types[1]
                        in self.person_1.person_types.all())
        # update reverse foreign key association and dont break the existing
        self.assertEqual(models.Author.objects.get(pk=self.author_1_pk).person,
                         self.person_1)
        self.assertEqual(models.Author.objects.get(pk=self.author_2_pk).person,
                         self.person_1)

        self.person_3.merge(self.person_1)
        # manage well empty many to many fields
        self.assertTrue(self.person_types[1]
                        in self.person_3.person_types.all())

    def testPersonMergeCandidate(self):
        init_mc = self.person_1.merge_candidate.count()
        person = models.Person.objects.create(
            name=self.person_1.name,
            surname=self.person_1.surname, history_modifier=self.user,
            attached_to=self.person_1.attached_to)
        self.assertEqual(self.person_1.merge_candidate.count(),
                         init_mc + 1)
        person.archive()
        self.assertEqual(self.person_1.merge_candidate.count(),
                         init_mc)


class ImportTest(TestCase):
    def testDeleteRelated(self):
        town = models.Town.objects.create(name='my-test')
        self.assertEqual(models.Town.objects.filter(name='my-test').count(), 1)

        # create an import, fields are not relevant...
        create_user()
        importer_type = models.ImporterType.objects.create(
            associated_models='ishtar_common.models.Person')
        mcc_operation_file = DjangoFile(file(
            settings.ROOT_PATH +
            '../archaeological_operations/tests/MCC-operations-example.csv',
            'rb'))
        imprt = models.Import.objects.create(
            user=models.IshtarUser.objects.all()[0],
            importer_type=importer_type,
            imported_file=mcc_operation_file)

        town.imports.add(imprt)
        imprt.delete()
        # town should be deleted
        self.assertEqual(models.Town.objects.filter(name='my-test').count(), 0)

    def testKeys(self):
        content_type = ContentType.objects.get_for_model(
            models.OrganizationType)

        # creation
        label = u"Ploufé"
        ot = models.OrganizationType.objects.create(label=label)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot.pk, key=slugify(label),
                         content_type=content_type).count(), 1)
        label_2 = u"Plif"
        ot_2 = models.OrganizationType.objects.create(label=label_2)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_2),
                         content_type=content_type).count(), 1)

        # replace key
        ot_2.add_key(slugify(label), force=True)
        # one key point to only one item
        self.assertEqual(models.ItemKey.objects.filter(
                         key=slugify(label),
                         content_type=content_type).count(), 1)
        # this key point to the right item
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label),
                         content_type=content_type).count(), 1)

        # modification
        label_3 = "Yop"
        ot_2.label = label_3
        ot_2.txt_idx = slugify(label_3)
        ot_2.save()
        # old label not referenced anymore
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_2),
                         content_type=content_type).count(), 0)
        # # forced key association is always here
        # new key is here
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label),
                         content_type=content_type).count(), 1)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_3),
                         content_type=content_type).count(), 1)


class IshtarSiteProfileTest(TestCase):
    def testRelevance(self):
        cache.set('default-ishtarsiteprofile-is-current-profile', None,
                  settings.CACHE_TIMEOUT)
        profile = models.get_current_profile()
        default_slug = profile.slug
        profile2 = models.IshtarSiteProfile.objects.create(
            label="Test profile 2", slug='test-profile-2')
        profile2.save()
        # when no profile is the current, activate by default the first created
        self.assertTrue(profile.active and not profile2.active)
        profile2.active = True
        profile2 = profile2.save()
        # only one profile active at a time
        profile = models.IshtarSiteProfile.objects.get(slug=default_slug)
        self.assertTrue(profile2.active and not profile.active)
        # activate find active automatically context records
        self.assertFalse(profile.context_record)
        profile.find = True
        profile = profile.save()
        self.assertTrue(profile.context_record)
        # activate warehouse active automatically context records and finds
        self.assertFalse(profile2.context_record or profile2.find)
        profile2.warehouse = True
        profile2 = profile2.save()
        self.assertTrue(profile2.context_record and profile2.find)

    def testDefaultProfile(self):
        cache.set('default-ishtar_common-IshtarSiteProfile', None,
                  settings.CACHE_TIMEOUT)
        self.assertFalse(models.IshtarSiteProfile.objects.count())
        profile = models.get_current_profile(force=True)
        self.assertTrue(profile)
        self.assertEqual(models.IshtarSiteProfile.objects.count(), 1)

    def testMenuFiltering(self):
        cache.set('default-ishtarsiteprofile-is-current-profile', None,
                  settings.CACHE_TIMEOUT)
        username = 'username4277'
        password = 'dcbqj756456!@%'
        User.objects.create_superuser(username, "nomail@nomail.com",
                                      password)
        c = Client()
        c.login(username=username, password=password)
        response = c.get(reverse('start'))
        self.assertFalse("section-file_management" in response.content)
        profile = models.get_current_profile()
        profile.files = True
        profile.save()
        response = c.get(reverse('start'))
        self.assertTrue("section-file_management" in response.content)

    def testExternalKey(self):
        profile = models.get_current_profile()
        p = models.Person.objects.create(name='plouf', surname=u'Tégada')
        self.assertEqual(p.raw_name, u"PLOUF Tégada")
        profile.person_raw_name = u'{surname|slug} {name}'
        profile.save()
        p.raw_name = ''
        p.save()
        self.assertEqual(p.raw_name, u"tegada plouf")
