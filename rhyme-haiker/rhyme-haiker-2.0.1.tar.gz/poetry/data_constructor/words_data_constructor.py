# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import re

from poetry.data_constructor.data_constructor import DataConstructor

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class WordsDataConstructor(DataConstructor):

    FIVE_STR = 'five'
    SEVEN_STR = 'seven'

    LENGTH = 'length'

    def _extract_data(self, csv_data_list):
        """
        親クラスのメソッドをオーバーライド．
        下記のようなデータ構造を返す．
        {
            'five': [
                [
                    {
                        "word": "あ",
                        "vowel": "ア",
                        "length": 1,
                        "part": "名詞"
                    },
                    ...,
                    {
                        "word": "い",
                        "vowel": "イ",
                        "length": 1,
                        "part": "名詞"
                    }
                ],
                [
                    {
                        "word": "か",
                        "vowel": "カ",
                        "length": 1,
                        "part": "名詞"
                    },
                    {
                        "word": "き",
                        "vowel": "キ",
                        "length": 1,
                        "part": "名詞"
                    }
                    ,
                    ...
                ]
            ],
            'seven': [
                ...
            ]
        }
        """
        extracted_data_list = [[self._construct_words_dict(csv_data) for csv_data in sentence] for sentence in csv_data_list]
        # 5, 7 文字からなる文章以外除外
        sentence_five = self._extract_n_char_sentence(5, extracted_data_list)
        sentence_seven = self._extract_n_char_sentence(7, extracted_data_list)
        return {self.FIVE_STR: sentence_five,
                self.SEVEN_STR: sentence_seven}

    def _construct_words_dict(self, csv_data):
        """
        単語，品詞，読みの母音，読みの字数の辞書を返す
        """
        if not isinstance(csv_data, list):
            logger.warning("Input value is not List: %s." % csv_data)

        self.yomi = csv_data[self.PRONOUNCIATION]
        self._substitute_vowel()

        return {
            "word": csv_data[self.WORD],
            "part": csv_data[self.PART],
            "vowel": self.vowel_pronounciation,
            "length": len(self.vowel_pronounciation)
        }

    def _substitute_vowel(self):
        """
        読み の子音を母音に置換する
        """
        # 拗音をリストの先頭にする
        try:
            substituted_yomi = self._substitute_diphthong()
            self.vowel_pronounciation = self._substitute_straight_syllables(substituted_yomi)
        except SubstitutionError as e:
            print('Substitution was incompleted.', e.origin, e.value)

    def _substitute_diphthong(self):
        """
        拗音を母音に置換する．
        拗音と定義されていない特殊な音も置換．
        ローマ字変換を参考．
        """
        a = 'ア'
        i = 'イ'
        u = 'ウ'
        e = 'エ'
        o = 'オ'
        a_diphthong = (
            'キャ', 'シャ', 'チャ', 'ニャ', 'ヒャ', 'ミャ', 'リャ', 'ギャ', 'ジャ', 'ヂャ', 'ビャ', 'ピャ',
            'クァ', 'クヮ', 'グヮ',                         'ツァ', 'テャ', 'デャ', 'ファ', 'フャ', 'ブャ', 'ウァ', 'ヴァ', 'ブァ'
        )
        i_diphthong = (
            'クィ',         'グィ', 'ジィ', 'チィ', 'ヂィ', 'ツィ', 'ティ', 'ディ', 'フィ',                 'ウィ', 'ヴィ', 'ブィ'
        )
        u_diphthong = (
            'キュ', 'シュ', 'チュ', 'ニュ', 'ヒュ', 'ミュ', 'リュ', 'ギュ', 'ジュ', 'ヂュ', 'ビュ', 'ピュ',
            'クゥ',         'グゥ',                                 'テュ', 'デュ',         'フュ', 'ブュ'
        )
        e_diphthong = (
            'クェ', 'グェ', 'シェ', 'ジェ', 'チェ', 'ヂェ', 'ツェ', 'テェ', 'デェ', 'フェ',                 'ウェ', 'ヴェ', 'ブェ'
        )
        o_diphthong = (
            'キョ', 'ショ', 'チョ', 'ニョ', 'ヒョ', 'ミョ', 'リョ', 'ギョ', 'ジョ', 'ヂョ', 'ビョ', 'ピョ',
            'クォ',         'グォ',                         'ツォ', 'テョ', 'デョ', 'フォ', 'フョ', 'ブョ', 'ウォ', 'ヴォ', 'ブォ'
        )
        vowel_dict = {
            a: a_diphthong,
            i: i_diphthong,
            u: u_diphthong,
            e: e_diphthong,
            o: o_diphthong
        }

        substituted_yomi = self.yomi

        for vowel, consonants in vowel_dict.items():
            for c in consonants:
                substituted_yomi = re.sub(c, vowel, substituted_yomi)
        return substituted_yomi

    def _substitute_straight_syllables(self, yomi):
        """
        直音を母音に置換する．
        """
        a = 'ア'
        i = 'イ'
        u = 'ウ'
        e = 'エ'
        o = 'オ'
        a_consonants = ('カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', "ャ")
        i_consonants = ('キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ',       'リ',       'ギ', 'ジ', 'ヂ', 'ビ', 'ピ')
        u_consonants = ('ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル',       'グ', 'ズ', 'ヅ', 'ブ', 'プ', "ュ")
        e_consonants = ('ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ',       'レ',       'ゲ', 'ゼ', 'デ', 'ベ', 'ペ')
        o_consonants = ('コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', "ョ")
        vowel_dict = {
            a: a_consonants,
            i: i_consonants,
            u: u_consonants,
            e: e_consonants,
            o: o_consonants
        }

        substituted_yomi = yomi

        for vowel, consonants in vowel_dict.items():
            for c in consonants:
                substituted_yomi = re.sub(c, vowel, substituted_yomi)

                if self._completed_substitution(substituted_yomi):
                    return substituted_yomi

        # 置換完了しなかった場合
        raise SubstitutionError(yomi, substituted_yomi)

    def _completed_substitution(self, current_yomi):
        """
        拗音が全て置換済みであることが前提条件．
        母音と子音の置換が終わった場合 True を返す
        """
        if not isinstance(current_yomi, str):
            logger.warning("Input value is not String: %s." % current_yomi)

        # 可換な文字リスト
        substitutable_list = (
            'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ', 'ガ', 'ザ', 'ダ', 'バ', 'パ', "ャ",
            'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ',       'リ',       'ギ', 'ジ', 'ヂ', 'ビ', 'ピ',
            'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル',       'グ', 'ズ', 'ヅ', 'ブ', 'プ', "ュ",
            'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ',       'レ',       'ゲ', 'ゼ', 'デ', 'ベ', 'ペ',
            'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', 'ヲ', 'ゴ', 'ゾ', 'ド', 'ボ', 'ポ', "ョ"
        )

        origin_yomi = current_yomi

        for o, c in zip(origin_yomi, current_yomi):
            if o not in substitutable_list:
                continue
            if o == c:
                return False
        return True

    def _extract_n_char_sentence(self, n, sentence_list):
        """
        n 文字の文章のみ取得
        """
        n_char_sentence_list = list()
        for sentence in sentence_list:
            len_sum = 0
            for word in sentence:
                len_sum += word[self.LENGTH]
                if len_sum > n:
                    break
            if len_sum == n:
                n_char_sentence_list.append(sentence)
        return n_char_sentence_list


class SubstitutionError(Exception):

    def __init__(self, origin, value):
        self.origin = origin
        self.value = value

    def __str__(self):
        return repr(self.origin, self.value)
