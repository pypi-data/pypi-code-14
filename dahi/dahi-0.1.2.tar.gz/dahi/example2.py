from dahi import CONFIG
from dahi.bot import Bot
from dahi.context import Context
from dahi.knowledgebase import KnowledgeBase
from dahi.statement import Statement
from dahi.storages import Mongo


def getBot(botId, userId):
    print("hello")
    storage = Mongo("mongodb://localhost")
    kb = KnowledgeBase(storage, 3)
    context = Context(userId)
    bot = Bot(knowledgeBase=kb)
    print bot.respond(context, Statement("kredi"))

    print "LOGS:"
    for i in context.logs:
        print i

getBot(1, 2)


class KnowledgeBaseManager():
    def create(id):
        storage = Mongo("mongodb://localhost")
        knowledgeBase_class = import_component("knowledge_base")
        knowledgeBase_class(storage)