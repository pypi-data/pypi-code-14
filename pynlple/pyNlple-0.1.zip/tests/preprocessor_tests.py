# -*- coding: utf-8 -*-
import unittest

from processing.preprocessor import RegexReplacer, StackingPreprocessor, DoubleQuotesReplacer, QuotesReplacer, \
    MultiPunctuationReplacer, WordTokenizer, EmailReplacer, NonWordOrNumberOrWhitespaceAllUnicodeReplacer, \
    VKMentionReplacer, URLReplacer, MultiPunctuationAndDotReplacer, BoldTagReplacer


class VKMentionReplacerTest(unittest.TestCase):

    def test_should_replace_with_default(self):
        input_string = u'Здесь в тексте есть ссылка[id254351532|Олололя] как в вконтакте.'
        replacer = VKMentionReplacer()
        result = replacer.preprocess(input_string)
        expected = u'Здесь в тексте есть ссылка как в вконтакте.'
        self.assertEqual(expected, result)

    def test_should_replace_with_tag(self):
        input_string = u'Здесь в тексте есть ссылка[id254351532|Олололя] как в вконтакте.'
        replacer = VKMentionReplacer('tag')
        result = replacer.preprocess(input_string)
        expected = u'Здесь в тексте есть ссылкаtag как в вконтакте.'
        self.assertEqual(expected, result)

    def test_should_replace_hard_case(self):
        input_string = u'Здесь в тексте есть ссылка[id254351532:bp-16297716_231892|Coca-Cola] как в вконтакте.'
        replacer = VKMentionReplacer('tag')
        result = replacer.preprocess(input_string)
        expected = u'Здесь в тексте есть ссылкаtag как в вконтакте.'
        self.assertEqual(expected, result)


