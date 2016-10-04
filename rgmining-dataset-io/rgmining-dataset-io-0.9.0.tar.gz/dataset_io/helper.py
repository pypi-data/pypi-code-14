"""Provide helper functions and classes.
"""
from __future__ import absolute_import
import itertools
import json
import sys
from functools import wraps
from collections import namedtuple

from dataset_io.constants import PRODUCT_ID
from dataset_io.constants import REVIEWER_ID

Reviewer = namedtuple("Reviewer", (REVIEWER_ID, "score"))
"""Named tuple to access reviewer's attributes easily.
"""

Product = namedtuple("Product", (PRODUCT_ID, "summary"))
"""Named tuple to access product's attribute easily.
"""


def quiet(f):
    """Decorator ignoring ValueError.

    Args:
      f: A function

    Returns:
      A decorated function which ignores ValueError and returns None
      when such exceptions happen.
    """
    @wraps(f)
    def _(*args, **kwargs):
        """Decorated function returns None when ValueError occurs.
        """
        try:
            return f(*args, **kwargs)
        except ValueError:
            return None
    return _


def convert_date(date):
    """Convert data-type data to int.

    For example, date `2016-01-02` is converted to integer `20160102`.

    Args:
      data: data to convert

    Returns:
      Int-type date data.
    """
    return int(str(date).replace("-", ""))


def normalize_rating(v):
    """Normalize five star ratings between 0 to 1.

    Args:
      v: rating which is between 1 to 5

    Returns:
      Normalized rating data between 0 to 1
    """
    return (v - 1.) / 4.


def print_state(g, i, output=sys.stdout):
    """Print a current state of a given graph.

    This method outputs a current of a graph as a set of json objects.
    Graph objects must have two properties; `reviewers` and `products`.
    Those properties returns a set of reviewers and products respectively.

    In this output format, each line represents a reviewer or product object.

    Reviewer objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "reviewer_id": <Reviewer's ID>
              "score": <Anomalous score of the reviewer>
           }
        }

    Product objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "product_id": <Product's ID>
              "sumarry": <Summary of the reviews for the product>
           }
        }

    Args:
      g: Graph instance.
      i: Iteration number.
      output: A writable object (default: sys.stdout).
    """
    for r in g.reviewers:
        json.dump({
            "iteration": i,
            "reviewer": {
                REVIEWER_ID: r.name,
                "score": r.anomalous_score
            }
        }, output)
        output.write("\n")

    for p in g.products:
        json.dump({
            "iteration": i,
            "product": {
                PRODUCT_ID: p.name,
                "summary": float(str(p.summary)) * 4. + 1
            }
        }, output)
        output.write("\n")


def parse_state(fp, reviewer_handler=None, product_handler=None, iteration="final"):
    """Parse a state of a graph from an iterable.

    Parse a state outputted from print_state and call callback functions.
    The callback for reviewer must receive two arguments;
    *iteration* and *review object*.
    The review object has two attributes; *reviewer_id* and *score*.
    The callback for product must Recife's two arguments;
    *iteration* and *product object*.
    The product object has two attributes; *product_id* and *summary*.
    See print_state for more detail.

    If the callback is set None, associated objects are not parsed.

    Args:
      fp: An iterable object containing state data.
      reviewer_handler: A callback for reviewer (default: None).
      product_handler: A callback for product (default: None).
      iteration: Choose iteration to be parsed (default: 'final').
    """
    for item in itertools.ifilter(bool, itertools.imap(quiet(json.loads), fp)):
        if not isinstance(item, dict) or not "iteration" in item:
            continue

        if str(item["iteration"]) == str(iteration):
            if reviewer_handler and "reviewer" in item:
                reviewer_handler(iteration, Reviewer(**item["reviewer"]))

            elif product_handler and "product" in item:
                p = item["product"]
                product_handler(iteration, Product(
                    p["product_id"], normalize_rating(p["summary"])))
