import logging
import sys

from corpora_utils import sample_stanford_imdb_dataset

logging.basicConfig(level=logging.DEBUG)


def _main():
    cmd = sys.argv[1]
    if cmd == 'sample-stanford-imdb':
        sample_stanford_imdb_dataset()
    else:
        raise Exception('invalid command')


if __name__ == '__main__':
    _main()
