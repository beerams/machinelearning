"""
Module for utility functions and helper classes
"""
import os
from configparser import ConfigParser, ExtendedInterpolation, NoOptionError, NoSectionError


class ConfigHelper:
    config: ConfigParser = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(os.environ.get('CONFIG_FILE_PATH', 'config.txt'))

    @classmethod
    def get_config_value(cls, key, section: str = 'DEFAULT', default_value=None):
        try:
            return cls.config.get(section, key)
        except NoOptionError:
            return default_value
        except NoSectionError:
            return default_value
