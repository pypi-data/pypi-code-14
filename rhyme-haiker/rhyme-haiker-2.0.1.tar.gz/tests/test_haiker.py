# -*- coding: utf-8 -*-

from poetry.data_constructor.words_data import WordsData
from poetry.haiker.haiker import Haiker
import unittest


class TestHaiker(unittest.TestCase):

    SUCCESS_WORDS_FIVE = [
        [
            {
                "word": "あああ",
                "vowel": "アアア",
                "length": 3,
                "part": "名詞"
            },
            {
                "word": "いい",
                "vowel": "イイ",
                "length": 2,
                "part": "名詞"
            }
        ]
    ]
    SUCCESS_WORDS_SEVEN = [
        [
            {
                "word": "ああああ",
                "vowel": "アアアア",
                "length": 4,
                "part": "名詞"
            },
            {
                "word": "いいい",
                "vowel": "イイイ",
                "length": 3,
                "part": "名詞"
            }
        ]
    ]
    WORDS = [
        {
            "word": "古池",
            "vowel": "ウウイエ",
            "length": 4,
            "part": "名詞"
        },
        {
            "word": "蛙",
            "vowel": "アエウ",
            "length": 3,
            "part": "名詞"
        },
        {
            "word": "あ",
            "vowel": "ア",
            "length": 1,
            "part": "名詞"
        },
        {
            "word": "い",
            "vowel": "イ",
            "length": 1,
            "part": "名詞"
        },
        {
            "word": "う",
            "vowel": "ウ",
            "length": 1,
            "part": "名詞"
        }
    ]

    def test_get_n_char_sentence(self):
        haiker = Haiker()

        WordsData.words_five_list = self.SUCCESS_WORDS_FIVE
        WordsData.words_seven_list = self.SUCCESS_WORDS_SEVEN

        sentence = haiker._get_n_char_sentence(5)
        sentence_len = len(WordsData._get_vowel(sentence))
        self.assertEqual(
            sentence_len,
            5
        )

        sentence = haiker._get_n_char_sentence(7)
        sentence_len = len(WordsData._get_vowel(sentence))
        self.assertEqual(
            sentence_len,
            7
        )

        with self.assertRaises(ValueError):
            haiker._get_n_char_sentence(1)

if __name__ == '__main__':
    unittest.main()
