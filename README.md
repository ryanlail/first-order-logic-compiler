# first-order-logic-compiler
A front-end compiler for First-Order Logic. Performs Lexical and Syntax analysis, and produces the corresponding grammar and production rules for the given formulae and a parse tree. Where invalid formulae are used, the wrong character and it's position will be identified in the log file.

## First Order Logic
If you are new to first order logic, it is recomended to read this wikipedia article first https://en.wikipedia.org/wiki/First-order_logic#Syntax

The syntax of First Order logic used here is as follows:

* V is a set of variables (e.g. x1, x2,..., xn);
* C is a set of constants (e.g. C,D,...);
* P is a set of predicates of different arities (e.g. P(x, y) is a predicate of arity 2, Q(z) is a predicate
of arity 1) – the arity can be any positive integer;
* E = {=} is the equality symbol;
* L = {∧,∨, =⇒ , ⇐⇒ ,¬} is the set of logical connectives;
* Q = {∃,∀} is the set of quantifiers.

The last three sets are actually names for the respective items. Obviously, the brackets and the comma
are also symbols in this syntax.
Secondly, once the variables, constants, and predicates are defined, the language of all valid formulae is recursively defined as follows.

1. For any predicate P ∈ P of arity d and any collection of d variables y1,..., yd ∈ V (not necessarily
distinct), the atom P(y1,..., yd) is a valid formula.
2. For any constants C,D ∈ C and any variables x, y ∈ V , the atoms (C = D), (C = x), (x = C) and
(x = y) are also valid formulae.
3. If φ and ψ are valid formulae, then the following are all valid formulae:
(φ∧ψ); (φ∨ψ); (φ =⇒ ψ); (φ ⇐⇒ ψ); ¬φ.
4. If φ is a valid formula, then for any variable x ∈ V , ∃xφ and ∀xφ are also valid formulae.
For instance, for V = {w, x, y, z}, C = {C,D} and P = {P,Q} with respective arities 2 and 1, the following is a valid formula:
∀x(∃y(P(x, y) =⇒ ¬Q(x))∨ ∃z(((C = z)∧Q(z))∧ P(x, z)))

## Installation
This Program requires: 
* Python 3.6+ https://www.python.org/downloads/
* Graphviz https://graphviz.org/download
* anytree `pip3 install anytree` from the command-line

## Usage
`python3 compiler.py`

### Options
* -h - help
* -i - input file name
* -g - grammar output file name
* -t - parse tree output file name
* -l - log file name

## Input files
For examples on how to format the input files, please see example 1 included in this repository. There are also examples of invalid formulae.

## Examples
* Example 1 - valid input
* Example 2 - valid input
* Example 3 - Invalid input file (hence no tree, no grammar)
* Example 4 - Invalid formula (hence grammar no tree)
