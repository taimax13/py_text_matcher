#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import argparse
import datetime
import os.path
import re


#####
# meanwhile no usage for other then hardcoded params in this class,
# can be improved as a color choice
#####
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def is_ascii(pattern):
    """
    :param pattern:
    :validates: if pattern contains only ASCII regex symbols
    """
    assert len(pattern) == len(pattern.encode()), \
        "ERROR IN PATTERN FORMAT VALIDATION Please provide \
         a valid string(ASCII)"


def matcher(args):
    # getting and validating pattern
    pattern = args.r or args.regex
    is_ascii(pattern=pattern)
    pattern = re.compile(pattern)

    # getting true/false on mutual excluded params
    color = args.color
    underscore = args.underscore

    count_line = 0
    file_res = "matches.txt"
    file_names = args.file or args.f
    for file_name in file_names:
        assert os.path.exists(file_name), "Error in validation of the path {} \
         - PLEASE PROVIDE FULL PATH TO THE FILE".format(file_name)
        assert os.path.isfile(file_name), "Error in validation of  " \
                                          "the file {} is not a file  - \
                                          PLEASE PROVIDE VALID FILE" \
            .format(file_name)
        with open(file_res, 'w') as f:
            filetext = open(file_name, 'r')
            for line in filetext:
                count_line += 1
                if re.search(pattern, line):
                    f.write(file_name + ':' + str(count_line) + ':' + line)
        filetext.close()
        with open(file_res, 'r') as f:
            text = f.read()
            f.close()
        i = 0
        res = []
        if color:
            for m in pattern.finditer(text):
                res.append("" + Color.GREEN + text[i:m.start()]
                           + Color.PURPLE + text[m.start():m.end()])
                i = m.end()
        elif underscore:
            for m in pattern.finditer(text):
                res.append("" + text[i:m.start()] + "^"
                           + text[m.start():m.end()] + "^")
                i = m.end()
        else:
            # format: file_name:no_line:start_pos:matched_text
            for m in pattern.finditer(text):
                res.append("format:" + text[i:m.start()] +
                           "no_line:start_pos:" +
                           text[m.start():m.end()] + ":")
                i = m.end()
        print(' '.join(res))


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
