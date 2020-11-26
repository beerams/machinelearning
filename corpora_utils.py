"""
Utility/helper functions to read corpora
"""
import codecs
import glob
import logging
import os
import uuid

from utils import ConfigHelper, get_sample_dataset

LOGGER = logging.getLogger('app.'+__name__)
CORPORA_CONFIG_SECTION: str = 'corpora'
STANFORD_MOVIE_REVIEW_URL: str = 'stanford_movie_review_dataset_url'
STANFORD_MOVIE_REVIEW_TRAIN_FILE_PATH: str = 'stanford_movie_review_train_file_path'
STANFORD_MOVIE_REVIEW_TEST_FILE_PATH: str = 'stanford_movie_review_test_file_path'
STANFORD_MOVIE_REVIEW_DEV_FILE_PATH: str = 'stanford_movie_review_dev_file_path'


def sample_stanford_imdb_dataset(train_size: int = 5000, dev_size: int = 1000, test_size: int = 5000):
    """
    Samples from 'Large Movie Review Dataset' and creates a smaller dataset for training, validation and testing
    The corpora is hosted at https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
    """
    # file paths
    # ensure data folder exists
    dataset_dir: str = ConfigHelper.get_config_value('dataset_dir')
    if os.path.exists(dataset_dir):
        if not os.path.isdir(dataset_dir):
            LOGGER.error("'%s' exists but is not a folder", dataset_dir)
    else:
        os.makedirs(dataset_dir)
    master_data_set_url: str = ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_URL, CORPORA_CONFIG_SECTION)
    temp_folder_path: str = ConfigHelper.get_config_value('temp_dir')
    temp_working_directory: str = '{}/{}'.format(temp_folder_path, str(uuid.uuid4()))
    raw_data_file_path = '{}/{}'.format(temp_working_directory, 'data.tar.gz')
    LOGGER.debug('Temp working directory: %s', temp_working_directory)
    LOGGER.debug('Data file path: %s', raw_data_file_path)
    LOGGER.debug('Stanford IMDB dataset URL: %s', master_data_set_url)

    # create local temp directory
    LOGGER.debug('Creating temp working directory')
    # os.makedirs(temp_working_directory)

    # download
    LOGGER.debug('Downloading %s and saving into %s', master_data_set_url, raw_data_file_path)
    # HttpHelper.download_file(master_data_set_url, raw_data_file_path)

    # unpack/extract
    LOGGER.debug('Unpacking %s', raw_data_file_path)
    # shutil.unpack_archive(raw_data_file_path, temp_working_directory)

    # temp_working_directory = 'temp/605867db-d277-4dd0-8921-e567bd684088'

    # collect training files for both positive and negative classes
    training_class_files: dict = {
        1: glob.glob('{}/**/train/**/pos/**/*.txt'.format(temp_working_directory), recursive=True),
        -1: glob.glob('{}/**/train/**/neg/**/*.txt'.format(temp_working_directory), recursive=True)
    }
    # collect test files for both positive and negative classes
    test_class_files: dict = {
        1: glob.glob('{}/**/test/**/pos/**/*.txt'.format(temp_working_directory), recursive=True),
        -1: glob.glob('{}/**/test/**/neg/**/*.txt'.format(temp_working_directory), recursive=True)
    }

    # sample from the population of train and test files, to create smaller datasets
    # indices collected below are indices to train/test file paths
    train_dev_indices: list = get_sample_dataset([(c, len(arr)) for c, arr in training_class_files.items()],
                                                 train_size+dev_size)
    train_indices: list = train_dev_indices[:train_size]
    dev_indices: list = train_dev_indices[train_size:]
    test_indices: list = get_sample_dataset([(c, len(arr)) for c, arr in test_class_files.items()],
                                            test_size)

    # read from sampled raw files and save to train/dev/test files
    train_file_path = ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TRAIN_FILE_PATH, CORPORA_CONFIG_SECTION)
    LOGGER.debug('Saving training dataset to %s', train_file_path)
    _save_dataset(train_file_path, train_indices, training_class_files)

    dev_file_path = ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_DEV_FILE_PATH, CORPORA_CONFIG_SECTION)
    LOGGER.debug('Saving dev dataset to %s', train_file_path)
    _save_dataset(dev_file_path, dev_indices, training_class_files)

    test_file_path = ConfigHelper.get_config_value(STANFORD_MOVIE_REVIEW_TEST_FILE_PATH, CORPORA_CONFIG_SECTION)
    LOGGER.debug('Saving test dataset to %s', train_file_path)
    _save_dataset(test_file_path, test_indices, test_class_files)


def _save_dataset(file_path: str, class_indices: list, class_files: dict):
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        for c, i in class_indices:
            sample_file_path = class_files[c][i]
            with codecs.open(sample_file_path, 'r', encoding='utf-8') as sf:
                f.write('{} {}\n'.format(c, sf.read()))
