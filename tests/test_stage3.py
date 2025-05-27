#String literals and operations

from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter
import pytest

@pytest.fixture
def interpreter():
    return Interpreter()

@pytest.mark.parametrize("expr, expected", [
    ('"hello" + " world"', "hello world"),
    ('"repeat" * 3', "repeatrepeatrepeat"),
])
def test_strings(interpreter, expr, expected):
    lexer = Lexer(expr)
    parser = Parser(lexer)
    ast = parser.parse()
    result = None
    for node in ast:
        val = interpreter.visit(node)
        if val is not None:
            result = val
    assert result == expected

@pytest.mark.parametrize("expr", [
    '"foo" + 123',
])
def test_strings_errors(interpreter, expr):
    lexer = Lexer(expr)
    parser = Parser(lexer)
    ast = parser.parse()
    with pytest.raises(Exception):
        for node in ast:
            interpreter.visit(node)
