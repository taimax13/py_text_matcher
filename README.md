# py_text_matcher

Pre-requirements:
python@3

ASCII find the line in the file based on pattern.



Command Line Interface with Python using argparse
for more info please ref.here:
https://docs.python.org/3/library/argparse.html



Script, that searches for lines matching regular expression in file or files

Valid input is ASCII.

Script accept list optional parameters which are mutually exclusive:
-u ( --underscore ) which prints '^' under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine readable output
                  format: file_name:no_line:start_pos:matched_text


 
