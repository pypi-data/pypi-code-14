# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from cmsplugin_feed_ai.feed import get_profile_feed


class Command(BaseCommand):
    help = "Test feed fetching"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--profile",
            action="store",
            dest="profile_name",
            default="POTUS",
            help="Profile name to be used. Defaults to POTUS.",
        )

        parser.add_argument(
            "-l",
            "--limit",
            action="store",
            dest="limit",
            default=2,
            help="Limit amount of items fetched from each service.",
        )

    def handle(self, *args, **options):
        profile_name = options["profile_name"]
        limit = int(options["limit"])
        self.output_feeds(profile_name, limit)

    def output_feeds(self, profile_name, limit):
        twitter_feed = get_profile_feed("twitter", profile_name, limit)
        facebook_feed = get_profile_feed("facebook", profile_name, limit)
        print("=== Twitter feed ===")
        print(twitter_feed, "\n")
        print("=== Facebook feed ===")
        print(facebook_feed, "\n")
