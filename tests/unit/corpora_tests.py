import codecs
import os
import shutil
import unittest
from unittest.mock import patch

from corpora_utils import sample_stanford_imdb_dataset
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
