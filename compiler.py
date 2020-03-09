import argparse
import sys

class LanguageDefinition:

    def __init__(self):
        self.variables = []
        self.constants = []
        self.predicates = {} # hash table (predicate -> arity)
        self.equality = ""
        self.and = ""
        self.or = ""
        self.implies = ""
        self.iff = ""
        self.neg = ""
        self.exists = ""
        self.forall = ""
        self.whitespace = [" ", "\n", "\t"]
        self.neccesary_chars = ["(", ")", ","]
        self.formula = ""

    def read_input(self, input_file_name):
        with open(input_file_name) as fh:
            lines = fh.read().splitlines()

        for line in lines:
            if line.startswith("variables"):
                line = line.replace("variables: ", "")
                line = line.split()
                for variable in line:
                    self.variables.append(variable)

            elif line.startswith("constants"):
                line = line.replace("constants: ", "")
                line = line.split()
                for constant in line:
                    self.constants.append(constant)

            elif line.startswith("predicates"):
                line = line.replace("predicates: ", "")
                line = line.split()
                for predicate in line:
                    predicate_name = ""
                    predicate_arity = ""
                    count = 0
                    while predicate[count] != '[':
                        predicate_name += predicate[count]
                        count += 1
                    count += 1
                    while predicate[count] != ']':
                        predicate_arity += predicate[count]
                        count += 1
                    self.predicates[predicate_name] = int(predicate_arity)

            elif line.startswith("equality"):
                line = line.replace("equality: ", "")
                if len(line) == 0:
                    # error
                    pass
                self.equality = line

            elif line.startswith("connectives"):
                line = line.replace("connectives: ", "")
                line = line.split()
                try:
                    self.and = line[0]
                    self.or = line[1]
                    self.implies = line[2]
                    self.iff = line[3]
                    self.neg = line[4]
                except:
                    #error
                    pass

            elif line.startswith("quantifiers"):
                line = line.replace("quantifiers: ", "")
                line = line.split()
                try:
                    self.exists = line[0]
                    self.forall = line[1]

            elif line.startswith("formula"):
                line = line.replace("formula: ", "")
                self.formula = line

class Grammar:

    def __init__(self, LanguageDefinition):
        self.terminals = set()
        self.non_terminals = set()
        self.productions = set()
        self.start_symbol = ""

        self.populate_terminals(LanguageDefiniton)

    def populate_terminals(self, LanguageDefinition):
        for variable in LanguageDefinition.variables:
            if variable in self.terminals():
                # error
                pass
            self.terminals.add(variable)
        for constant in LanguageDefinition.constants:
            if constant in self.terminals():
                # error
                pass
            self.termainals.add(constant)
        for predicate in LanguageDefinition.predicates.keys():
            if predicate in self.terminals():
                # error
                pass
            self.terminals.add(predicate)
        if LanguageDefinition.equality in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.equality)
        if LanguageDefinition.and in self.terminals():
            # error
            pass
        else:
            self.termianls.add(LanguageDefinition.and)
        if LanguageDefinition.or in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.or)
        if LanguageDefinition.implies in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.implies)
        if LanguageDefinition.iff in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.iff)
        if LanguageDefinition.neg in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.neg)
        if LanguageDefinition.exists in self.terminals():
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.exists)
        if LanguageDefinition.forall in self.terminals():
            #error
            pass
        else:
            self.terminals.add(LanguageDefinition.forall)
        for neccesary_char in LanguageDefinition.neccesary_chars():
            if neccesary_char in self.terminals():
                # error
                pass
            else:
                self.termainals.add(LanguageDefinition.neccesary_chars)




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
