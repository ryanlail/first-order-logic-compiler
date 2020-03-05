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

    def read_input(self):
        input_file_name = sys.argv[1]

        with open(input_file_name) as fh:
            lines = fh.read().splitlines()






def main():
    input_from_file = input()
    input_from_file.read_input()

if __name__ == "__main__":
    main()
