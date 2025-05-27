Project: Simple Language Interpreter in Python
---------------------------------------------

Overview:
---------
This project implements an interpreter for a simple programming language featuring:
- Arithmetic expressions (+, -, *, /)
- Boolean logic and comparisons
- String literals and operations
- Variables with assignment and access
- Control flow constructs: if-else, while loops
- Input and output (print, input())

Project Structure:
------------------
- src/
  Contains all source code files:
  - lexer.py         : Lexical analyzer turning source code into tokens
  - my_token.py      : Token type constants and keywords definitions
  - my_parser.py     : Recursive descent parser generating AST nodes
  - interpreter.py   : AST visitor that executes the program
  - __init__.py      : Marks src as a Python package

- tests/
  Automated test files split by language feature stage:
  - test_stage1.py   : Arithmetic expression tests
  - test_stage2.py   : Boolean logic and comparisons tests
  - test_stage3.py   : String operations tests
  - test_stage4.py   : Variables and print tests
  - test_stage5.py   : Control flow and input tests

Features:
---------
- Modular design separating tokens, lexer, parser, and interpreter.
- Clear AST node classes with visitor pattern for interpretation.
- Automated tests using pytest for thorough correctness checking.
- Interactive interpreter mode for user input and code evaluation.

How to Run:
-----------
1. Interactive interpreter:
python src/interpreter.py