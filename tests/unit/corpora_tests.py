import codecs
import os
import shutil
import unittest
from unittest.mock import patch

from corpora_utils import sample_stanford_imdb_dataset, clean_text, get_bow_dictionary, \
    get_stanford_imbd_vocabulary, get_stanford_imdb_markup_vocabulary, get_stanford_imdb_labels_features
from utils import ConfigHelper


def _mock_stfrd_imdb_file_download(url: str, local_file_path: str):
    shutil.copy('test-stfrd-reviews.tar.gz', local_file_path)


def _read_lines(file_path: str) -> list:
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


class TestCorporaUtils(unittest.TestCase):
    @patch('corpora_utils._download_file', _mock_stfrd_imdb_file_download)
    def test_sample_stanford_imdb_dataset(self):
        try:
            sample_stanford_imdb_dataset(train_size=5, dev_size=3, test_size=5)

            train_file_path = ConfigHelper.get_config_value('stanford_movie_review_train_file_path', 'corpora')
            dev_file_path = ConfigHelper.get_config_value('stanford_movie_review_dev_file_path', 'corpora')
            test_file_path = ConfigHelper.get_config_value('stanford_movie_review_test_file_path', 'corpora')

            # ensure train, dev and test files exists
            self.assertTrue(os.path.exists(train_file_path) and os.path.isfile(train_file_path))
            self.assertTrue(os.path.exists(dev_file_path) and os.path.isfile(dev_file_path))
            self.assertTrue(os.path.exists(test_file_path) and os.path.isfile(test_file_path))

            # ensure no.of lines in each file matches what's expected
            self.assertEqual(5, len(_read_lines(train_file_path)))
            self.assertEqual(3, len(_read_lines(dev_file_path)))
            self.assertEqual(5, len(_read_lines(test_file_path)))
        finally:
            shutil.rmtree('data')
            shutil.rmtree('temp')

    def test_clean_text(self):
        import corpora_utils
        temp = list(corpora_utils.HTML_WHITESPACE_PATTERNS)
        corpora_utils.HTML_WHITESPACE_PATTERNS.extend([r'<pre */?>'])
        try:
            s = ' \t\nabcd <br> <br />  <br > <br/> <br   /><pre><pre/><pre /> efg\n\t  '
            self.assertEqual('abcd               efg', clean_text(s))
        finally:
            corpora_utils.HTML_WHITESPACE_PATTERNS = list(temp)

    def test_get_bow_dictionary(self):
        s = 'The road goes ever on and on, down from the road where it began.'
        self.assertEqual({
            'The': 1,
            'road': 2,
            'goes': 1,
            'ever': 1,
            'on': 1,
            'and': 1,
            'on,': 1,
            'down': 1,
            'from': 1,
            'the': 1,
            'where': 1,
            'it': 1,
            'began.': 1,
        }, get_bow_dictionary(s))

    def test_get_stanford_imbd_vocabulary(self):
        vocabulary: set = get_stanford_imbd_vocabulary('text_file_for_test.txt')
        self.assertEqual(20, len(vocabulary))

    def test_get_stanford_imdb_markup_vocabulary(self):
        vocabulary: set = get_stanford_imdb_markup_vocabulary('text_file_for_test.txt')
        self.assertEqual({'<pre/>', '<br>', '<p>', '<br />', '<test 123>'}, vocabulary)

    def test_get_stanford_imdb_labels_features(self):
        labels_features = get_stanford_imdb_labels_features('text_file_for_test.txt')
        self.assertEqual(5, len(labels_features))
        self.assertEqual((1, {'efg': 1, '<p>': 1, '<pre/>': 1}), labels_features[2])
        self.assertEqual((1, {'hijk': 1}), labels_features[3])
        self.assertEqual((-1, {'lmnop': 1, '<test': 1, '123>': 1}), labels_features[4])
