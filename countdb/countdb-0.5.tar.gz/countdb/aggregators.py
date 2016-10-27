#!/usr/bin/env python
from __future__ import division

from datetime import (datetime, timedelta)
from os.path import (join, sep, basename, exists)
from os import (walk, remove)
from shutil import copy

from countdb import (CountDB, aggregate, makedirs)


def get_current_datetime():
    return datetime.now()


def calc_path_depth(path):
    return len(path.split(sep))


class TimeAggregator(object):
    def __init__(self,
                 stage_dir="/tmp/netconns/__stage__/",
                 final_dir="/tmp/netconns/final/"):
        self.stage_dir = stage_dir
        self.final_dir = final_dir
        self.count_now_filename_format = "%Y-%m-%d/%Y-%m-%d--%H/%Y-%m-%d--%H-%M/%Y-%m-%d--%H-%M-%S"
        self.delta_thresholds = {
            0: timedelta(days=2),
            1: timedelta(hours=24)
        }

        self.stage_dir_depth = calc_path_depth(self.stage_dir)
        makedirs(self.final_dir)

    def create_counter_filename(self, when=None):
        when = when if when else get_current_datetime()
        return join(self.stage_dir, when.strftime(self.count_now_filename_format))

    def create_counter_now(self):
        return CountDB.open_for_counting(self.create_counter_filename())

    def copy_to_final(self, source):
        target = join(self.final_dir, basename(source))
        if not exists(target):
            copy(source, target)

    def finalize(self, path):
        # print("aggregating %s" % path)
        aggregate(path)
        depth = calc_path_depth(path) - self.stage_dir_depth
        if depth in self.delta_thresholds:
            # print("    copy to final")
            self.copy_to_final(path)

    def aggregate(self):
        now = get_current_datetime()
        current_filename = self.create_counter_filename(now)
        # print("  current: %s" % current_filename)
        for dirpath, dirnames, filenames in walk(self.stage_dir, topdown=False):
            for dirname in dirnames:
                full_path = join(dirpath, dirname)
                if not current_filename.startswith(full_path):
                    self.finalize(full_path)

        for dirpath, dirnames, filenames in walk(self.final_dir):
            for filename in filenames:
                full_path = join(dirpath, filename)
                # print("checking %s" % full_path)

                filename_datetime = None
                for depth, date_format in enumerate(self.count_now_filename_format.split(sep)):
                    try:
                        filename_datetime = datetime.strptime(filename, date_format)
                        break
                    except ValueError:
                        pass
                if not filename_datetime:
                    print("WARN: invalid filename encountered: %s" % filename)
                    break
                # print("    depth %i" % depth)
                delta = now - filename_datetime
                # print("    delta %s" % delta)

                if delta > self.delta_thresholds.get(depth, 0):
                    # print("        too old, removing")
                    remove(full_path)


if __name__ == "__main__":
    ta = TimeAggregator()

    orig_get_current_datetime = get_current_datetime
    for delta in (timedelta(days=1, hours=4),
                  timedelta(days=1, hours=3),
                  timedelta(days=1, hours=3, minutes=2),
                  timedelta(hours=2),
                  timedelta(hours=2, minutes=2),
                  timedelta(minutes=2)):
        def patched_current():
            return datetime.now() - delta
        get_current_datetime = patched_current
        with ta.create_counter_now() as counter:
            counter.count("foo bar 1")
            counter.count("bar braz 2")
            counter.count("bar braz 2")
    get_current_datetime = orig_get_current_datetime

    ta.aggregate()
