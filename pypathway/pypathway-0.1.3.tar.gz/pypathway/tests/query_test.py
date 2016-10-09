# test the data query and map in kegg pathway
from pypathway import *
import unittest


class KEGGTest(unittest.TestCase):
    def test_search_database(self):
        keyword_list = ["jak", "carbon", "insulin", "g protein", "t cell"]
        for i, x in enumerate(keyword_list):
            PublicDatabase.search_kegg(x)

    def test_draw_pathway(self):
        res = PublicDatabase.search_kegg("insulin")
        for i, x in enumerate(res):
            d = x.load().draw()

    def test_access_entity_and_reaction(self):
        res = PublicDatabase.search_kegg("insulin")
        print(len(res))
        for x in res:
            p = x.load()
            for x in p.entitys:
                id = x.id
            for x in p.genes:
                id = x.id
            for x in p.reactions:
                x.summary()

    def test_draw_all_human_pathway(self):
        pass



class WikiTest(unittest.TestCase):
    def test_search_wikipathway(self):
        keyword_list = ["jak", "carbon", "insulin", "g protein", "t cell"]
        for i, x in enumerate(keyword_list):
            PublicDatabase.search_wp(x)


class ReactomeTest(unittest.TestCase):
    pass


class CommandLineExecuteOfPaxtools(unittest.TestCase):
    pass


class VisualizeTest(unittest.TestCase):
    pass


def loc():
    import os
    return os.path.dirname(os.path.realpath(__file__)) + "/query_test.py"

if __name__ == '__main__':
    unittest.main()
