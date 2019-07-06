import os
import re


class Color:
    """
    meanwhile no usage for other then hardcoded params in this class,
    can be improved as a color choice
    """
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


class ConstantsUsed:
    """
    name of the file , where intermediate result is stored
    """
    TEXT_FILE_NAME = "matches.txt"


class ResultPrinter:

    def __init__(self, filenames, pattern, color, underscore):
        self.parser = None
        self.pattern = pattern
        self.color = color
        self.underscore = underscore
        Printer.create_matched_result(filenames, self.pattern)

    def set_parser(self, parserObj):
        self.parser = parserObj

    def print(self):
        if self.color:
            self.set_parser(ColorPrinter())
            self.parser.print_res(pattern=self.pattern)

        elif self.underscore:
            self.set_parser(UnderscorePrinter())
            self.parser.print_res(pattern=self.pattern)
        else:
            self.set_parser(MachinePrinter())
            self.parser.print_res(pattern=self.pattern)


class Printer:
    res = []
    text = None
    i = 0

    @staticmethod
    def create_matched_result(file_names, pattern):
        """
            :param file_names:
            :param pattern:
            :stores: to the file line , line number if the pattern was found
            """
        count_line = 0
        for file_name in file_names:
            assert os.path.exists(file_name), "Error in validation \
            of the path {} - PLEASE PROVIDE FULL PATH TO THE FILE" \
                .format(file_name)
            assert os.path.isfile(file_name), "Error in validation of  " \
                                              "the file {} is not a file  - \
                                                  PLEASE PROVIDE VALID FILE" \
                .format(file_name)
            with open(ConstantsUsed.TEXT_FILE_NAME, 'w') as f:
                filetext = open(file_name, 'r')
                for line in filetext:
                    count_line += 1
                    if re.search(pattern, line):
                        f.write(file_name + ':' + str(count_line) + ':' + line)
            filetext.close()

    def read_res_file(self):
        with open(ConstantsUsed.TEXT_FILE_NAME, 'r') as f:
            self.text = f.read()
            f.close()

    def prepare_result(self, pattern):
        raise NotImplementedError("print_result method \
        must be define in subclass ")

    def print_res(self, pattern):
        self.read_res_file()
        self.prepare_result(pattern)
        print(' '.join(self.res))


class ColorPrinter(Printer):
    def prepare_result(self, pattern):
        for m in pattern.finditer(self.text):
            self.res.append("" + Color.GREEN + self.text[self.i:m.start()]
                            + Color.PURPLE + self.text[m.start():m.end()])
            self.i = m.end()


class UnderscorePrinter(Printer):
    def prepare_result(self, pattern):
        for m in pattern.finditer(self.text):
            self.res.append("" + self.text[self.i:m.start()] + "^"
                            + self.text[m.start():m.end()] + "^")
            self.i = m.end()


class MachinePrinter(Printer):
    def prepare_result(self, pattern):
        for m in pattern.finditer(self.text):
            self.res.append("format:" + self.text[self.i:m.start()] +
                            "no_line:start_pos:" + str(m.start()) + ":" +
                            self.text[m.start():m.end()] + ":")
            self.i = m.end()
