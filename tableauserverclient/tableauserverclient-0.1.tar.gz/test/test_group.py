import unittest
import os
import requests_mock
import tableauserverclient as TSC

TEST_ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

GET_XML = os.path.join(TEST_ASSET_DIR, 'group_get.xml')
POPULATE_USERS = os.path.join(TEST_ASSET_DIR, 'group_populate_users.xml')
ADD_USER = os.path.join(TEST_ASSET_DIR, 'group_add_user.xml')


class GroupTests(unittest.TestCase):
    def setUp(self):
        self.server = TSC.Server('http://test')

        # Fake signin
        self.server._site_id = 'dad65087-b08b-4603-af4e-2887b8aafc67'
        self.server._auth_token = 'j80k54ll2lfMZ0tv97mlPvvSCRyD0DOM'

        self.baseurl = self.server.groups._construct_url()

    def test_get(self):
        with open(GET_XML, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            m.get(self.baseurl, text=response_xml)
            all_groups, pagination_item = self.server.groups.get()

        self.assertEqual(3, pagination_item.total_available)
        self.assertEqual('ef8b19c0-43b6-11e6-af50-63f5805dbe3c', all_groups[0].id)
        self.assertEqual('All Users', all_groups[0].name)
        self.assertEqual('local', all_groups[0].domain_name)

        self.assertEqual('e7833b48-c6f7-47b5-a2a7-36e7dd232758', all_groups[1].id)
        self.assertEqual('Another group', all_groups[1].name)
        self.assertEqual('local', all_groups[1].domain_name)

        self.assertEqual('86a66d40-f289-472a-83d0-927b0f954dc8', all_groups[2].id)
        self.assertEqual('TableauExample', all_groups[2].name)
        self.assertEqual('local', all_groups[2].domain_name)

    def test_get_before_signin(self):
        self.server._auth_token = None
        self.assertRaises(TSC.NotSignedInError, self.server.groups.get)

    def test_populate_users(self):
        with open(POPULATE_USERS, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            m.get(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users', text=response_xml)
            single_group = TSC.GroupItem(name='Test Group')
            single_group._id = 'e7833b48-c6f7-47b5-a2a7-36e7dd232758'
            pagination_item = self.server.groups.populate_users(single_group)

        self.assertEqual(1, pagination_item.total_available)
        user = single_group.users.pop()
        self.assertEqual('dd2239f6-ddf1-4107-981a-4cf94e415794', user.id)
        self.assertEqual('alice', user.name)
        self.assertEqual('Publisher', user.site_role)
        self.assertEqual('2016-08-16T23:17:06Z', user.last_login)

    def test_delete(self):
        with requests_mock.mock() as m:
            m.delete(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758', status_code=204)
            self.server.groups.delete('e7833b48-c6f7-47b5-a2a7-36e7dd232758')

    def test_remove_user(self):
        with open(POPULATE_USERS, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            url = self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users' \
                                 '/dd2239f6-ddf1-4107-981a-4cf94e415794'
            m.delete(url, status_code=204)
            m.get(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users', text=response_xml)
            single_group = TSC.GroupItem('test')
            single_group._id = 'e7833b48-c6f7-47b5-a2a7-36e7dd232758'
            self.server.groups.populate_users(single_group)
            self.assertEqual(1, len(single_group.users))
            self.server.groups.remove_user(single_group, 'dd2239f6-ddf1-4107-981a-4cf94e415794')

        self.assertEqual(0, len(single_group.users))

    def test_add_user(self):
        with open(ADD_USER, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            m.post(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users', text=response_xml)
            single_group = TSC.GroupItem('test')
            single_group._id = 'e7833b48-c6f7-47b5-a2a7-36e7dd232758'
            single_group._users = set()
            self.server.groups.add_user(single_group, '5de011f8-5aa9-4d5b-b991-f462c8dd6bb7')

        self.assertEqual(1, len(single_group.users))
        user = single_group.users.pop()
        self.assertEqual('5de011f8-5aa9-4d5b-b991-f462c8dd6bb7', user.id)
        self.assertEqual('testuser', user.name)
        self.assertEqual('ServerAdministrator', user.site_role)

    def test_add_user_before_populating(self):
        single_group = TSC.GroupItem('test')
        self.assertRaises(TSC.UnpopulatedPropertyError, self.server.groups.add_user, single_group,
                          '5de011f8-5aa9-4d5b-b991-f462c8dd6bb7')

    def test_add_user_missing_user_id(self):
        with open(POPULATE_USERS, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            m.get(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users', text=response_xml)
            single_group = TSC.GroupItem(name='Test Group')
            single_group._id = 'e7833b48-c6f7-47b5-a2a7-36e7dd232758'
            self.server.groups.populate_users(single_group)

        self.assertRaises(ValueError, self.server.groups.add_user, single_group, '')

    def test_add_user_missing_group_id(self):
        single_group = TSC.GroupItem('test')
        single_group._users = []
        self.assertRaises(TSC.MissingRequiredFieldError, self.server.groups.add_user, single_group,
                          '5de011f8-5aa9-4d5b-b991-f462c8dd6bb7')

    def test_remove_user_before_populating(self):
        single_group = TSC.GroupItem('test')
        self.assertRaises(TSC.UnpopulatedPropertyError, self.server.groups.remove_user, single_group,
                          '5de011f8-5aa9-4d5b-b991-f462c8dd6bb7')

    def test_remove_user_missing_user_id(self):
        with open(POPULATE_USERS, 'rb') as f:
            response_xml = f.read().decode('utf-8')
        with requests_mock.mock() as m:
            m.get(self.baseurl + '/e7833b48-c6f7-47b5-a2a7-36e7dd232758/users', text=response_xml)
            single_group = TSC.GroupItem(name='Test Group')
            single_group._id = 'e7833b48-c6f7-47b5-a2a7-36e7dd232758'
            self.server.groups.populate_users(single_group)

        self.assertRaises(ValueError, self.server.groups.remove_user, single_group, '')

    def test_remove_user_missing_group_id(self):
        single_group = TSC.GroupItem('test')
        single_group._users = []
        self.assertRaises(TSC.MissingRequiredFieldError, self.server.groups.remove_user, single_group,
                          '5de011f8-5aa9-4d5b-b991-f462c8dd6bb7')
