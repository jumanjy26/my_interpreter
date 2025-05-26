# Project: Simple Language Interpreter in Python

---------
Overview
---------
This project implements an interpreter for a simple programming language featuring:
- Arithmetic expressions (`+`, `-`, `*`, `/`)
- Boolean logic and comparisons
- String literals and operations
- Variables with assignment and access
- Control flow constructs: if-else, while loops
- Input and output (`print`, `input()`)

------------------
Project Structure
------------------
my_interpreter/
├── src/
│ ├── lexer.py # Lexical analyzer turning source code into tokens
│ ├── my_token.py # Token type constants and keywords definitions
│ ├── my_parser.py # Recursive descent parser generating AST nodes
│ ├── interpreter.py # AST visitor that executes the program
│ └── init.py # Marks src as a Python package
├── tests/
│ ├── test_stage1.py # Arithmetic expression tests
│ ├── test_stage2.py # Boolean logic and comparisons tests
│ ├── test_stage3.py # String operations tests
│ ├── test_stage4.py # Variables and print tests
│ └── test_stage5.py # Control flow and input tests
├── BUILD.txt
└── README.md

---------
Features
---------
- Modular design separating tokens, lexer, parser, and interpreter.
- Clear AST node classes with visitor pattern for interpretation.
- Automated tests using `pytest` for thorough correctness checking.
- Interactive interpreter mode for user input and code evaluation.

-----------------
## How to Run ##
-----------------

1. Interactive interpreter:

python -m src.interpreter

Enter your program statements or expressions interactively.

Type exit or quit to leave the interpreter.

2. Run automated tests:
From the project root directory, set the Python path environment variable to allow imports:

Windows PowerShell:
$env:PYTHONPATH = "."

Windows Command Prompt:
set PYTHONPATH=.

Run all tests:
pytest tests/

To run tests for a specific stage only:
pytest tests/test_stage3.py

------------
Requirements
------------
Python 3.7 or newer
pytest (install via pip install pytest)

------
Notes
------
Ensure src/__init__.py exists (can be empty) to mark src as a package.

Tokens and keywords are defined in src/my_token.py.

The interpreter’s interactive loop is protected by if __name__ == '__main__': to avoid blocking tests.

Tests use pytest fixtures and mock input() for thorough coverage.

---------------
Troubleshooting
---------------
If import errors occur, verify you run commands from the project root and PYTHONPATH is set correctly.

If tests hang, ensure no interactive input code runs outside the main guard block.

--------
Contact
--------
For questions or support, contact 100600430@unimail.derby.ac.uk