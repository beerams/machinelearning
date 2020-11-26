"""
Module for utility functions and helper classes
"""
import os
from configparser import ConfigParser, ExtendedInterpolation


class ConfigHelper:
    config: ConfigParser = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(os.environ.get('CONFIG_FILE_PATH', 'config.txt'))

    @classmethod
    def get_config_value(cls, key, section: str, default_value=None):
        return cls.config.get(section, key)
