README

Project: Simple Interpreter for a Custom Language (Stages 1-5)

1. Overview:
   This project implements a simple interpreter that supports:
   - Stage 1: Arithmetic expressions (+, -, *, /)
   - Stage 2: Boolean logic (and, or, not) and comparisons
   - Stage 3: String literals and operations (+ concatenation, * repetition)
   - Stage 4: Variables, assignments, and print statements
   - Stage 5: Control flow constructs (if-else, while loops) and input()

2. How to use:
   - Run the interpreter interactively with:
     python interpreter.py
   - Input code statements or expressions.
   - Use a blank line to execute entered multi-line code.
   - Type 'exit' or 'quit' to end the session.

3. Testing:
   - Automated testing is done with pytest. Run:
     pytest test_interpreter_pytest.py
   - Manual parser and interpreter tests can be run for demonstration.

4. Example source files:
   - Five example programs (example1.txt ... example5.txt) demonstrate valid language syntax and features.

5. Notes:
   - The interpreter performs lexical analysis, parsing, and interpretation.
   - Errors such as undefined variables or type errors are reported during execution.

