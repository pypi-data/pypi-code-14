from __future__ import division

from collections import OrderedDict
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fireworks import Firework

__author__ = 'Anubhav Jain <ajain@lbl.gov>'


# indices for parsing a datetime string in format 2015-09-28T12:00:07.772058
DATE_KEYS = {"years": 4, "months": 7, "days": 10, "hours": 13, "minutes": 16}


class FWReport:
    def __init__(self, lpad):
        """
        Args:
        lpad (LaunchPad)
        """
        self.db = lpad.db

    def get_stats(self, coll="fireworks", interval="days", num_intervals=5, additional_query=None):
        """
        Compile statistics of completed Fireworks/Workflows for past <num_intervals> <interval>,
        e.g. past 5 days.

        Args:
            coll (str): collection, either "fireworks", "workflows", or "launches"
            interval (str): one of "minutes", "hours", "days", "months", "years"
            num_intervals (int): number of intervals to go back in time from present moment
            additional_query (dict): additional constraints on reporting

        Returns:
            list, with each item being a dictionary of statistics for a given interval
        """

        # confirm interval
        if interval not in DATE_KEYS.keys():
            raise ValueError(
                "Specified interval ({}) is not in list of allowed intervals({})".format(
                    interval, DATE_KEYS.keys()))
        # used for querying later
        date_key_idx = DATE_KEYS[interval]

        # initialize collection
        if coll.lower() in ["fws", "fireworks"]:
            coll = "fireworks"
        elif coll.lower() in ["launches"]:
            coll = "launches"
        elif coll.lower() in ["wflows", "workflows"]:
            coll = "workflows"
        else:
            raise ValueError("Unrecognized collection!")

        # whether the collection uses String or Date time dates
        string_type_dates = True if coll in ["fireworks", "launches"] else False
        time_field = "updated_on" if coll in ["fireworks", "workflows"] else "time_end"

        coll = self.db[coll]

        pipeline = []
        match_q = additional_query if additional_query else {}
        if num_intervals:
            now_time = datetime.utcnow()
            start_time = now_time - relativedelta(**{interval:num_intervals})
            date_q = {"$gte": start_time.isoformat()} if string_type_dates else {"$gte": start_time}
            match_q.update({time_field: date_q})

        pipeline.append({"$match": match_q})
        pipeline.append({"$project": {"state": 1, "_id": 0,
                                      "date_key": {"$substr": ["$"+time_field, 0, date_key_idx]}}})
        pipeline.append({"$group": {"_id": {"state:": "$state", "date_key": "$date_key"},
                                    "count": {"$sum": 1}, "state": {"$first": "$state"}}})
        pipeline.append({"$group": {"_id": {"_id.date_key": "$_id.date_key"},
                                    "date_key": {"$first": "$_id.date_key"},
                                    "states": {"$push": {"count": "$count", "state": "$state"}}}})
        pipeline.append({"$sort": {"date_key": -1}})

        # add in missing states and more fields
        decorated_list = []
        for x in coll.aggregate(pipeline):
            total_count = 0
            fizzled_cnt = 0
            completed_cnt = 0
            new_states = OrderedDict()
            for s in sorted(Firework.STATE_RANKS, key=Firework.STATE_RANKS.__getitem__):
                count = 0
                for i in x['states']:
                    if i['state'] == s:
                        count = i['count']
                    if s == "FIZZLED":
                        fizzled_cnt = count
                    if s == "COMPLETED":
                        completed_cnt = count

                new_states[s] = count
                total_count += count

            completed_score = 0 if completed_cnt == 0 else (completed_cnt/(completed_cnt+fizzled_cnt))
            completed_score = round(completed_score, 3)*100
            decorated_list.append({"date_key": x["date_key"], "states": new_states,
                                   "count": total_count, "completed_score": completed_score})
        return decorated_list

    def get_stats_str(self, decorated_stat_list):
        """
        Convert the list of stats from FWReport.get_stats() to a string representation for viewing.

        Args:
            decorated_stat_list ([dict])

        Returns:
             str
        """
        if not decorated_stat_list:
            return "There are no stats to display for the chosen time period."

        my_str = ""
        for x in decorated_stat_list:
            header_str = 'Stats for time-period {}\n'.format(x['date_key'])
            my_str += header_str
            border_str = "=" * len(header_str) + "\n"
            my_str += border_str

            for i in x['states']:
                my_str += "{} : {}\n".format(i, x['states'][i])
            my_str += "\n"
            my_str += "total : {}\n".format(x['count'])
            my_str += "C/(C+F) : {}\n".format(x['completed_score'])
            my_str += "\n"
        return my_str
