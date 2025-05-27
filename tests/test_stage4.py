#Variables, assignment, print statements

from src.lexer import Lexer
from src.my_parser import Parser
from src.interpreter import Interpreter
import pytest

@pytest.fixture
def interpreter():
    return Interpreter()

def test_variables_and_print(interpreter):
    program = """
    x = 10 + 5;
    y = "hello ";
    z = y + "world";
    print x;
    print z;
    w = x * 2;
    print w;
    """
    lexer = Lexer(program)
    parser = Parser(lexer)
    ast = parser.parse()
    for node in ast:
        interpreter.visit(node)