from mock import Mock
import unittest2
from applause.beta import ApplauseBETA
from applause import settings


# Test only distribution since only one method is overriden
class ApplauseBetaTest(unittest2.TestCase):
    TEST_INSTALLER_ID = 333
    TEST_APPLICATION_ID = 22

    def setUp(self):
        self.session_mock = Mock()
        self.beta = ApplauseBETA(self.session_mock)
        self.distribution_url = settings.MBM_BASE_URL + "applications/%s/distributions/" % self.TEST_APPLICATION_ID

    def test_distribution_success(self):
        # self.beta.upload_to_buaps = Mock()
        self.beta.upload = Mock(return_value=self.TEST_INSTALLER_ID)

        self.beta.distribute(self.TEST_APPLICATION_ID, "/tmp/example.ipa",
                             groups=["group1", "group2"],
                             emails=["test1@example.com", "test2@example.com"],
                             changelog="The change log",
                             sent_from="sender@email.com")

        self.session_mock.post.assert_called_once_with(
            self.distribution_url,
            json={
                "installer": self.TEST_INSTALLER_ID,
                "individuals": ["test1@example.com", "test2@example.com"],
                "group_names": ["group1", "group2"],
                "locale": 'en',
                "sent_from": "sender@email.com",
            },
        )

    def test_distribution_success_without_sender_address(self):
        self.beta.upload = Mock(return_value=self.TEST_INSTALLER_ID)

        self.beta.distribute(self.TEST_APPLICATION_ID, "/tmp/example.ipa",
                             emails=["test1@example.com", "test2@example.com"])

        self.session_mock.post.assert_called_once_with(
            self.distribution_url,
            json={
                "installer": self.TEST_INSTALLER_ID,
                "individuals": ["test1@example.com", "test2@example.com"],
                'group_names': None,
                "locale": 'en',
            },
        )

    def test_validate_fail(self):
        with self.assertRaises(Exception):
            ApplauseBETA.validate(None, None)

    @staticmethod
    def test_validate_success_groups():
        ApplauseBETA.validate(["groups"], None)

    @staticmethod
    def test_validate_success_emails():
        ApplauseBETA.validate(None, ["emails"])
