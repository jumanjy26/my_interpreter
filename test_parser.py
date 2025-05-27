# test_parser.py
# Automated batch tests for a fixed set of expressions.
# This script lexes and parses multiple sample expressions,
# then prints their Abstract Syntax Tree (AST) for manual verification.

from src.lexer import Lexer
from src.my_parser import Parser

def test_parser():
    """
    Test function for Stage 2 and 3 features:
    Booleans, arithmetic expressions, and string literals/operations.
    """
    test_cases = [
        # Stage 2 tests: Booleans and arithmetic expressions
        "true and false",
        "5 + 3 * 2",
        "(10 / 2) == 5",
        "not false or true",

        # Stage 3 tests: String literals and concatenation/repetition
        '"hello"',
        '"foo" + "bar"',
        '"repeat" * 3',
        '"number " + 123',  # Mixing string and number (for parsing; semantic error handled elsewhere)
    ]

    for expr in test_cases:
        # Initialize lexer and parser for each expression
        lexer = Lexer(expr)
        parser = Parser(lexer)
        # Parse input and get AST nodes (list of statements)
        ast = parser.parse()

        # Print original expression and its parsed AST for inspection
        print(f'Expression: {expr}')
        print('Parsed AST:', ast)
        print('---')

def test_parser_stage4():
    """
    Test function for Stage 4 features:
    Variable assignments and print statements.
    """
    test_cases = [
        "x = 5 + 3;",                # Variable assignment with arithmetic
        "y = \"hello\" + \" world\";",  # String concatenation in assignment
        "print x;",                  # Print variable
        "print y;",                  # Print string variable
        "z = x * 2;",                # Variable assignment with multiplication
        "print z;"                   # Print variable
    ]

    for expr in test_cases:
        # Initialize lexer and parser for each statement
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()

        # Print statement and its AST for manual checking
        print(f'Expression: {expr}')
        print('Parsed AST:', ast)
        print('---')

# Run stage 4 parser tests when script is executed directly
if __name__ == '__main__':
    test_parser_stage4()