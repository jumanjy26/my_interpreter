from src.lexer import Lexer
from src.my_parser import Parser
from src.interpreter import Interpreter

def manual_interpreter_test():
    # List of test programs covering all stages (1 to 5) of the interpreter
    test_programs = [
        # Stage 1: Arithmetic expressions
        "3 + 4",
        "(5 + 2) * 3",
        "10 / 2 - 1",
        "-7 + 8",

        # Stage 2: Boolean logic and comparisons
        "true and false",
        "not false",
        "5 > 3",
        "10 == 10",
        "(4 <= 5) or false",

        # Stage 3: String operations (concatenation and repetition)
        '"hello" + " world"',
        '"ha" * 3',

        # Stage 4: Variable assignment and print statements
        "x = 10 + 5;",
        "y = \"hello \";",
        "z = y + \"world\";",
        "print x;",
        "print z;",
        "w = x * 2;",
        "print w;",

        # Stage 5: Control flow (while, if-else) and input (interactive)
        """
        x = 2;
        while (x > 0) {
            print x;
            x = x - 1;
        }
        if (x == 0) {
            print "Blast off!";
        } else {
            print "Counting down...";
        }
        print "Enter your name:";
        name = input();
        print "Hello, " + name;
        """
    ]

    # Create a single interpreter instance to run all programs
    interpreter = Interpreter()

    # Loop through each test program, running and printing output
    for i, program in enumerate(test_programs, start=1):
        print(f"--- Test Program {i} ---")
        # Print the source code of the program (strip extra whitespace)
        print(program.strip())
        print("Output:")
        try:
            # Create a lexer and parser for the current program
            lexer = Lexer(program)
            parser = Parser(lexer)
            # Parse the program into an AST (list of statements)
            statements = parser.parse()
            # Interpret (execute) the parsed statements
            interpreter.interpret(statements)
        except Exception as e:
            # If an error occurs during lexing/parsing/interpreting, print it
            print(f"Error: {e}")
        print("\n")  # Print a blank line for readability between tests

# Run the manual interpreter test suite if the script is executed directly
if __name__ == "__main__":
    manual_interpreter_test()