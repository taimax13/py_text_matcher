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
              
to emphasise the pattern I took https://www.saltycrane.com/blog/2007/10/using-pythons-finditer-to-highlight/ 
as an example

To run the script from terminal please use the following format:
                  
python commandline.py  -r "< pattern >" -f "<path-to-file/s>" -m |-c |-u

two files  example:

python commandline.py  -r "pattern" -f "path-to/test_file" "path-to/test_file1"  -c | -m | -u











 
