from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter
import pytest
import builtins

@pytest.fixture
def interpreter():
    return Interpreter()

def run_source(source, interpreter):
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    result = None
    for node in ast:
        val = interpreter.visit(node)
        if val is not None:
            result = val
    return result

def test_stage_1_to_3(interpreter):
    test_cases = [
        ("3 + 4", 7),
        ("10 - 2 * 3", 4),
        ("(5 + 6) * 2", 22),
        ("true and false", False),
        ("not false or true", True),
        ('"hello" + " world"', "hello world"),
        ('"repeat" * 3', "repeatrepeatrepeat"),
        ('"foo" + 123', None),  # Expect error (None) for mixed type addition
    ]

    for expr, expected in test_cases:
        if expected is None:
            # Expect an exception
            with pytest.raises(Exception):
                run_source(expr, interpreter)
        else:
            result = run_source(expr, interpreter)
            assert result == expected, f"Failed on expression: {expr}"

def test_stage_4(interpreter):
    program = """
    x = 10 + 5;
    y = "hello ";
    z = y + "world";
    print x;
    print z;
    w = x * 2;
    print w;
    """
    run_source(program, interpreter)

def test_stage_5(interpreter, capsys, monkeypatch):
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

    run_source(program, interpreter)
    captured = capsys.readouterr()
    assert "2" in captured.out
    assert "1" in captured.out
    assert "Blast off!" in captured.out
    assert "Enter your name:" in captured.out
    assert "Hello, Alice" in captured.out

if __name__ == '__main__':
    pytest.main()
