"""Load review data formatted in JSON to a graph object.
"""
from __future__ import absolute_import
import json
from itertools import imap, ifilter
from dataset_io.helper import convert_date
from dataset_io.helper import normalize_rating
from dataset_io.helper import quiet
from dataset_io.constants import PRODUCT_ID
from dataset_io.constants import MEMBER_ID


def load(g, fp, anomalous=None):
    """Load a review dataset to a given graph object.

    The graph object must have the following methods;

    new_reviewer(name, anomalous)
        create and register a new reviewer which has a given `name` and
        be initialized by a given `anomalous` score,
    new_product(name)
        create and register a new product which has a given `name`,
    find_reviewer(name)
        find and return a reviewer which has given `name`,
    find_product(name)
        find and return a product which has given `name`,
    add_review(self, reviewer, product, review, date)
        add a new review from `reviewer` to `product` issued in `date`,
        in which the review is a float value.

    `fp` is an iterative object which yields a JSON string representing a review.
    Each review must have the following elements::

        {
            "member_id": "A1AF30H2MPOO9",
            "product_id": "0001056530",
            "rating": 4.0,
            "date": "2000-08-21"
        }

    where `member_id` is a reviewer's id, i.e. name, `product_id` is a product's
    id which the reviewer posts a review. Rating is a five-star score for the
    product. Date is the date the review issued.

    Args:
      g: graph object where loaded review data are stored.
      fp: readable object containing JSON data of a loading table.
      anomalous: default anomalous scores (Default: None).

    Returns:
      The graph instance, which is as same as *g*.
    """
    reviewers = {}
    products = {}
    for review in ifilter(bool, imap(quiet(json.loads), fp)):

        member_id = review[MEMBER_ID]
        product_id = review[PRODUCT_ID]
        rating = normalize_rating(review["rating"])
        date = convert_date(review["date"])

        if member_id in reviewers:
            r = reviewers[member_id]
        else:
            r = g.new_reviewer(name=member_id, anomalous=anomalous)
            reviewers[member_id] = r

        if product_id in products:
            p = products[product_id]
        else:
            p = g.new_product(name=product_id.strip())
            products[product_id] = p

        g.add_review(r, p, rating, date)

    return g
