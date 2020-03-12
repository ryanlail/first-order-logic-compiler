from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph
from anytree.exporter import UniqueDotExporter
import argparse
import sys
import re

class LanguageDefinition:

    def __init__(self):
        self.variables = []
        self.constants = []
        self.predicates = {} # hash table (predicate -> arity)
        self.equality = ""
        self.and_ = ""
        self.or_ = ""
        self.implies = ""
        self.iff = ""
        self.neg = ""
        self.exists = ""
        self.forall = ""
        self.whitespace = [" ", "\n", "\t"]
        self.neccesary_chars = ["(", ")", ","]
        self.formula = ""

    def read_input(self, input_file_name, log_file):
        with open(input_file_name) as fh:
            lines = fh.read().splitlines()

        for line in lines:
            if line.startswith("variables: "): # only if there ARE vars defined (via the space)
                line = line.replace("variables: ", "")
                line = line.split()
                for variable in line:
                    for char in variable:
                        if not(char.isalnum()) and char != "_":
                            with open(log_file, "a") as fh:
                                fh.write("ERROR reading in file: \n VARIABLE " + variable + " contains invalid character " + char)
                                sys.exit(1)
                    if variable in self.variables or variable in self.constants or variable in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n VARIABLE " + variable + " is a repeated identifier")
                        sys.exit(1)
                    elif variable == self.equality or variable == self.and_ or variable == self.or_ or variable == self.implies or variable == self.iff or variable == self.neg or variable == self.exists or variable == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n VARIABLE" + variable + " is a reserved string with input language")
                            sys.exit(1)
                    self.variables.append(variable)

            elif line.startswith("constants: "):
                line = line.replace("constants: ", "")
                line = line.split()
                for constant in line:
                    for char in constant:
                        if not(char.isalnum()) and char != "_":
                            with open(log_file, "a") as fh:
                                fh.write("ERROR reading in file: \n CONSTANT " + constant + " contains invalid character " + char)
                                sys.exit(1)
                    if constant in self.variables or constant in self.constants or constant in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n CONSTANT " + constant + " is a repeated identifier")
                            sys.exit(1)
                    elif constant == self.equality or constant == self.and_ or constant == self.or_ or constant == self.implies or constant == self.iff or constant == self.neg or constant == self.exists or constant == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n CONSTANT" + constant + " is a reserved string with input language")
                            sys.exit(1)
                    self.constants.append(constant)

            elif line.startswith("predicates: "):
                line = line.replace("predicates: ", "")
                line = line.split()
                for predicate in line:
                    predicate_name = ""
                    predicate_arity = ""
                    count = 0
                    try:
                        while predicate[count] != '[':
                            predicate_name += predicate[count]
                            if not(predicate[count].isalnum()) and predicate[count] != "_":
                                with open(log_file, "a") as fh:
                                    fh.write("ERROR reading in file: \n PREDICATE starting " + predicate_name + " contains inalid character " + predicate[count])
                                    sys.exit(1)
                            count += 1
                        count += 1
                        if predicate_name in self.variables or predicate_name in self.constants or predicate_name in self.predicates.keys():
                            with open(log_file, "a") as fh:
                                fh.write("ERROR reading in file: \n PREDICATE " + predicate + " is a repeated identifier")
                            sys.exit(1)

                        elif predicate_name == self.equality or predicate_name == self.and_ or predicate_name == self.or_ or predicate_name == self.implies or predicate_name == self.iff or predicate_name == self.neg or predicate_name == self.exists or predicate_name == self.forall:
                            with open(log_file, "a") as fh:
                                fh.write("ERROR reading in file: \n PREDICATE" + predicate_name + " is a reserved string with input language")
                                sys.exit(1)
                        while predicate[count] != ']':
                            predicate_arity += predicate[count]
                            count += 1
                        try:
                            self.predicates[predicate_name] = int(predicate_arity)
                        except:
                            with open(log_file, "a") as fh:
                                fh.write("ERROR reading in file: \n PREDICATE " + predicate_name + " arity is not a number")
                                sys.exit(1)
                    except:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n PREDICATE definition is malformed! Must follow format:  Predicate_Name[arity]")
                            sys.exit(1)

            elif line.startswith("equality:"):
                line = line.replace("equality: ", "")
                if len(line.split()) != 1:
                    with open(log_file, "a") as fh:
                        fh.write("ERROR reading in file: \n Expected 1 equality symbol, recieved " + str(len(line.split())))
                elif line in self.variables or line in self.constants or line in self.predicates.keys():
                    with open(log_file, "a") as fh:
                        fh.write("ERROR reading in file: \n Symbol " + line + " is a reserved string with input language")
                        sys.exit(1)
                elif line == self.and_ or line == self.or_ or line  == self.implies or line == self.iff or line == self.neg or line == self.exists or line == self.forall:
                    with open(log_file, "a") as fh:
                        fh.write("ERROR reading in file: \n EQUALITY " + line + " is already a different reserved string")
                        sys.exit(1)
                else:
                    self.equality = line

            elif line.startswith("connectives"):
                line = line.replace("connectives: ", "")
                line = line.split()
                if len(line) == 5:
                    self.and_ = line[0]
                    if self.and_ in self.variables or self.and_ in self.constants or self.and_ in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.and_ + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.and_ == self.equality or self.and_ == self.or_ or self.and_  == self.implies or self.and_ == self.iff or self.and_ == self.neg or self.and_ == self.exists or self.and_ == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n AND " + self.and_ + " is already a different reserved string")
                            sys.exit(1)
                    self.or_ = line[1]
                    if self.or_ in self.variables or self.or_ in self.constants or self.or_ in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.or_ + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.or_ == self.equality or self.and_ == self.or_ or self.or_  == self.implies or self.or_ == self.iff or self.or_ == self.neg or self.or_ == self.exists or self.or_ == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n OR " + self.and_ + " is already a different reserved string")
                            sys.exit(1)
                    self.implies = line[2]
                    if self.implies in self.variables or self.implies in self.constants or self.implies in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.implies + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.implies == self.equality or self.implies == self.or_ or self.and_  == self.implies or self.implies == self.iff or self.implies == self.neg or self.implies == self.exists or self.implies == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n IMPLIES " + self.implies + " is already a different reserved string")
                            sys.exit(1)
                    self.iff = line[3]
                    if self.iff in self.variables or self.iff in self.constants or self.iff in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.iff + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.iff == self.equality or self.iff == self.or_ or self.iff  == self.implies or self.and_ == self.iff or self.iff == self.neg or self.iff == self.exists or self.iff == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n IFF " + self.iff + " is already a different reserved string")
                            sys.exit(1)
                    self.neg = line[4]
                    if self.neg in self.variables or self.neg in self.constants or self.neg in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.neg + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.neg == self.equality or self.neg == self.or_ or self.neg  == self.implies or self.neg == self.iff or self.and_ == self.neg or self.neg == self.exists or self.neg == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n NEG " + self.neg + " is already a different reserved string")
                            sys.exit(1)
                else:
                    with open(log_file, "w") as fh:
                        fh.write("ERROR reading in file: \n Expected 5 connectives, recieved " + str(len(line)))

            elif line.startswith("quantifiers"):
                line = line.replace("quantifiers: ", "")
                line = line.split()
                if len(line) == 2:
                    self.exists = line[0]
                    if self.exists in self.variables or self.exists in self.constants or self.exists in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.exists + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.exists == self.equality or self.exists == self.or_ or self.exists  == self.implies or self.exists == self.iff or self.exists == self.neg or self.and_ == self.exists or self.exists == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n EXISTS " + self.exists + " is already a different reserved string")
                            sys.exit(1)
                    self.forall = line[1]
                    if self.forall in self.variables or self.forall in self.constants or self.forall in self.predicates.keys():
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n Symbol " + self.forall + " is a reserved string with input language")
                            sys.exit(1)
                    elif self.forall == self.equality or self.forall == self.or_ or self.forall  == self.implies or self.forall == self.iff or self.forall == self.neg or self.forall == self.exists or self.and_ == self.forall:
                        with open(log_file, "a") as fh:
                            fh.write("ERROR reading in file: \n FORALL " + self.forall + " is already a different reserved string")
                            sys.exit(1)
                else:
                    with open(log_file, "w") as fh:
                        fh.write("ERROR reading in file: \n Expected 2 quantifiers, recieved " + str(len(line)))

            elif line.startswith("formula"):
                line = line.replace("formula: ", "")
                self.formula = line

            else:
                # must still be part of formula
                self.formula += line

