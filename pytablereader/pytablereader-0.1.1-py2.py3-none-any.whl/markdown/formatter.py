# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ..html.formatter import HtmlTableFormatter


class MarkdownTableFormatter(HtmlTableFormatter):

    def __init__(self, source_data):
        import markdown2

        super(MarkdownTableFormatter, self).__init__(
            markdown2.markdown(source_data, extras=["tables"]))
