import unittest

from utils import ConfigHelper, HttpHelper, get_sample_dataset, StringHelper, FileHelper


class TestUtils(unittest.TestCase):
    def test_config_helper(self):
        self.assertEqual(ConfigHelper.get_config_value('key1', 'section1'), 'section1-value1')
        self.assertEqual(ConfigHelper.get_config_value('key2', 'section1'), 'section1-value2')
        self.assertEqual(ConfigHelper.get_config_value('key3', 'section1'), 'section1-value1+section1-value2+value3')

        self.assertEqual(ConfigHelper.get_config_value('key1', 'section2'), 'section2-value1')
        self.assertEqual(ConfigHelper.get_config_value('key2', 'section2'), 'section2-value2')
        self.assertEqual(ConfigHelper.get_config_value('key3', 'section2'), 'section2-value1+section2-value2+value3')

        self.assertEqual('section1-value1+section1-value2+value3+section2-value1+section2-value2+value3+value',
                         ConfigHelper.get_config_value('key', 'section3'))

        self.assertEqual('value1', ConfigHelper.get_config_value('key1'))
        self.assertEqual('value2', ConfigHelper.get_config_value('key2'))
        self.assertEqual('value1+value2+value3', ConfigHelper.get_config_value('key3'))
        self.assertEqual('value1+section1-value1+section2-value1+value_x', ConfigHelper.get_config_value('key_x', 'section3'))

        self.assertEqual('defaultvalue', ConfigHelper.get_config_value('missingkey', default_value='defaultvalue'))
        self.assertEqual('defaultvalue', ConfigHelper.get_config_value('missingkey', 'missingsection',
                                                                       default_value='defaultvalue'))

    @unittest.skip
    def test_download_file(self):
        local_file_path = 'aclImdb_v1.tar.gz'
        HttpHelper.download_file('https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz',
                                 local_file_path)

    def test_get_sample_dataset(self):
        class_counts_dict = {
            'A': 100,
            'B': 91,
            'C': 109
        }
        class_counts = [(k, v) for k, v in class_counts_dict.items()]  # total of 300 elements
        self.assertEqual([], get_sample_dataset(class_counts, 400))
        for n in [1, 200, 300]:
            sample = get_sample_dataset(class_counts, n)
            self.assertEqual(n, len(sample),
                             msg='Test case failed for sample size = {}'.format(n))
            for c, i in sample:
                # test to ensure returned sample only contains specified classes
                # and row indices are bounded within [0, #rows of the class)
                self.assertTrue(c in class_counts_dict and 0 <= i <= class_counts_dict[c])

    def test_find_markups(self):
        markups = StringHelper.find_markups('this is a <test> string <> to find <markups>. N is <= 10 or >= 20 >>><<< END!')
        self.assertEqual(['<test>', '<>', '<markups>', '<= 10 or >'], markups)

    def test_read_lines(self):
        lines = [line for line in FileHelper.read_lines('text_file_for_test.txt')]
        self.assertEqual(7, len(lines))