class Grammar:

    def __init__(self, LanguageDefinition):
        self.terminals = set()
        self.non_terminals = {"<VARIABLES>", "<CONSTANTS>", "<CONNECTIVES>",
                "<QUANTIFIERS>", "<PREDICATE>", "<EQUALITY>", "<VAR_CON>",
                "<LOGIC>", "<FORMULA>", "<QUANTIFICATION>"}
        self.productions = []
        self.start_symbol = "<FORMULA>"

        self.populate_terminals(LanguageDefinition)
        self.populate_productions(LanguageDefinition)

    def populate_terminals(self, LanguageDefinition):
        for variable in LanguageDefinition.variables:
            if variable in self.terminals:
                # error
                pass
            self.terminals.add(variable)
        for constant in LanguageDefinition.constants:
            if constant in self.terminals:
                # error
                pass
            self.terminals.add(constant)
        for predicate in LanguageDefinition.predicates.keys():
            if predicate in self.terminals:
                # error
                pass
            self.terminals.add(predicate)
        if LanguageDefinition.equality in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.equality)
        if LanguageDefinition.and_ in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.and_)
        if LanguageDefinition.or_ in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.or_)
        if LanguageDefinition.implies in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.implies)
        if LanguageDefinition.iff in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.iff)
        if LanguageDefinition.neg in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.neg)
        if LanguageDefinition.exists in self.terminals:
            # error
            pass
        else:
            self.terminals.add(LanguageDefinition.exists)
        if LanguageDefinition.forall in self.terminals:
            #error
            pass
        else:
            self.terminals.add(LanguageDefinition.forall)
        for neccesary_char in LanguageDefinition.neccesary_chars:
            if neccesary_char in self.terminals:
                # error
                pass
            else:
                self.terminals.add(neccesary_char)

    def populate_productions(self, LanguageDefinition):
        self.productions.append("<FORMULA> -> <QUANTIFICATION> | <LOGIC> | <EQUALITY> | <PREDICATE>")
        self.productions.append("<QUANTIFICATION> -> <QUANTIFIERS> <VARIABLES> <FORMULA>")
        self.productions.append("<LOGIC> -> (<FORMULA> <CONNECTIVES> <FORMULA>) | " + LanguageDefinition.neg +
                " <FORMULA>")
        self.productions.append("<EQUALITY> -> (<VAR_CON> " + LanguageDefinition.equality + " <VAR_CON>)")

        predicate_rule = "<PREDICATE> -> "
        for predicate in LanguageDefinition.predicates.keys():
            predicate_rule += predicate + "("
            for arity in range(LanguageDefinition.predicates[predicate]):
                predicate_rule += "<VARIABLES>, "
            predicate_rule = predicate_rule[:-2]
            predicate_rule += ") | "
        self.productions.append(predicate_rule[:-2])

        self.productions.append("<VAR_CON> -> <VARIABLES> | <CONSTANTS>")
        self.productions.append("<QUANTIFIERS> -> " + LanguageDefinition.exists + " | " +
                LanguageDefinition.forall)
        self.productions.append("<CONNECTIVES> -> " + LanguageDefinition.and_ + " | " + LanguageDefinition.or_ +
                " | " + LanguageDefinition.implies + " | " + LanguageDefinition.iff)

        constants_rule = "<CONSTANTS> -> "
        for constant in LanguageDefinition.constants:
            constants_rule += constant + " | "
        self.productions.append(constants_rule[:-2])

        variables_rule = "<VARIABLES> -> "
        for variable in LanguageDefinition.variables:
            variables_rule += variable + " | "
        self.productions.append(variables_rule[:-2])

    def output(self, file_name):
        with open(file_name, "w") as fh:
            terminal_output = ""
            terminal_output += "Terminal Symbols: {"
            for terminal in self.terminals:
                terminal_output += terminal + ", "
            terminal_output = terminal_output[:-2]
            terminal_output += "}\n"
            fh.write(terminal_output)
            fh.write("Non-terminal Symbols: " + str(self.non_terminals) + "\n")
            fh.write("Production Rules: \n")
            for rule in self.productions:
                fh.write(rule + "\n")
            fh.write("Start Symbol: " + self.start_symbol + "\n")

