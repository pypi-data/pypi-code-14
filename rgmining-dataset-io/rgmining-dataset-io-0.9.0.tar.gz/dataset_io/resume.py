"""Provide a function to resume mining.
"""
from __future__ import absolute_import
from dataset_io.helper import parse_state


def resume(graph, state, iteration="final"):
    """Reconstruct a bipertite graph from original file and outputed state file.

    Args:
      graph: A empty bipertite graph object.
      state: A readable object containing state data outputed by helper.print_state.
      iteration: Loading iteration. (Default: final)

    Returns:
      The graph instance. This is as same as *graph*.
    """
    def reviewer_handler(_, reviewer):
        """Parse reviewers.

        Args:
          reviewer: New reviewer.
        """
        r = graph.find_reviewer(reviewer.reviewer_id)
        if r:
            r.anomalous_score = reviewer.score

    def product_handler(_, product):
        """Parse product.

        Args:
          product: New product.
        """
        p = graph.find_product(product.product_id)
        if p:
            p.summary = product.summary

    parse_state(state, reviewer_handler, product_handler, iteration)
    return graph
