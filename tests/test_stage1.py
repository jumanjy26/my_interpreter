#Arithmetic expressions

from src.lexer import Lexer
from src.my_parser import Parser
from src.interpreter import Interpreter
import pytest

@pytest.fixture
def interpreter():
    return Interpreter()

@pytest.mark.parametrize("expr, expected", [
    ("3 + 4", 7),
    ("10 - 2 * 3", 4),
    ("(5 + 6) * 2", 22),
    ("-7 + 8", 1),
    ("10 / 2 - 1", 4.0),
])
def test_arithmetic(interpreter, expr, expected):
    lexer = Lexer(expr)
    parser = Parser(lexer)
    ast = parser.parse()
    result = None
    for node in ast:
        val = interpreter.visit(node)
        if val is not None:
            result = val
    assert result == expected
