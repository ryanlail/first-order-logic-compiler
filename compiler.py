import argparse
import sys

class LanguageDefinition:

    def __init__(self):
        self.variables = []
        self.constants = []
        self.predicates = [] #  2d array e.g. [[p,2],[q,1]]
        self.equality = ""
        self.connectives = []
        self.quantifiers = []
        self.formula = ""

    def read_input(self, input_file_name):
        with open(input_file_name) as fh:
            lines = fh.read().splitlines()

        #for line in lines:






def arg_parser():
    #  parse the arugments from the command line NOT the compiler parser
    parser = argparse.ArgumentParser(description="A Lexical Analyser & Parser for First-Order Logic")
    parser.add_argument("-i","--input_file_name", type = str, default = "example.txt", help = "Name of the input file to read language definitons and formula from")
   # parser.add_argument("parse_tree_file_name", type = str, default = "tree.png", help = "Name of the output parse tree")
   # parser.add_argument("log_file_name", type = str, default = "log.txt", help = "Name of the log file")

    return parser.parse_args()

def main():
    arguments = arg_parser()
    input_from_file = LanguageDefinition()
    input_from_file.read_input(arguments.input_file_name)

if __name__ == "__main__":
    main()
