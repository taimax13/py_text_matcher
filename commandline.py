#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import argparse
import os.path
import re


#####
### meanwhile no usage for other then hardcoaded params in this class, can be improved as a coloe choice
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


def matcher(args):
    # getting and validating pattern
    pattern = args.r or args.regex
    is_ascii = lambda pattern: len(pattern) == len(pattern.encode())
    assert is_ascii(pattern=pattern), "ERROR IN PATTERN FORMAT VALIDATION Please provide a valid string(ASCII)"
    pattern = re.compile(pattern)

    # getting true/false on mutual excluded params
    color = args.color
    underscore = args.underscore
    machine = args.machine  # not used in context of the function

    matches = {}
    count_line=0
    file_res="matches.txt"
    file_names = args.file or args.f
    for file_name in file_names:
        assert os.path.exists(file_name), "Error in validation of the path {} - PLEASE PROVIDE FULL PATH TO THE FILE".format(file_name)
        assert os.path.isfile(file_name), "Error in validation of the file {} is not a file - PLEASE PROVIDE VALID FILE".format(file_name)
        with open(file_res, 'w') as f:
            filetext = open(file_name, 'r')
            for line in filetext:
                count_line+=1
                if re.search(pattern, line):
                    f.write(file_name+':'+str(count_line)+':'+line) #it is possible to avoid this step and cut/print right away from given target, but I prefer to work with already filtered stuff
        filetext.close()
        with open(file_res, 'r') as f:
            text = f.read()
            f.close()
        if color:
            i=0
            for m in pattern.finditer(text):
                print (""+Color.GREEN + text[i:m.start()] + Color.PURPLE + text[m.start():m.end()])
                i = m.end()
        elif underscore:
            i = 0
            for m in pattern.finditer(text):
                print("" + text[i:m.start()] + "^" + text[m.start():m.end()] + "^")
                i = m.end()
        else:
            #timestamp,target,type,data...
            i = 0
            for m in pattern.finditer(text):
                print("" + text[i:m.start()] + ":" + text[m.start():m.end()] + ":")
                i = m.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("This is the parser for search of a pattern in file/s")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--underscore', action='store_true')
    group.add_argument('-c', '--color', action='store_true')
    group.add_argument('-m', '--machine', action='store_true')

    parser.add_argument('-r', '-regex', type=str,
                        help='patter expression to look into the file', required=True)

    parser.add_argument('-f', '--file', type=str, nargs="+",
                        help='File/s name to look for the pattern', required=True)

    args = parser.parse_args()
    matcher(args)
