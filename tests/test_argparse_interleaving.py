import sys
from unittest import mock

import gptdiff.gptdiff as gptdiff


def parse(argv):
    with mock.patch.object(sys, 'argv', argv):
        return gptdiff.parse_arguments()


def test_apply_after_file():
    args = parse(['gptdiff', 'prompt', 'file.js', '--apply'])
    assert args.apply is True
    assert args.files == ['file.js']


def test_apply_before_file():
    args = parse(['gptdiff', 'prompt', '--apply', 'file.js'])
    assert args.apply is True
    assert args.files == ['file.js']
