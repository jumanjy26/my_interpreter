#Boolean logic and comparisons

from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter
import pytest

@pytest.fixture
def interpreter():
    return Interpreter()

@pytest.mark.parametrize("expr, expected", [
    ("true and false", False),
    ("not false or true", True),
    ("5 > 3", True),
    ("10 == 10", True),
    ("4 <= 5 or false", True),
])
def test_booleans(interpreter, expr, expected):
    lexer = Lexer(expr)
    parser = Parser(lexer)
    ast = parser.parse()
    result = None
    for node in ast:
        val = interpreter.visit(node)
        if val is not None:
            result = val
    assert result == expected
