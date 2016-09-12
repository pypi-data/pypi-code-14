#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Thomas'

import re
from tgbot.tglogging import logger
from tgbot.tgredis import TGRedis
from tgbot.basicapi.parser.methodparser import parsemethods
import inspect
regex = re.compile(r'/(?P<command>\w+)(\s(?P<parameter>.+))?')

def getcommand(text):
    """
    Holt sich den Befehl aus dem angegebenen Text heraus
    :param text: Der angegebene Text
    :return: Der Commandwert
    """
    m = regex.match(text)
    value = m.group("command")
    value.lower()
    return value

def parseconversation(message,conversationcommand,args):
    parsemethods(message,conversationcommand,args)


def parsecommand(message,args):

    text = message.text
    logger.debug("PARSING COMMAND WITH TEXT:" +text)

    if re.match(r'/(\w)+', message.text):
        command = getcommand(text)
    elif TGRedis.getconvcommand(message):
        logger.debug("COMMAND FROM REDIS: "+TGRedis.getconvcommand(message))
        command = TGRedis.getconvcommand(message)
    else:
        return
    logger.debug("FOUND COMMAND: "+command)
    parsemethods(message,command,args)



