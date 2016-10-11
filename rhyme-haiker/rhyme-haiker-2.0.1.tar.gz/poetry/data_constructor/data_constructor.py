# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
from logging import INFO
import MeCab
import re

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


class DataConstructor:

    WORD = 0
    PART = 1
    PART_SUBTYPE = 2
    PRONOUNCIATION = 9

    DELIMITER = '\n'
    EMPTY = ''

    def __init__(self):
        self.yomi = ""
        self.vowel_pronounciation = ""

    def construct_data(self, read_data):
        """
        インターフェイス
        テーブル挿入用データを作成する．
        """
        return self._construct_parsed_data(read_data)  # TODO: 修正対象

    def _construct_parsed_data(self, read_data):
        """
        Mecab で解析後のデータを返す
        """
        # 1文を改行コードで切る
        delimited_read_data_list = self._delimit(read_data)
        # 句読点で改行
        text_list = list()
        for line in delimited_read_data_list:
            text_list += self._start_new_line(line)
        parsed_list = self._parse_list(text_list)
        csv_list = self._splited_word_data_to_csv_list(parsed_list)
        sanitized_data_list = self._sanitize_data_list(csv_list)
        return self._extract_data(sanitized_data_list)

    def _delimit(self, parsed_text):
        return parsed_text.splitlines()

    def _start_new_line(self, text):
        """
        句読点で改行する
        """
        assert isinstance(text, str), '引数が文字列ではない: {}'.format(text)
        text_list = [text]
        symbols = ['、', '。', '，', '．']
        for s in symbols:
            tmp_list = list()

            for t in text_list:
                for splited_list in t.split(s):
                    tmp_list.append(splited_list)
            text_list = tmp_list

        if text_list.count(self.EMPTY):
            text_list.remove(self.EMPTY)
        return text_list

    def _parse_list(self, text_list):
        """
        リスト中の単語をそれぞれパースする
        """
        m = MeCab.Tagger()
        parsed_list = list()
        for text in text_list:
            parsed = m.parse(text)
            substituted = re.sub('\nEOS', '', parsed)
            splited_list = substituted.split('\n')
            splited_list.remove('')
            parsed_list.append(splited_list)
        return parsed_list

    def _splited_word_data_to_csv_list(self, parsed_list):
        """
        分かち書き後のデータリストを csv のリストへ変換．
        """
        # TODO: Utils クラスへ引越
        csv_list = list()
        for sentence in parsed_list:
            splited_sentence = list()
            for parsed_words in sentence:
                if not isinstance(parsed_words, str):
                    logger.warning("Input value is not String: %s." % parsed_words)

                csv_text = re.sub('\t', ',', parsed_words)
                splited_csv_list = csv_text.split(',')
                splited_sentence.append(splited_csv_list)
            csv_list.append(splited_sentence)
        return csv_list

    def _sanitize_data_list(self, csv_list):
        """
        csv のリストから不要なデータを除外．
        """
        if not isinstance(csv_list, list):
            logger.warning("Input value is not List: %s." % csv_list)

        sanitized_data_list = []
        unique_sentence_list = []
        for sentence in csv_list:
            if self._is_invalid_sentence(sentence):
                logger.debug("Invalid sentence: %s." % sentence)
            elif sentence in unique_sentence_list:
                logger.debug("Duplicated: %s." % sentence)
            else:
                sanitized_data_list.append(sentence)
                unique_sentence_list.append(sentence)
        return sanitized_data_list

    def _is_invalid_sentence(self, sentence):
        """
        文章に含まれる単語リストを探索し，
        不適切な単語が含まれる場合 False を返す
        除外対象
        - 辞書に 読み が登録されていない項目
        """
        if not isinstance(sentence, list):
            logger.warning("Input value is not List: %s." % sentence)

        if self._is_invalid_part_for_head(sentence):
            logger.debug("Invalid sentence head: %s" % sentence)
            return True
        for csv_data in sentence:
            if not self._can_read(csv_data):
                logger.debug("Invalid word: %s." % csv_data[self.WORD])
                return True
            elif self._is_invalid_part(csv_data[self.PART]):
                logger.debug("Invalid part: %s." % csv_data[self.PART])
                return True
            else:
                continue
        return False

    def _can_read(self, csv_data):
        """
        辞書に 読み が登録されている場合，True を返す．
        特殊な音(フォ，ウォ など)は登録されている場合といない場合とがあるので注意．
        """
        if not isinstance(csv_data, list):
            logger.warning("{}: Input value is not List: {}.".format(__name__, csv_data))

        logger.debug("--------------------------------------")
        logger.debug(csv_data)
        if len(csv_data) <= self.PRONOUNCIATION:
            return False
        elif csv_data[self.PART] == u'記号':
            return False
        elif csv_data[self.PART] is '名詞' and \
                csv_data[self.PART_SUBTYPE is 'サ変接続']:
            return False
        else:
            return True

    def _is_invalid_part(self, part):
        """
        無効な品詞の場合，True を返す
        """
        assert isinstance(part, str), 'Input value is not Str: {}'.format(part)
        valid_parts = ['名詞',
                       '動詞',
                       '助詞',
                       '助動詞',
                       '形容詞',
                       '副詞',
                       '連体詞']
        if part in valid_parts:
            return False
        else:
            return True

    def _is_invalid_part_for_head(self, sentence):
        """
        文章の先頭に無効な品詞がある場合，True を返す
        """
        invalid_parts = ['助詞']
        if sentence[0][self.PART] in invalid_parts:
            return True
        else:
            return False

    def _extract_data(self, csv_data_list):
        """
        出力したいデータごとに構築された辞書を返す．
        子クラスでオーバーライドして使う．
        """
        raise NotImplementedError
