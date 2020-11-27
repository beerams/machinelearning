"""
Module for utility functions and helper classes
"""
import os
import re
from configparser import ConfigParser, ExtendedInterpolation, NoOptionError, NoSectionError

import requests
from requests import Response
import logging
import random

LOGGER = logging.getLogger(__name__)


class ConfigHelper:
    """
    Helper class to read configurations from a file
    """
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


class HttpHelper:
    """
    Helper for HTTP operations
    """
    @classmethod
    def _http_get(cls, url, stream=False) -> Response:
        return requests.get(url, stream=stream)

    @classmethod
    def download_file(cls, url: str, local_file_path: str):
        with cls._http_get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)


class StringHelper:
    @classmethod
    def find_markups(cls, s: str):
        """
        Finds all substrings which form html (or even xml) markups
        Any substring that begins with < and ends with > is treated as a markup
        """
        return re.findall('<.*?>', s)


class FileHelper:
    @classmethod
    def read_lines(cls, file_path: str):
        """
        Reads one line at a time and yields the same
        """
        with open(file_path, 'r', encoding="utf-8") as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                yield line


def get_sample_dataset(class_counts: list, sample_size: int) -> list:
    """
    Given number of rows (usually files) per class, randomize uniformly and select required number of rows. Return
    a list of tuples, each tuple containing the class and row index

    Uniform distribution is used to ensure sample selected is representative of class population.

    required_size must be <= sum of all rows across all classes. Returns an empty list if this condition is not met.

    Typical use case:
    You have a bunch of files or an array of data for each class, imagine you are building a classification task.
    Imagine there are 1000 rows for class A, 1100 for class B, and 1200 for class C, a total of 3300 rows
    You want to select 1500 rows randomly across all classes.
    Call this function with an array of tuples [('A', 1000), ('B', 1100), ('C', 1200)] and required sample size = 1500
    This function returns a list of tuples, each tuple is of the form (<class name/id>, row index).
    Example: [('A', 501), ('A', 943), ('C', 89), .... ]

    class_counts: a list of tuples of the form (<class name/id>, count of rows)
    required_size: no. of rows required
    """
    population_size = sum(n for _, n in class_counts)
    if population_size < sample_size:
        LOGGER.error('Sample size %s is greater than the population size %s', sample_size, population_size)
        return []
    class_indices = [(c, i) for c, n in class_counts for i in range(n)]
    random.shuffle(class_indices)
    return class_indices[0:sample_size]
