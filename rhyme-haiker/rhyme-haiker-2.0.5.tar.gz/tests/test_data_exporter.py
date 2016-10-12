# -*- coding: utf-8 -*-

from poetry.utils.data_exporter import DataExporter
import unittest


class TestDataExporter(unittest.TestCase):

    # def test_dumps_tuple(self):
    #     chains = {
    #         ("古池", "あ", "古池"): [
    #             "い"
    #         ],
    #         ("あ", "古池", "い"): [
    #             "古池"
    #         ],
    #         ("古池", "い", "古池"): [
    #             "う"
    #         ],
    #         ("い", "古池", "う"): [
    #             "蛙"
    #         ],
    #         ("古池", "う", "蛙"): [
    #             "あ"
    #         ],
    #         ("う", "蛙", "あ"): [
    #             "蛙"
    #         ],
    #         ("蛙", "あ", "蛙"): [
    #             "い"
    #         ],
    #         ("あ", "蛙", "い"): [
    #             None
    #         ]
    #     }

    #     de = DataExporter(chains_data=chains, words_data="")
    #     print("dumped: ", de.chains_data)
    #     self.assertEqual(
    #         de._dumps_tuple(chains),
    #         {"('あ', '古池', 'い')": ['古池'], "('あ', '蛙', 'い')": [None], "('い', '古池', 'う')": ['蛙'], "('古池', 'あ', '古池')": ['い'], "('古池', 'う', '蛙')": ['あ'], "('古池', 'い', '古池')": ['う'], "('蛙', 'あ', '蛙')": ['い'], "('う', '蛙', 'あ')": ['蛙']}
    #     )
    pass

if __name__ == '__main__':
    unittest.main()