class RegexReplacerTest(unittest.TestCase):

    TEST_REGEX = 'a+'
    TEST_TARGET = 'b'
    TEST_STRING = 'cCaaAAaACc'

    TEST_GROUP_REGEX = '(a+)'
    TEST_GROUP_TARGET = '\\1b\\1'

    TEST_W_REGEX = u'\\w'
    TEST_W_TARGET = u'w'
    TEST_W_STRING = u't+tЫ+ЫІ+Іj+j'

    TEST_W_RARE_STRING = u'\u263A+⛇+ۑ+Ҝ+Θ+ᰔ+⃣a+ꋘ'

    def test_should_perform_case_insensitive_replacement(self):
        replacer = RegexReplacer(RegexReplacerTest.TEST_REGEX, RegexReplacerTest.TEST_TARGET, False, False, False)
        result = replacer.preprocess(RegexReplacerTest.TEST_STRING)
        expected = 'cCbCc'
        self.assertEqual(expected, result)

    def test_should_perform_case_sensitive_replacement(self):
        replacer = RegexReplacer(RegexReplacerTest.TEST_REGEX, RegexReplacerTest.TEST_TARGET, True, False, False)
        result = replacer.preprocess(RegexReplacerTest.TEST_STRING)
        expected = 'cCbAAbACc'
        self.assertEqual(expected, result)

    def test_should_perform_w_replacement_without_unicode_symbols(self):
        replacer = RegexReplacer(RegexReplacerTest.TEST_W_REGEX,
                                 RegexReplacerTest.TEST_W_TARGET,
                                 False, False, False)
        result = replacer.preprocess(RegexReplacerTest.TEST_W_STRING)
        expected = u'w+wЫ+ЫІ+Іw+w'
        self.assertEqual(expected, result)

    def test_should_perform_w_replacement_with_unicode_symbols(self):
        replacer = RegexReplacer(RegexReplacerTest.TEST_W_REGEX,
                                 RegexReplacerTest.TEST_W_TARGET,
                                 False, False, True)
        result = replacer.preprocess(RegexReplacerTest.TEST_W_STRING)
        expected = u'w+ww+ww+ww+w'
        self.assertEqual(expected, result)

    def test_should_perform_w_replacement_with_unicode_rare_symbols(self):
        replacer = RegexReplacer(RegexReplacerTest.TEST_W_REGEX,
                                 RegexReplacerTest.TEST_W_TARGET,
                                 False, False, True)
        result = replacer.preprocess(RegexReplacerTest.TEST_W_RARE_STRING)
        expected = u'\u263A+⛇+w+w+w+w+⃣w+w'
        self.assertEqual(expected, result)

    def test_should_replace_rare_double_quotes_in_stack_with_single_quote_replacer(self):
        replacer_1 = QuotesReplacer()
        replacer_2 = DoubleQuotesReplacer()

        replacer = StackingPreprocessor([replacer_1, replacer_2])

        # First symbol is a comma, second one - is a quote
        input_string = u",‚тестируем′ «Нестле» "
        output = replacer.preprocess(input_string)

        expected = u",\'тестируем\' \"Нестле\" "
        self.assertEqual(expected, output)

    def test_should_remove_all_except_words_and_numbers(self):
        punct_string = u'!!!1.word.\' \'2.word-with-hypen 3.word\'s here! ' \
                       u'4.6 12:60 12,000!? -no way-^_^'
        replacer = NonWordOrNumberOrWhitespaceAllUnicodeReplacer()
        result = replacer.preprocess(punct_string)
        expected = u' 1 word   2 word-with-hypen 3 word\'s here  ' \
                   u'4.6 12:60 12,000   no way '
        self.assertEqual(expected, result)

    def test_should_reduce_multiple_punctuation_symbols(self):
        punct_string = u' ... !!...!?????asddf --a !!kek shlak&&**&&&&'
        replacer = MultiPunctuationReplacer()
        result = replacer.preprocess(punct_string)
        expected = u' ... !...!?asddf -a !kek shlak&*&'
        self.assertEqual(expected, result)

    def test_should_reduce_multiple_punctuation_symbols_including_dots(self):
        punct_string = u' ... !!...!?????asddf --a !!kek shlak&&**&&&&'
        replacer = MultiPunctuationAndDotReplacer()
        result = replacer.preprocess(punct_string)
        expected = u' . !.!?asddf -a !kek shlak&*&'
        self.assertEqual(expected, result)

    def test_should_replace_email(self):
        email_string = u'Hi, guys! I had email@yahoo.com, I didn\'t use @ at yahoo.com. Here\'s my new e-mail: my_email+test@mail.yahoo.com. '\
                       u'Can you please validate it?'
        replacer = EmailReplacer(u' emailTag ')
        result = replacer.preprocess(email_string)
        expected = u'Hi, guys! I had  emailTag , I didn\'t use @ at yahoo.com. Here\'s my new e-mail:  emailTag . '\
                   u'Can you please validate it?'
        self.assertEqual(expected, result)

    def test_should_replace_bold_tag(self):
        punct_string = u'#<b>лотерея</b> #<b>выигрыш</b> #<b>лото</b> #<b>тираж</b> #<b>Спортлото</b>'
        replacer = BoldTagReplacer()
        result = replacer.preprocess(punct_string)
        expected = u'#лотерея #выигрыш #лото #тираж #Спортлото'
        self.assertEqual(expected, result)

