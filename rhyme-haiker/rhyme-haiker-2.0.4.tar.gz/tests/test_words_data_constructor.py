# -*- coding: utf-8 -*-

from poetry.data_constructor.words_data_constructor import WordsDataConstructor
import unittest

import MeCab


class TestWordsDataConstructor(unittest.TestCase):

    def test_construct_parsed_data(self):
        wdc = WordsDataConstructor()

        read_data = "気象庁"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            {
                wdc.FIVE_STR: [
                    [
                        {
                            "word": "気象庁",
                            "part": "名詞",
                            "vowel": "イオーオー",
                            "length": 5
                        }
                    ]
                ],
                wdc.SEVEN_STR: []
            }
        )

        read_data = "雨が降る"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            {
                wdc.FIVE_STR: [
                    [
                        {
                            "word": "雨",
                            "part": "名詞",
                            "vowel": "アエ",
                            "length": 2
                        },
                        {
                            "word": "が",
                            "part": "助詞",
                            "vowel": "ア",
                            "length": 1
                        },
                        {
                            "word": "降る",
                            "part": "動詞",
                            "vowel": "ウウ",
                            "length": 2
                        }
                    ]
                ],
                wdc.SEVEN_STR: []
            }
        )

        read_data = "あいうえお，さしすせそ"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            {
                wdc.FIVE_STR:
                [
                    [
                        {
                            "word": "さ",
                            "part": "副詞",
                            "vowel": "ア",
                            "length": 1
                        },
                        {
                            "word": "しす",
                            "part": "動詞",
                            "vowel": "イウ",
                            "length": 2
                        },
                        {
                            "word": "せ",
                            "part": "動詞",
                            "vowel": "エ",
                            "length": 1
                        },
                        {
                            "word": "そ",
                            "part": "名詞",
                            "vowel": "オ",
                            "length": 1
                        }
                    ]
                ],
                wdc.SEVEN_STR: []
            }
        )

        read_data = "かきくけこ，さしすせそ"
        self.assertEqual(
            wdc._construct_parsed_data(read_data),
            {
                wdc.FIVE_STR: [
                    [
                        {
                            "word": "かき",
                            "part": "動詞",
                            "vowel": "アイ",
                            "length": 2
                        },
                        {
                            "word": "くけ",
                            "part": "動詞",
                            "vowel": "ウエ",
                            "length": 2
                        },
                        {
                            "word": "こ",
                            "part": "動詞",
                            "vowel": "オ",
                            "length": 1
                        }
                    ],
                    [
                        {
                            "word": "さ",
                            "part": "副詞",
                            "vowel": "ア",
                            "length": 1
                        },
                        {
                            "word": "しす",
                            "part": "動詞",
                            "vowel": "イウ",
                            "length": 2
                        },
                        {
                            "word": "せ",
                            "part": "動詞",
                            "vowel": "エ",
                            "length": 1
                        },
                        {
                            "word": "そ",
                            "part": "名詞",
                            "vowel": "オ",
                            "length": 1
                        }
                    ]
                ],
                wdc.SEVEN_STR: []
            }
        )

    def test_extract_data(self):
        import re
        m = MeCab.Tagger()
        mecabed_sentence_a = m.parse("あいうえお").split("\n")[:-4]
        mecabed_csv_list_a = [re.sub('\t', ',', mecabed_list).split(',') for mecabed_list in mecabed_sentence_a]
        mecabed_sentence_s = m.parse("さしすせそ").split("\n")[:-2]
        mecabed_csv_list_s = [re.sub('\t', ',', mecabed_list).split(',') for mecabed_list in mecabed_sentence_s]
        mecabed_csv_list = [mecabed_csv_list_a,
                            mecabed_csv_list_s]
        wdc = WordsDataConstructor()
        self.assertEqual(
            wdc._extract_data(mecabed_csv_list),
            {
                wdc.FIVE_STR: [
                    [
                        {
                            "word": "さ",
                            "part": "副詞",
                            "vowel": "ア",
                            "length": 1
                        },
                        {
                            "word": "しす",
                            "part": "動詞",
                            "vowel": "イウ",
                            "length": 2
                        },
                        {
                            "word": "せ",
                            "part": "動詞",
                            "vowel": "エ",
                            "length": 1
                        },
                        {
                            "word": "そ",
                            "part": "名詞",
                            "vowel": "オ",
                            "length": 1
                        }
                    ]
                ],
                wdc.SEVEN_STR: []
            }
        )

    def test_substitute_vowel(self):
        wdc = WordsDataConstructor()
        wdc.yomi = "カキクケコ"
        wdc._substitute_vowel(),
        self.assertEqual(
            wdc.vowel_pronounciation,
            "アイウエオ"
        )
        wdc.yomi = "キショーチョー"
        wdc._substitute_vowel(),
        self.assertEqual(
            wdc.vowel_pronounciation,
            "イオーオー"
        )

    def test_substitute_diphthong(self):
        wdc = WordsDataConstructor()
        wdc.yomi = "キショーチョー"  # 気象庁
        self.assertEqual(
            wdc._substitute_diphthong(),
            "キオーオー"
        )
        wdc.yomi = "ヒャフォウォー"
        self.assertEqual(
            wdc._substitute_diphthong(),
            "アオオー"
        )

    def test_substitute_straight_syllables(self):
        wdc = WordsDataConstructor()
        yomi = "サシスセソ"
        self.assertEqual(
            wdc._substitute_straight_syllables(yomi),
            "アイウエオ"
        )

    def test_completed_substitution(self):
        complete_yomi = "アイウエオ"
        incomplete_yomi = "カイウエオ"

        wdc = WordsDataConstructor()
        wdc.yomi = "アイウエオ"
        self.assertTrue(wdc._completed_substitution(complete_yomi))
        wdc.yomi = "カキクケコ"
        self.assertFalse(wdc._completed_substitution(incomplete_yomi))

if __name__ == '__main__':
    unittest.main()
