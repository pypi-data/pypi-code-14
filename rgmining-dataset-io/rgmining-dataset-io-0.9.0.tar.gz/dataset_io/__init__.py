"""Define dataset file format and load/output methods.

This package provides a set of methods to load review datasets and output
mining results in JSON format.

Review data
=============
Review data are a set of tuples.
Each tuple consists of a *reviewer's ID*, a *review target product ID*,
*five-start rating score*, and *reviewing date*.
In the JSON format, keys of them are *member_id*, *product_id*, *rating*,
and *date*, respectively.
A review tuple looks like::

    {
        "member_id": "A1AF30H2MPOO9",
        "product_id": "0001056530",
        "rating": 4.0,
        "date": "2000-08-21"
    }

Review data file must consist of such JSON object and each line has only one
object.

:meth:`dataset_io.loader.load` or its alias :meth:`dataset_io.load` parse a JSON
file and add those review data to a graph.


Mining results
===============
Mining results are described as a set of state information.
Since we assume mining algorithms employ repeated improvement principle,
every iteration outputs a new state.

In the output format, each line represents a reviewer or a product object.
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
          "summary": <Summary of the reviews for the product>
       }
    }

:meth:`dataset_io.heler.print_state` or its alias :meth:`dataset_io.print_state`
output a state of a graph.

Outputted state information can be used to restore some state by
:meth:`dataset_io.resume.resume` or its alias :meth:`dataset_io.resume`.
This function takes state data and construct a graph which has same state.


Graph interface
=================
This package assumes graph, reviewer, and product objects are following
certain APIs.


Graph object
--------------
Graph object maintains relationship between reviewers and products.
Most of algorithms treat it by a bipartite graph but any modeling is allowed.

Any graph object needs to supply some methods and properties.
The required methods are the followings;

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

The required properties are the followings;

reviewers (readable)
    a set of reviewers,
products (readable)
    a set of products.


Reviewer object
----------------
A reviewer object represents a reviewer who has a name and anomalous score.
The reviewer object is required to have two properties;

name (readable)
    a name of the reviewer,
anomalous_score (readable)
    a float value of the reviewer's anomalous score.


Product object
----------------
A product object represents a product which has a name and summarized reviews,
called `summary`. The product object is required to have two properties;

name (readable)
    a name of the product,
summary (readable)
    a float value of the summarized reviews.


Aliases
==========
The top level module provides the following aliases;

:meth:`dataset_io.load`
    arias of :meth:`dataset_io.loader.load`,
:meth:`dataset_io.print_state`
    arias of :meth:`dataset_io.helper.print_state`,
:meth:`dataset_io.parse_state`
    arias of :meth:`dataset_io.helper.parse_state`,
:meth:`dataset_io.quiet`
    arias of :meth:`dataset_io.helper.quiet`,
:meth:`dataset_io.normalize_rating`
    arias of :meth:`dataset_io.helper.normalize_rating`,
:meth:`dataset_io.resume`
    arias of :meth:`dataset_io.resume.resume`,
:class:`dataset_io.UniformSampler`
    arias of :class:`dataset_io.sampler.UniformSampler`,
:class:`dataset_io.RatingBasedSampler`
    arias of :class:`dataset_io.sampler.RatingBasedSampler`.
"""
from __future__ import absolute_import
from dataset_io.loader import load
from dataset_io.helper import print_state
from dataset_io.helper import parse_state
from dataset_io.helper import quiet
from dataset_io.helper import normalize_rating
from dataset_io.resume import resume
from dataset_io.sampler import UniformSampler
from dataset_io.sampler import RatingBasedSampler

from dataset_io.constants import REVIEWER_ID
from dataset_io.constants import PRODUCT_ID
from dataset_io.constants import MEMBER_ID