class TokenizerTest(unittest.TestCase):

    def test_should_tokenize_words(self):
        input_string = u'!These words, un-like-ly said here(sic!), should be tokenized. ' \
                  u'Ukrainska mova takoj z\'yavliaetsia tyt.'
        tokenizer = WordTokenizer()
        expected = u'! These words , un-like-ly said here ( sic ! ) , should be tokenized . ' \
                   u'Ukrainska mova takoj z\'yavliaetsia tyt .'

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_words_w_cyrillics(self):
        input_string = u'за 2011 год). Вот полный список торговых марок от Nestle, которые можно найти в любом российском магазине: Nescafé, КитКат,'
        tokenizer = WordTokenizer()
        expected = u'за 2011 год ) . Вот полный список торговых марок от Nestle , которые можно найти в любом российском магазине : Nescafé , КитКат ,'

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_digits_w_special_symbols(self):
        input_string = u"0.0, 000 00-00 00- 00' 0.00, 00.00, 00:00, 0000.00.00, 0000:00, 000,00, 00..00 :00 0"
        tokenizer = WordTokenizer()
        expected = u"0.0 , 000 00 - 00 00 - 00 ' 0.00 , 00.00 , 00:00 , 0000.00.00 , 0000:00 , 000,00 , 00 .. 00 : 00 0"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_words_w_special_symbols(self):
        input_string = u"п'ятого 'november' з-під рову- merry-go-round"
        tokenizer = WordTokenizer()
        expected = u"п'ятого ' november ' з-під рову - merry-go-round"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_not_tokenize_words_w_dash(self):
        input_string = u"wi-fi"
        tokenizer = WordTokenizer()
        expected = u"wi-fi"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_words_w_digits_w_special_symbols(self):
        input_string = u"25.двадцатьпять 15'16-річний я 15'ок 'солюшнз-"
        tokenizer = WordTokenizer()
        expected = u"25 . двадцатьпять 15 ' 16-річний я 15'ок ' солюшнз -"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_words_w_digits(self):
        input_string = u"25двадцатьпять 15річний15"
        tokenizer = WordTokenizer()
        expected = u"25 двадцатьпять 15 річний 15"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_tokenize_words_and_not_multiple_dots(self):
        input_string = u"...я ... не знаю... что и... сказать"
        tokenizer = WordTokenizer()
        expected = u"... я ... не знаю ... что и ... сказать"

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)

    def test_should_replace_urls_with_tags_isnide(self):
        replacement = u'LINK'
        input_string = u'this is the link http://dostavka-gaza-v-<b>dom</b>.<b>ru</b> we need to replace.'
        tokenizer = URLReplacer(replace_tag_with=replacement)
        expected = u'this is the link ' + replacement + u' we need to replace.'

        result = tokenizer.preprocess(input_string)
        self.assertEqual(expected, result)


class StackingPreprocessorTest(unittest.TestCase):

    REGEX_1 = 'a'
    TARGET_1 = 'b'
    REGEX_2 = 'c'
    TARGET_2 = 'd'

    def test_should_replace_continuosly_without_collisions(self):
        replacer_1 = RegexReplacer(StackingPreprocessorTest.REGEX_1, StackingPreprocessorTest.TARGET_1, False, False, False)
        replacer_2 = RegexReplacer(StackingPreprocessorTest.REGEX_2, StackingPreprocessorTest.TARGET_2, False, False, False)

        stacking_replacer = StackingPreprocessor()
        stacking_replacer.append_preprocessor(replacer_1)
        stacking_replacer.append_preprocessor(replacer_2)

        input_string = 'acaca'
        output = stacking_replacer.preprocess(input_string)

        expected = 'bdbdb'
        self.assertEqual(expected, output)

    def test_should_replace_continuosly_with_chaining(self):
        replacer_1 = RegexReplacer(StackingPreprocessorTest.REGEX_1, StackingPreprocessorTest.TARGET_1, False, False, False)
        replacer_2 = RegexReplacer(StackingPreprocessorTest.TARGET_1, StackingPreprocessorTest.TARGET_2, False, False, False)

        stacking_replacer = StackingPreprocessor()

        stacking_replacer.append_preprocessor(replacer_1)
        stacking_replacer.append_preprocessor(replacer_2)

        input_string = 'acaca'
        output = stacking_replacer.preprocess(input_string)

        expected = 'dcdcd'
        self.assertEqual(expected, output)

    def test_should_replace_in_right_order_when_prepend(self):
        replacer_1 = RegexReplacer(StackingPreprocessorTest.TARGET_2, StackingPreprocessorTest.TARGET_1, False, False, False)
        replacer_2 = RegexReplacer(StackingPreprocessorTest.REGEX_2, StackingPreprocessorTest.TARGET_2, False, False, False)

        stacking_replacer = StackingPreprocessor()

        stacking_replacer.append_preprocessor(replacer_1)
        stacking_replacer.prepend_preprocessor(replacer_2)

        input_string = 'acaca'
        output = stacking_replacer.preprocess(input_string)

        expected = 'ababa'
        self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()
