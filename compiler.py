from anytree import Node, RenderTree
import argparse
import sys

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
                    self.and_ = line[0]
                    self.or_ = line[1]
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
                except:
                    # error
                    pass

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
                "<QUANTIFIERS>", "<PREDICATE>", "<ASSIGNMENT>", "<VAR_CON>",
                "<LOGIC>", "<FORMULA>", "<QUANTIFICATION>"}
        self.productions = []
        self.start_symbol = "<FORMULA>"
#        self.transition_graph = nx.Graph()

        self.populate_terminals(LanguageDefinition)
        self.populate_productions(LanguageDefinition)
#        self.populate_tree()

#    def populate_tree(self):
#        self.transition_graph.add_nodes_from(list(self.non_terminals))
#        self.transition_graph.add_edge("<FORMULA>", "<QUANTIFICATION>")
#        self.transition_graph.add_edge("<FORMULA>", "<LOGIC>")
#        self.transition_graph.add_edge("<FORMULA>", "<ASSIGNMENT>")
#        self.transition_graph.add_edge("<FORMULA>", "<PREDICATE>")
#        self.transition_graph.add_edge("<QUANTIFICATION>", "<QUANTIFIERS>")
#        self.transition



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
        self.productions.append("<FORMULA> -> <QUANTIFICATION> | <LOGIC> | <ASSIGNMENT> | <PREDICATE>")
        self.productions.append("<QUANTIFICATION> -> <QUANTIFIERS> <VARIABLES> <FORMULA>")
        self.productions.append("<LOGIC> -> (<FORMULA> <CONNECTIVES> <FORMULA>) | " + LanguageDefinition.neg +
                " <FORMULA>")
        self.productions.append("<ASSIGNMENT> -> (<VAR_CON> " + LanguageDefinition.equality + " <VAR_CON>)")

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

    def __init__(self, LanguageDefinition):
        self.LanguageDefinition = LanguageDefinition
        self.lexeme_stream = LanguageDefinition.formula
        self.symbol_table = []
        self.tokens = [] # 2d array, token and id
        self.recursion_stack = []

        self.sanatized_stream = self.sanatize_stream(LanguageDefinition)
        self.tokenize(LanguageDefinition)
        self.analysis()
       # print(self.tokens)

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

    def analysis(self):
        root = Node("<FORMULA>")
        self.lookahead = 0
        print(self.formula())

    def formula(self):
        self.recursion_stack.append("<FORMULA>")
        if self.quantification():
            return True
        elif self.logic():
            return True
        elif self.assignment():
            return True
        elif self.predicate():
            return True
        else:
            return False

    def quantification(self):
        self.recursion_stack.append("<QUANTIFICATION>")
        if self.quantifiers() and self.variables() and self.formula():
            return True

    def logic(self):
        self.recursion_stack.append("<LOGIC>")
        if self.tokens[self.lookahead][0] == "(":
            self.lookahead += 1
            if self.formula() and self.connectives() and self.formula():
                if self.tokens[self.lookahead][0] == ")":
                    self.lookahead += 1
                    return True
        elif self.tokens[self.lookahead][0] == "<NEG>":
            self.lookahead += 1
            if self.formula():
                return True
        else:
            return False

    def assignment(self):
        self.recursion_stack.append("<ASSINGMENT>")
        if self.tokens[self.lookahead][0] == "(":
            self.lookahead += 1
            if self.var_con():
                if self.tokens[self.lookahead][0] == "<EQUALITY>" :
                    self.lookahead += 1
                    if self.var_con():
                        if self.tokens[self.lookahead][0] == ")":
                            self.lookahead += 1
                            return True
        else:
            return False

    def predicate(self):
        self.recursion_stack.append("<PREDICATE>")
        if self.tokens[self.lookahead][0] in self.LanguageDefinition.predicates.keys():
            arity = self.LanguageDefinition.predicates[self.tokens[self.lookahead][0]]
            self.lookahead += 1
            if self.tokens[self.lookahead][0] == "(":
                self.lookahead += 1
                for i in range(arity - 1):
                    if self.variables():
                        if self.tokens[self.lookahead][0] == ",":
                            self.lookahead += 1
                        else:
                            return False
                    else:
                        return False
                if self.variables():
                    if self.tokens[self.lookahead][0] == ")":
                        self.lookahead += 1
                        return True

    def var_con(self):
        self.recursion_stack.append("<VAR_CON>")
        if self.variables() or self.constants():
            return True
        else:
            return False

    def quantifiers(self):
        self.recursion_stack.append("<QUANTIFIERS>")
        if self.tokens[self.lookahead][0] == "<QUANTIFIERS>":
            print(self.symbol_table[self.tokens[self.lookahead][1]])
            self.lookahead += 1
            return True
        else:
            return False

    def connectives(self):
        self.recursion_stack.append("<CONNECTIVES>")
        if self.tokens[self.lookahead][0] == "<CONNECTIVES>":
            self.lookahead += 1
            return True
        else:
            return False

    def constants(self):
        self.recursion_stack.append("<CONSTANTS>")
        if self.tokens[self.lookahead][0] == "<CONSTANTS>":
            self.lookahead += 1
            return True
        else:
            return False

    def variables(self):
        self.recursion_stack.append("<VARIABLES>")
        if self.tokens[self.lookahead][0] == "<VARIABLES>":
            self.lookahead += 1
            return True
        else:
            return False


def arg_parser():
    #  parse the arugments from the command line NOT the compiler parser
    parser = argparse.ArgumentParser(description="A Lexical Analyser & Parser for First-Order Logic")
    parser.add_argument("-i","--input_file_name", type = str, default = "example.txt",
            help = "Name of the input file to read language definitons and formula from")
    parser.add_argument("-g", "--grammar_file_name", type = str, default = "grammar.txt",
            help = "Name of the output file for the definition of the grammar")
   # parser.add_argument("parse_tree_file_name", type = str, default = "tree.png", help = "Name of the output parse tree")
   # parser.add_argument("log_file_name", type = str, default = "log.txt", help = "Name of the log file")

    return parser.parse_args()

def main():
    arguments = arg_parser()
    input_from_file = LanguageDefinition()
    input_from_file.read_input(arguments.input_file_name)
    new_grammar = Grammar(input_from_file)
    new_grammar.output(arguments.grammar_file_name)
    lexial_analysis = Compiler(input_from_file)


if __name__ == "__main__":
    main()
