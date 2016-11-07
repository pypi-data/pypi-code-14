# -*- coding: utf-8 -*-
import unittest

from processing.dictionary import DictionaryLookUp, Tagger, FileDictionaryLookUp


class TaggerTest(unittest.TestCase):

    def setUp(self):
        self.mappings = [
            ('a b c', 'class1'),
            ('a b', 'class11'),
            ('a c', 'class1'),
            ('b c', 'class11'),
            ('a a a', 'class2'),
            ('a a', 'class21'),
            ('b b b', 'class2'),
            ('c c c', 'class2'),
            ('a b c d', 'class3'),
            ('a b c e', 'class3'),
        ]
        self.dictionary = DictionaryLookUp(self.mappings)

    def test_should_result_be_empty(self):
        tagger = Tagger(DictionaryLookUp([]))
        tokens = 'a b c a b a a a c c c a b c d a b c e'.split()
        self.assertEqual(0, len(tagger.get_tagged_entities(tokens)))

    def test_should_match_one_result(self):
        tagger = Tagger(self.dictionary)
        tokens = 'a c a b'.split()
        self.assertEqual([(0, 2, 'class1'), (2, 4, 'class11')], tagger.get_tagged_entities(tokens))

    def test_should_match_some_results(self):
        tagger = Tagger(self.dictionary)
        tokens = 'c c c a'.split()
        self.assertEqual((0, 3, 'class2'), tagger.get_tagged_entities(tokens)[0])

    def test_should_match_many_longer_parts_results(self):
        tagger = Tagger(self.dictionary)
        tokens = 'a b c b b b a b c e a a a'.split()
        self.assertEqual([(0, 3, 'class1'),
                          (3, 6, 'class2'),
                          (6, 10, 'class3'),
                          (10, 13, 'class2')],
                         tagger.get_tagged_entities(tokens, False))

    def test_should_match_all_and_short_parts_results(self):
        tagger = Tagger(self.dictionary)
        tokens = 'a b c b b b a b c e a a a'.split()
        self.assertEqual({(0, 3, 'class1'),
                          (0, 2, 'class11'),
                          (1, 3, 'class11'),
                          (3, 6, 'class2'),
                          (6, 10, 'class3'),
                          (6, 8, 'class11'),
                          (7, 9, 'class11'),
                          (6, 9, 'class1'),
                          (10, 13, 'class2'),
                          (10, 12, 'class21'),
                          (11, 13, 'class21')},
                         set(tagger.get_tagged_entities(tokens, True)))


class FileDictionaryLookUpTest(unittest.TestCase):

    def test_should_init_from_file(self):
        filepath = 'data/punctuation'
        dictionary = FileDictionaryLookUp(filepath)
        self.assertIsNotNone(dictionary)

    def test_should_contain(self):
        filepath = 'data/punctuation'
        dictionary = FileDictionaryLookUp(filepath)
        self.assertIsNotNone(dictionary['.'])

    def test_should_not_contain(self):
        filepath = 'data/punctuation'
        dictionary = FileDictionaryLookUp(filepath)
        self.assertIsNone(dictionary['...'])

    def test_should_get_correct_tag(self):
        filepath = 'data/punctuation'
        dictionary = FileDictionaryLookUp(filepath)
        self.assertEquals(filepath, dictionary['.'])


class DictionaryLookUpTest(unittest.TestCase):

    def setUp(self):
        self.mappings = [
            ('a b c', 'class1'),
            ('a b', 'class11'),
            ('a c', 'class1'),
            ('b c', 'class1'),
            ('a a a', 'class2'),
            ('a a', 'class21'),
            ('b b b', 'class2'),
            ('c c c', 'class2'),
            ('a b c d', 'class3'),
            ('a b c e', 'class3'),
        ]

    def test_should_init_from_strings(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNotNone(dictionary)

    def test_should_init_from_tokens(self):
        dictionary = DictionaryLookUp([(tokens.split(), classes) for (tokens, classes) in self.mappings])
        self.assertIsNotNone(dictionary)

    def test_should_contain_simple_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNotNone(dictionary.get_tag(self.mappings[7][0]))

    def test_should_contain_sub_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNotNone(dictionary.get_tag(self.mappings[1][0]))

    def test_should_contain_mega_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNotNone(dictionary.get_tag(self.mappings[8][0]))

    def test_should_not_contain_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNone(dictionary.get_tag(' '.join([tokens for tokens, _ in self.mappings])))

    def test_should_contain_correct_tag_for_simple_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertEqual(dictionary.get_tag(self.mappings[7][0]), self.mappings[7][1])

    def test_should_contain_correct_tag_for_sub_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertEqual(dictionary.get_tag(self.mappings[1][0]), self.mappings[1][1])

    def test_should_contain_correct_tag_for_mega_mapping(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertEqual(dictionary.get_tag(self.mappings[8][0]), self.mappings[8][1])

    def test_should_rewrite_class(self):
        new_mappings = list(self.mappings)
        new_mappings.append((self.mappings[len(self.mappings) - 1][0],self.mappings[len(self.mappings) - 1][1][::-1]))
        dictionary = DictionaryLookUp(new_mappings)
        self.assertEqual(dictionary.get_tag(self.mappings[len(self.mappings) - 1][0]), new_mappings[len(new_mappings) - 1][1])
        self.assertNotEqual(dictionary.get_tag(self.mappings[len(self.mappings) - 1][0]), self.mappings[len(self.mappings) - 1][1])

    def test_should_contain_correct_tag_for_simple_mapping_via_getitem(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertEqual(dictionary[self.mappings[7][0]], self.mappings[7][1])

    def test_should_contain_simple_mapping_via_getitem(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertIsNotNone(dictionary[self.mappings[7][0]])

    def test_should_add_simple_mapping_via_setitem(self):
        dictionary = DictionaryLookUp({})
        dictionary['new mapping'] = 'new_class'
        self.assertIsNotNone(dictionary['new mapping'])
        self.assertEqual(dictionary['new mapping'], 'new_class')

    def test_should_get_longest(self):
        dictionary = DictionaryLookUp(self.mappings)
        self.assertEqual(max([len(token.split()) for token, _ in self.mappings]), dictionary.get_longest_sequence())

    def test_should_get_longest_zero(self):
        dictionary = DictionaryLookUp([])
        self.assertEqual(0, dictionary.get_longest_sequence())

    def test_should_get_longest_multiple_alternatives(self):
        mappings = [('a a a a a a a a a a b', 'c'), ('a a a a a a a a a a c', 'c2')]
        dictionary = DictionaryLookUp(mappings)
        self.assertEqual(max([len(token.split()) for token, _ in mappings]), dictionary.get_longest_sequence())
