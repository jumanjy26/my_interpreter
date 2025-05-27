from src.lexer import Lexer
from src.my_parser import Parser

def manual_parser_test():
    test_cases = [
        # Boolean and arithmetic expressions
        "true and false",
        "5 + 3 * 2",
        "(10 / 2) == 5",
        "not false or true",

        # String literals and operations
        '"hello"',
        '"foo" + "bar"',
        '"repeat" * 3',
        # This one should raise an error in interpreter but we just parse here
        '"number " + 123',

        # Variable assignment and print statements
        "x = 5 + 3;",
        "y = \"hello\" + \" world\";",
        "print x;",
        "print y;",

        # Control flow statements
        "if (x > 3) { print x; } else { print 0; }",
        "while (x < 10) { x = x + 1; print x; }",
    ]

    for expr in test_cases:
        try:
            # Initialize the lexer with the current input expression string
            lexer = Lexer(expr)
            # Initialize the parser with the lexer to parse tokens into an AST
            parser = Parser(lexer)
            # Parse the expression into a list of AST nodes (statements)
            ast = parser.parse()
            
            # Print the original input expression for reference
            print(f"Input: {expr}")
            print("Parsed AST:")
            
            # Iterate through all AST nodes and print their representation
            for node in ast:
                print(f"  {node}")
            
            # Print a separator line for readability between test cases
            print('-' * 40)
        
        except Exception as e:
            # If parsing fails, print the input and the error message
            print(f"Input: {expr}")
            print(f"Error parsing: {e}")
            print('-' * 40)

if __name__ == "__main__":
    manual_parser_test()
