#!/usr/bin/env python
from __future__ import absolute_import
import argparse
import re
import os
import sys

current_path = os.path.abspath('.')
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)
os.environ.setdefault('ResultPrinter', 'result_printer')


def is_ascii(pattern):
    """
    :param pattern:
    :validates: if pattern contains only ASCII regex symbols
    """
    assert len(pattern) == len(pattern.encode()), \
        "ERROR IN PATTERN FORMAT VALIDATION Please provide \
         a valid string(ASCII)"


def matcher(args_input):
    pattern = args_input.r or args_input.regex
    is_ascii(pattern=pattern)

    pattern = re.compile(pattern)

    color = args_input.color
    underscore = args_input.underscore

    file_names = args_input.file or args_input.f

    from src.result_helper.result_printer import ResultPrinter
    result_printer = ResultPrinter(filenames=file_names, color=color,
                                   underscore=underscore, pattern=pattern)
    result_printer.print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("This is the parser for \
    search of a pattern in file/s")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--underscore', action='store_true')
    group.add_argument('-c', '--color', action='store_true')
    group.add_argument('-m', '--machine', action='store_true')

    parser.add_argument('-r', '-regex', type=str,
                        help='patter expression to look into the file',
                        required=True)

    parser.add_argument('-f', '--file', type=str, nargs="+",
                        help='File/s name to look for the pattern',
                        required=True)

    args = parser.parse_args()
    matcher(args)
