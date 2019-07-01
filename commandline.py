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
    #getting and validating pattern
    pattern = args.r or args.regex
    is_ascii = lambda pattern: len(pattern) == len(pattern.encode())
    assert is_ascii(pattern=pattern), "ERROR IN PATTERN FORMAT VALIDATION Please provide a valid string(ASCII)"
    pattern = re.compile(pattern)

    #getting true/false on mutual excluded params
    color = args.color
    underscore = args.underscore
    machine = args.machine #not used in context of the function

    matches={}
    file_names = args.file or args.f
    for file_name in file_names:
        assert os.path.exists(file_name), "Error in validation of the path {} - PLEASE PROVIDE FULL PATH TO THE FILE".format(file_name)
        assert os.path.isfile(file_name), "Error in validation of the file {} is not a file - PLEASE PROVIDE VALID FILE".format(file_name)
        filetext = open(file_name, 'r')
        for line in filetext:
            match=re.search(pattern,line)
            if match:
                matches[match.start] = pattern.findall(line)

        filetext.close()
        #filetext = textfile.read()
        #textfile.close()
        #matches = re.findall(pattern, filetext)
        if color:
                #todo change the format, to print the line and color the mattching pattern
                print(Color.PURPLE + '\t'.join(matches))
        elif underscore:
                #todo ^pattern^
                print(Color.UNDERLINE + '\t'.join(matches))
        else:
            position = re.search(pattern, filetext)
            print("" + file_name + ":" + str(position.start()) + ":" + matches[0])


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
