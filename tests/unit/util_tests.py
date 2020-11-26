import unittest

from utils import ConfigHelper


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
