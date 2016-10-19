#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from flask_tat.base import BaseTATClient


class HTTP2KafkaClient(BaseTATClient):
    def message_add(self, topic, **kwargs):
        return self.client.do_request(
            method="POST", path="/message/%s" % topic.lstrip('/'), data=kwargs
        )

    def message_reply(self, topic, tag_ref, text):
        return self.client.do_request(
            method="POST", path="/message/{}".format(topic.lstrip('/')),
            data={"text": text, "tagReference": tag_ref, "action": "reply"}
        )

    def message_relabel(self, topic, tag_ref, labels):
        return self.client.do_request(
            method="PUT", path="/message/{}".format(topic.lstrip('/')),
            data={
                "labels": labels, "tagReference": tag_ref, "action": "relabel"
            }
        )
