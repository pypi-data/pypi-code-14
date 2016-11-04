import km3pipe as kp
import numpy as np
import pandas as pd     # noqa
from km3pipe.dataclasses import HitSeries


class FirstHits(kp.Module):
    def process(self, blob):
        hits = blob['Hits'].serialise(to='pandas')
        # hackish. Pandas only keeps 1st unique row of each
        # and since the hits are sorted, this works
        first_hits = hits.drop_duplicates(subset='dom_id')
        blob['FirstHits'] = HitSeries.from_table(first_hits)
        return blob
