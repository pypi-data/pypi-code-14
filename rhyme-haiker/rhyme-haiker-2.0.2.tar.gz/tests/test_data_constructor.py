# -*- coding: utf-8 -*-

from poetry.data_constructor.data_constructor import DataConstructor
import unittest


class TestDataConstructor(unittest.TestCase):

    # def test_construct_parsed_data(self):
    #     dc = DataConstructor()

    #     read_data = "気象庁"
    #     self.assertEqual(
    #         dc._construct_parsed_data(read_data),
    #         [
    #             {
    #                 "word": "気象庁",
    #                 "part": "名詞",
    #                 "vowel": "イオーオー",
    #                 "length": 5
    #             },
    #         ]
    #     )

    #     read_data = "雨が降る"
    #     self.assertEqual(
    #         dc._construct_parsed_data(read_data),
    #         [
    #             {
    #                 "word": "雨",
    #                 "part": "名詞",
    #                 "vowel": "アエ",
    #                 "length": 2
    #             },
    #             {
    #                 "word": "が",
    #                 "part": "助詞",
    #                 "vowel": "ア",
    #                 "length": 1
    #             },
    #             {
    #                 "word": "降る",
    #                 "part": "動詞",
    #                 "vowel": "ウウ",
    #                 "length": 2
    #             },
    #         ]
    #     )

    def test_delimit(self):
        parsed_text = "あいうえお，さしすせそ"
        dc = DataConstructor()
        self.assertEqual(
            dc._delimit(parsed_text),
            [
                'あいうえお，さしすせそ'
            ]
        )

        parsed_text = "あいうえお\nかきくけこ"
        dc = DataConstructor()
        self.assertEqual(
            dc._delimit(parsed_text),
            [
                'あいうえお',
                'かきくけこ'
            ]
        )

    def test_start_new_line(self):
        text = "あいうえお，さしすせそ"
        dc = DataConstructor()
        self.assertEqual(
            dc._start_new_line(text),
            ['あいうえお', 'さしすせそ']
        )

        text = "あい，うえお．かき，くけこ．さし、すせそ。たち，つてと。"
        dc = DataConstructor()
        self.assertEqual(
            dc._start_new_line(text),
            ['あい', 'うえお', 'かき', 'くけこ', 'さし', 'すせそ', 'たち', 'つてと']
        )

    def test_parse_list(self):
        text_list = ['あいうえお',
                     'さしすせそ']
        dc = DataConstructor()
        self.assertEqual(
            dc._parse_list(text_list),
            [['あい\t動詞,自立,*,*,五段・カ行イ音便,連用タ接続,あく,アイ,アイ',
              'う\t助動詞,*,*,*,不変化型,基本形,う,ウ,ウ',
              'え\tフィラー,*,*,*,*,*,え,エ,エ',
              'お\t感動詞,*,*,*,*,*,お,オ,オ'],
             ['さ\t副詞,助詞類接続,*,*,*,*,さ,サ,サ',
              'しす\t動詞,自立,*,*,五段・サ行,基本形,しす,シス,シス',
              'せ\t動詞,接尾,*,*,一段,連用形,せる,セ,セ',
              'そ\t名詞,接尾,助動詞語幹,*,*,*,そ,ソ,ソ']]
        )

        text_list = ['あ', 'いう', 'えお',
                     'か', 'きく', 'けこ',
                     'さ', 'しす', 'せそ']
        dc = DataConstructor()
        self.assertEqual(
            dc._parse_list(text_list),
            [['あ\tフィラー,*,*,*,*,*,あ,ア,ア'],
             ['いう\t動詞,自立,*,*,五段・ワ行促音便,基本形,いう,イウ,イウ'],
             ['え\tフィラー,*,*,*,*,*,え,エ,エ',
              'お\t感動詞,*,*,*,*,*,お,オ,オ'],
             ['か\t助詞,副助詞／並立助詞／終助詞,*,*,*,*,か,カ,カ'],
             ['きく\t動詞,自立,*,*,五段・カ行イ音便,基本形,きく,キク,キク'],
             ['け\t助詞,終助詞,*,*,*,*,け,ケ,ケ',
              'こ\t名詞,一般,*,*,*,*,こ,コ,コ'],
             ['さ\t助詞,終助詞,*,*,*,*,さ,サ,サ'],
             ['しす\t動詞,自立,*,*,五段・サ行,基本形,しす,シス,シス'],
             ['せ\t動詞,自立,*,*,サ変・スル,未然ヌ接続,する,セ,セ',
              'そ\t名詞,特殊,助動詞語幹,*,*,*,そ,ソ,ソ']]
        )

    def test_splited_word_data_to_csv_list(self):
        dc = DataConstructor()
        # parsed_data = "気象庁\t名詞,固有名詞,組織,*,*,*,気象庁,キショウチョウ,キショーチョー"
        parsed_words = [['あ\tフィラー,*,*,*,*,*,あ,ア,ア',
                         'いう\t動詞,自立,*,*,五段・ワ行促音便,基本形,いう,イウ,イウ',
                         'え\tフィラー,*,*,*,*,*,え,エ,エ',
                         'お\t感動詞,*,*,*,*,*,お,オ,オ'],
                        ['か\t助詞,副助詞／並立助詞／終助詞,*,*,*,*,か,カ,カ',
                         'きく\t動詞,自立,*,*,五段・カ行イ音便,基本形,きく,キク,キク',
                         'け\t助詞,終助詞,*,*,*,*,け,ケ,ケ',
                         'こ\t名詞,一般,*,*,*,*,こ,コ,コ'],
                        ['さ\t助詞,終助詞,*,*,*,*,さ,サ,サ',
                         'しす\t動詞,自立,*,*,五段・サ行,基本形,しす,シス,シス',
                         'せ\t動詞,自立,*,*,サ変・スル,未然ヌ接続,する,セ,セ',
                         'そ\t名詞,特殊,助動詞語幹,*,*,*,そ,ソ,ソ']]
        self.assertEqual(
            dc._splited_word_data_to_csv_list(parsed_words),
            [[['あ', 'フィラー', '*', '*', '*', '*', '*', 'あ', 'ア', 'ア'],
              ['いう', '動詞', '自立', '*', '*', '五段・ワ行促音便', '基本形', 'いう', 'イウ', 'イウ'],
              ['え', 'フィラー', '*', '*', '*', '*', '*', 'え', 'エ', 'エ'],
              ['お', '感動詞', '*', '*', '*', '*', '*', 'お', 'オ', 'オ']],
             [['か', '助詞', '副助詞／並立助詞／終助詞', '*', '*', '*', '*', 'か', 'カ', 'カ'],
              ['きく', '動詞', '自立', '*', '*', '五段・カ行イ音便', '基本形', 'きく', 'キク', 'キク'],
              ['け', '助詞', '終助詞', '*', '*', '*', '*', 'け', 'ケ', 'ケ'],
              ['こ', '名詞', '一般', '*', '*', '*', '*', 'こ', 'コ', 'コ']],
             [['さ', '助詞', '終助詞', '*', '*', '*', '*', 'さ', 'サ', 'サ'],
              ['しす', '動詞', '自立', '*', '*', '五段・サ行', '基本形', 'しす', 'シス', 'シス'],
              ['せ', '動詞', '自立', '*', '*', 'サ変・スル', '未然ヌ接続', 'する', 'セ', 'セ'],
              ['そ', '名詞', '特殊', '助動詞語幹', '*', '*', '*', 'そ', 'ソ', 'ソ']]]
            # [
            #     "気象庁", "名詞", "固有名詞", "組織", "*",
            #     "*", "*", "気象庁", "キショウチョウ", "キショーチョー"
            # ]
        )

        parsed_data = ""
        self.assertEqual(
            dc._splited_word_data_to_csv_list(parsed_data),
            []
        )

    def test_sanitize_data_list(self):
        csv_list = [
            [['いう', '動詞', '自立', '*', '*', '五段・ワ行促音便', '基本形', 'いう', 'イウ', 'イウ'],
             ['え', 'フィラー', '*', '*', '*', '*', '*', 'え', 'エ', 'エ'],
             ['お', '感動詞', '*', '*', '*', '*', '*', 'お', 'オ', 'オ']],
            [['きく', '動詞', '自立', '*', '*', '五段・カ行イ音便', '基本形', 'きく', 'キク', 'キク'],
             ['け', '助詞', '終助詞', '*', '*', '*', '*', 'け', 'ケ', 'ケ'],
             ['こ', '名詞', '一般', '*', '*', '*', '*', 'こ', 'コ', 'コ']],
            [['しす', '動詞', '自立', '*', '*', '五段・サ行', '基本形', 'しす', 'シス', 'シス'],
             ['せ', '動詞', '自立', '*', '*', 'サ変・スル', '未然ヌ接続', 'する', 'セ', 'セ'],
             ['そ', '名詞', '特殊', '助動詞語幹', '*', '*', '*', 'そ', 'ソ', 'ソ']]
        ]
        dc = DataConstructor()
        self.assertEqual(
            dc._sanitize_data_list(csv_list),
            [
                [['きく', '動詞', '自立', '*', '*', '五段・カ行イ音便', '基本形', 'きく', 'キク', 'キク'],
                 ['け', '助詞', '終助詞', '*', '*', '*', '*', 'け', 'ケ', 'ケ'],
                 ['こ', '名詞', '一般', '*', '*', '*', '*', 'こ', 'コ', 'コ']],
                [['しす', '動詞', '自立', '*', '*', '五段・サ行', '基本形', 'しす', 'シス', 'シス'],
                 ['せ', '動詞', '自立', '*', '*', 'サ変・スル', '未然ヌ接続', 'する', 'セ', 'セ'],
                 ['そ', '名詞', '特殊', '助動詞語幹', '*', '*', '*', 'そ', 'ソ', 'ソ']]
            ]
        )

    def test_is_invalid_sentence_true(self):
        dc = DataConstructor()
        self.assertFalse(dc._is_invalid_sentence(
            [
                ['きく', '動詞', '自立', '*', '*', '五段・カ行イ音便', '基本形', 'きく', 'キク', 'キク'],
                ['け', '助詞', '終助詞', '*', '*', '*', '*', 'け', 'ケ', 'ケ'],
                ['こ', '名詞', '一般', '*', '*', '*', '*', 'こ', 'コ', 'コ']
            ]
        ))

    def test_is_invalid_sentence_false(self):
        dc = DataConstructor()
        self.assertTrue(dc._is_invalid_sentence(
            [
                ['あ', 'フィラー', '*', '*', '*', '*', '*', 'あ', 'ア', 'ア'],
                ['いう', '動詞', '自立', '*', '*', '五段・ワ行促音便', '基本形', 'いう', 'イウ', 'イウ'],
                ['え', 'フィラー', '*', '*', '*', '*', '*', 'え', 'エ', 'エ'],
                ['お', '感動詞', '*', '*', '*', '*', '*', 'お', 'オ', 'オ']
            ]
        ))

    def test_can_read(self):
        dc = DataConstructor()
        self.assertTrue(dc._can_read(
            [
                "雨", "名詞", "一般", "*", "*", "*", "*", "雨", "アメ", "アメ"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "-", "名詞", "サ変接続", "*", "*", "*", "*", "*"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "、", "記号", "読点", "*", "*", "*", "*", "、", "、", "、"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "．", "記号", "句点", "*", "*", "*", "*", "．", "．", "．"
            ]
        ))
        self.assertFalse(dc._can_read(
            [
                "　", "記号", "空白", "*", "*", "*", "*", "　", "　", "　"
            ]
        ))

    def test_is_invalid_part(self):
        dc = DataConstructor()
        self.assertTrue(dc._is_invalid_part("形容動詞"))
        self.assertTrue(dc._is_invalid_part("代名詞"))
        self.assertTrue(dc._is_invalid_part("接続詞"))
        self.assertTrue(dc._is_invalid_part("感動詞"))
        self.assertTrue(dc._is_invalid_part("フィラー"))
        self.assertTrue(dc._is_invalid_part("記号"))
        self.assertFalse(dc._is_invalid_part("名詞"))
        self.assertFalse(dc._is_invalid_part("動詞"))
        self.assertFalse(dc._is_invalid_part("助詞"))
        self.assertFalse(dc._is_invalid_part("助動詞"))
        self.assertFalse(dc._is_invalid_part("形容詞"))
        self.assertFalse(dc._is_invalid_part("副詞"))
        self.assertFalse(dc._is_invalid_part("連体詞"))

    def test_is_invalid_part_for_head(self):
        dc = DataConstructor()
        sentence = [['か', '助詞', '副助詞／並立助詞／終助詞', '*', '*', '*', '*', 'か', 'カ', 'カ'],
                    ['きく', '動詞', '自立', '*', '*', '五段・カ行イ音便', '基本形', 'きく', 'キク', 'キク'],
                    ['け', '助詞', '終助詞', '*', '*', '*', '*', 'け', 'ケ', 'ケ'],
                    ['こ', '名詞', '一般', '*', '*', '*', '*', 'こ', 'コ', 'コ']]
        self.assertTrue(dc._is_invalid_part_for_head(sentence))

if __name__ == '__main__':
    unittest.main()