class Compiler():

    def __init__(self, LanguageDefinition, parse_tree_name, log_file):
        self.LanguageDefinition = LanguageDefinition
        self.lexeme_stream = LanguageDefinition.formula
        self.symbol_table = []
        self.tokens = [] # 2d array, token and id
        self.recursion_stack = []

        self.sanatized_stream = self.sanatize_stream(LanguageDefinition)
        self.tokenize(LanguageDefinition)
        self.analysis(parse_tree_name, log_file)

        #for pre, fill, node in RenderTree(self.recursion_stack[0]):
        #    print("%s%s" % (pre, node.name))

        #UniqueDotExporter(self.recursion_stack[0]).to_picture(parse_tree_name)

    def sanatize_stream(self, LanguageDefinition):
        for whitespace in LanguageDefinition.whitespace:
            self.lexeme_stream = self.lexeme_stream.replace(whitespace, " ")
        self.lexeme_stream = self.lexeme_stream.replace("(", " ( ")
        self.lexeme_stream = self.lexeme_stream.replace(")", " ) ")
        self.lexeme_stream = self.lexeme_stream.replace(",", " , ")
        return self.lexeme_stream.split()

    def tokenize(self, LanguageDefinition):
        for lexeme in self.sanatized_stream:
            if lexeme in LanguageDefinition.variables:
                self.tokens.append(["<VARIABLES>", len(self.symbol_table)])
                self.symbol_table.append(lexeme)
            elif lexeme in LanguageDefinition.constants:
                self.tokens.append(["<CONSTANTS>", len(self.symbol_table)])
                self.symbol_table.append(lexeme)
            elif lexeme == LanguageDefinition.equality:
                self.tokens.append(["<EQUALITY>"])
            elif (lexeme == LanguageDefinition.and_) or (lexeme == LanguageDefinition.or_) or (lexeme ==
                    LanguageDefinition.implies) or (lexeme == LanguageDefinition.iff):
                self.tokens.append(["<CONNECTIVES>", len(self.symbol_table)])
                self.symbol_table.append(lexeme)
            elif lexeme == LanguageDefinition.neg:
                self.tokens.append(["<NEG>"])
            elif lexeme == LanguageDefinition.exists or lexeme == LanguageDefinition.forall:
                self.tokens.append(["<QUANTIFIERS>", len(self.symbol_table)])
                self.symbol_table.append(lexeme)
            else:
                self.tokens.append([lexeme])

    def analysis(self, parse_tree_name, log_file):
        self.lookahead = 0
        if self.formula(None):
            UniqueDotExporter(self.recursion_stack[0]).to_picture(parse_tree_name)
            with open(log_file, "a") as fh:
                fh.write("PASS\n")

    def formula(self, caller):
        self.recursion_stack.append(Node("<FORMULA>", parent = caller))
        current = self.recursion_stack[-1]
        if self.quantification(current):
            return True
        elif self.logic(current):
            return True
        elif self.equality(current):
            return True
        elif self.predicate(current):
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def quantification(self, caller):
        self.recursion_stack.append(Node("<QUANTIFICATION>", parent = caller))
        current = self.recursion_stack[-1]
        if self.quantifiers(current) and self.variables(current) and self.formula(current):
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def logic(self, caller):
        self.recursion_stack.append(Node("<LOGIC>", parent = caller))
        current = self.recursion_stack[-1]
        if self.tokens[self.lookahead][0] == "(" and (self.tokens[self.lookahead + 2][0] != "<EQUALITY>"): # must look a head to check not equality
            self.recursion_stack.append(Node("(", parent = current))
            self.lookahead += 1
            if self.formula(current) and self.connectives(current) and self.formula(current):
                if self.tokens[self.lookahead][0] == ")":
                    self.recursion_stack.append(Node( ")", parent = current))
                    self.lookahead += 1
                    return True
        elif self.tokens[self.lookahead][0] == "<NEG>":
            self.recursion_stack.append(Node(re.escape(self.LanguageDefinition.neg), parent = self.recursion_stack[-1]))
            self.lookahead += 1
            if self.formula(current):
                return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def equality(self, caller):
        self.recursion_stack.append(Node("<EQUALITY>", parent = caller))
        current = self.recursion_stack[-1]
        if self.tokens[self.lookahead][0] == "(":
            self.recursion_stack.append(Node("(", parent = current))
            self.lookahead += 1
            if self.var_con(current):
                if self.tokens[self.lookahead][0] == "<EQUALITY>" :
                    self.recursion_stack.append(Node(re.escape(self.LanguageDefinition.equality), parent = current))
                    self.lookahead += 1
                    if self.var_con(current):
                        if self.tokens[self.lookahead][0] == ")":
                            self.recursion_stack.append(Node(")", parent = current))
                            self.lookahead += 1
                            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def predicate(self, caller):
        self.recursion_stack.append(Node("<PREDICATE>", parent = caller))
        current = self.recursion_stack[-1]
        if self.tokens[self.lookahead][0] in self.LanguageDefinition.predicates.keys():
            self.recursion_stack.append(Node(re.escape(self.tokens[self.lookahead][0]), parent = self.recursion_stack[-1]))
            arity = self.LanguageDefinition.predicates[self.tokens[self.lookahead][0]]
            self.lookahead += 1
            if self.tokens[self.lookahead][0] == "(":
                self.recursion_stack.append(Node("(", parent = current))
                self.lookahead += 1
                for i in range(arity - 1):
                    if self.variables(current):
                        if self.tokens[self.lookahead][0] == ",":
                            self.recursion_stack.append(Node(",", parent = current))
                            self.lookahead += 1
                        else:
                            self.recursion_stack.pop().parent = None
                            return False
                    else:
                        self.recursion_stack.pop()
                        return False
                if self.variables(current):
                    if self.tokens[self.lookahead][0] == ")":
                        self.recursion_stack.append(Node(")", parent = current))
                        self.lookahead += 1
                        return True
                    else:
                        self.recursion_stack.pop().parent = None
                        return False
                else:
                    self.recursion_stack.pop().parent = None
                    return False

    def var_con(self, caller):
        self.recursion_stack.append(Node("<VAR_CON>", parent = caller))
        current = self.recursion_stack[-1]
        if self.variables(current) or self.constants(current):
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def quantifiers(self, caller):
        self.recursion_stack.append(Node("<QUANTIFIERS>", parent = caller))
        if self.tokens[self.lookahead][0] == "<QUANTIFIERS>":
            self.recursion_stack.append(Node(re.escape(self.symbol_table[self.tokens[self.lookahead][1]]), parent = self.recursion_stack[-1]))
            self.lookahead += 1
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def connectives(self, caller):
        self.recursion_stack.append(Node("<CONNECTIVES>", parent = caller))
        if self.tokens[self.lookahead][0] == "<CONNECTIVES>":
            self.recursion_stack.append(Node(re.escape(self.symbol_table[self.tokens[self.lookahead][1]]), parent = self.recursion_stack[-1]))
            self.lookahead += 1
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def constants(self, caller):
        self.recursion_stack.append(Node("<CONSTANTS>", parent = caller))
        if self.tokens[self.lookahead][0] == "<CONSTANTS>":
            self.recursion_stack.append(Node(re.escape(self.symbol_table[self.tokens[self.lookahead][1]]), parent = self.recursion_stack[-1]))
            self.lookahead += 1
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False

    def variables(self, caller):
        self.recursion_stack.append(Node("<VARIABLES>", parent = caller))
        if self.tokens[self.lookahead][0] == "<VARIABLES>":
            self.recursion_stack.append(Node(re.escape(self.symbol_table[self.tokens[self.lookahead][1]]), parent = self.recursion_stack[-1]))
            self.lookahead += 1
            return True
        else:
            self.recursion_stack.pop().parent = None
            return False


def arg_parser():
    #  parse the arugments from the command line NOT the compiler parser
    parser = argparse.ArgumentParser(description="A Lexical Analyser & Parser for First-Order Logic")
    parser.add_argument("-i","--input_file_name", type = str, default = "example.txt",
            help = "Name of the input file to read language definitons and formula from")
    parser.add_argument("-g", "--grammar_file_name", type = str, default = "grammar.txt",
            help = "Name of the output file for the definition of the grammar")
    parser.add_argument("-t", "--parse_tree_file_name", type = str, default = "tree.png", help = "Name of the output parse tree (png)")
    parser.add_argument("-l", "--log_file_name", type = str, default = "log.txt", help = "Name of the log file")

    return parser.parse_args()

def main():
    arguments = arg_parser()
    with open(arguments.log_file_name, "w") as fh:
        fh.write("Log file for input: " + arguments.input_file_name + "\n")
    input_from_file = LanguageDefinition()
    input_from_file.read_input(arguments.input_file_name, arguments.log_file_name)
    new_grammar = Grammar(input_from_file)
    new_grammar.output(arguments.grammar_file_name)
    parse = Compiler(input_from_file, arguments.parse_tree_file_name, arguments.log_file_name)

if __name__ == "__main__":
    main()
