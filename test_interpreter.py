# test_interpreter.py

from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter

def test_interpreter():
    interpreter = Interpreter()
    test_cases = [
        # Stage 2 interpreter tests
        "true and false",
        "5 + 3 * 2",
        "(10 / 2) == 5",
        "not false or true",

        # Stage 3 interpreter tests with strings
        '"hello"',
        '"foo" + "bar"',
        '"\nrepeat" * 3',
        '"number " + 123',
    ]

    for expr in test_cases:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        result = interpreter.visit(ast)
        print(f'Expression: {expr}')
        print('Result:', result)
        print('---')

if __name__ == '__main__':
    test_interpreter()
