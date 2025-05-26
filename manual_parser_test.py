from lexer import Lexer
from my_parser import Parser

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
            lexer = Lexer(expr)
            parser = Parser(lexer)
            ast = parser.parse()
            print(f"Input: {expr}")
            print("Parsed AST:")
            for node in ast:
                print(f"  {node}")
            print('-' * 40)
        except Exception as e:
            print(f"Input: {expr}")
            print(f"Error parsing: {e}")
            print('-' * 40)

if __name__ == "__main__":
    manual_parser_test()
