# coding=utf-8

import unittest

from tcell_agent.appsensor import params

class ParamsTest(unittest.TestCase):

    def one_flatten_params_test(self):
        result = params.flatten_clean({
            "action": "index"
        })

        self.assertEqual(
            result,
            {("action",): "index"}
        )

    def two_flatten_params_test(self):
        result = params.flatten_clean({
            u"müller": "sadness"
        })

        self.assertEqual(
            result,
            {(u"müller",): "sadness"}
        )

    def three_flatten_params_test(self):
        result = params.flatten_clean({
            u"müller".encode("utf-8"): "sadnessdos"
        })

        self.assertEqual(
            result,
            {(b'm\xc3\xbcller',): "sadnessdos"}
        )

    def four_flatten_params_test(self):
        result = params.flatten_clean({
            "utf8-char": u"Müller",
        })

        self.assertEqual(
            result,
            {("utf8-char",): u"Müller"}
        )

    def five_flatten_params_test(self):
        result = params.flatten_clean({
            "waitlist_entries": {"email": "emailone", "preferences": {"email": "emaildos"}}
        })

        self.assertEqual(
            result,
            {
                ("waitlist_entries", "email",): "emailone",
                ("waitlist_entries", "preferences", "email",): "emaildos"
            }
        )

    def six_flatten_params_test(self):
        result = params.flatten_clean({
            "email_preferences": ["daily_digest", "reminders", u"Müller".encode('utf8')],
        })

        self.assertEqual(
            result,
            {
                ('0', "email_preferences",): "daily_digest",
                ('1', "email_preferences",): "reminders",
                ('2', 'email_preferences'): u'M\xfcller',
            }
        )

    def seven_flatten_params_test(self):
        result = params.flatten_clean({
            "users": [
                {"email": "one@email.com"},
                {"email": "dos@email.com"},
            ]
        })

        self.assertEqual(
            result,
            {
                ('0', "users", "email",): "one@email.com",
                ('1', "users", "email",): "dos@email.com"
            }
        )
