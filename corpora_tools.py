#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

from corpora_utils import sample_stanford_imdb_dataset, get_stanford_imbd_vocabulary, \
    STANFORD_MOVIE_REVIEW_TRAIN_FILE_PATH, CORPORA_CONFIG_SECTION, STANFORD_MOVIE_REVIEW_DEV_FILE_PATH, \
    STANFORD_MOVIE_REVIEW_TEST_FILE_PATH, get_stanford_imdb_markup_vocabulary
from utils import ConfigHelper

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _sample_stanford_imdb_dataset():
    sample_stanford_imdb_dataset()


def _analyze_stanford_imdb_data():
    vocab: set = get_stanford_imbd_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TRAIN_FILE_PATH,
                                                                            CORPORA_CONFIG_SECTION))
    vocab.update(get_stanford_imbd_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_DEV_FILE_PATH,
                                                                            CORPORA_CONFIG_SECTION)))
    vocab.update(get_stanford_imbd_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TEST_FILE_PATH,
                                                                            CORPORA_CONFIG_SECTION)))
    for word in sorted(vocab):
        print(word)
    print('Vocabulary size: %s' % len(vocab))

    markup_vocab: set = get_stanford_imdb_markup_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TRAIN_FILE_PATH,
                                                                                          CORPORA_CONFIG_SECTION))
    markup_vocab.update(get_stanford_imdb_markup_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_DEV_FILE_PATH,
                                                                                          CORPORA_CONFIG_SECTION)))
    markup_vocab.update(get_stanford_imdb_markup_vocabulary(ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TEST_FILE_PATH,
                                                                                          CORPORA_CONFIG_SECTION)))
    for word in sorted(markup_vocab):
        print(word)
    print('Markup vocabulary size: %s' % len(markup_vocab))


def _main():
    valid_commands = {
        'sample-stanford-imdb': _sample_stanford_imdb_dataset,
        'analyze-stanford-imdb': _analyze_stanford_imdb_data,
    }
    cmd = sys.argv[1]
    if cmd in valid_commands:
        valid_commands[cmd]()
    else:
        raise Exception('Invalid command %s. Valid commands are %s' % (cmd, valid_commands.keys()))


if __name__ == '__main__':
    _main()
