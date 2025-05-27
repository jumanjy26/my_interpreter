#Control flow, loops, input

from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter
import pytest
import builtins

@pytest.fixture
def interpreter():
    return Interpreter()

def test_control_flow_and_input(interpreter, monkeypatch, capsys):
    inputs = iter(["Alice"])
    monkeypatch.setattr(builtins, 'input', lambda: next(inputs))
    program = """
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
    lexer = Lexer(program)
    parser = Parser(lexer)
    ast = parser.parse()
    for node in ast:
        interpreter.visit(node)
    captured = capsys.readouterr()
    assert "2" in captured.out
    assert "1" in captured.out
    assert "Blast off!" in captured.out
    assert "Enter your name:" in captured.out
    assert "Hello, Alice" in captured.out
