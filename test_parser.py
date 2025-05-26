# test_parser.py
#Automated batch tests for a fixed set of expressions

from lexer import Lexer
from my_parser import Parser

def test_parser():
    test_cases = [
        # Stage 2 tests: Booleans and arithmetic
        "true and false",
        "5 + 3 * 2",
        "(10 / 2) == 5",
        "not false or true",

        # Stage 3 tests: String literals and concatenation
        '"hello"',
        '"foo" + "bar"',
        '"repeat" * 3',
        '"number " + 123',
    ]

    for expr in test_cases:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        print(f'Expression: {expr}')
        print('Parsed AST:', ast)
        print('---')

def test_parser_stage4():
    test_cases = [
        "x = 5 + 3;",
        "y = \"hello\" + \" world\";",
        "print x;",
        "print y;",
        "z = x * 2;",
        "print z;"
    ]
    for expr in test_cases:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        print(f'Expression: {expr}')
        print('Parsed AST:', ast)
        print('---')

if __name__ == '__main__':
    test_parser_stage4()
