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

# Stage 1: Arithmetic tests
@pytest.mark.parametrize("expr, expected", [
    ("3 + 4", 7),
    ("10 - 2 * 3", 4),
    ("(5 + 6) * 2", 22),
    ("-7 + 8", 1),
    ("10 / 2 - 1", 4.0),
])
def test_stage_1_arithmetic(interpreter, expr, expected):
    result = run_source(expr, interpreter)
    assert result == expected

# Stage 2: Booleans and comparisons
@pytest.mark.parametrize("expr, expected", [
    ("true and false", False),
    ("not false or true", True),
    ("5 > 3", True),
    ("10 == 10", True),
    ("4 <= 5 or false", True),
])
def test_stage_2_booleans(interpreter, expr, expected):
    result = run_source(expr, interpreter)
    assert result == expected

# Stage 3: Strings and string ops
@pytest.mark.parametrize("expr, expected", [
    ('"hello" + " world"', "hello world"),
    ('"repeat" * 3', "repeatrepeatrepeat"),
])
def test_stage_3_strings(interpreter, expr, expected):
    result = run_source(expr, interpreter)
    assert result == expected

@pytest.mark.parametrize("expr", [
    '"foo" + 123',  # Should raise type error for mixed types
])
def test_stage_3_strings_error(interpreter, expr):
    with pytest.raises(Exception):
        run_source(expr, interpreter)

# Stage 4: Variables and print
def test_stage_4_variables_and_print(interpreter):
    program = """
    x = 10 + 5;
    y = "hello ";
    z = y + "world";
    print x;
    print z;
    w = x * 2;
    print w;
    """
    # Just run to ensure no exceptions
    run_source(program, interpreter)

# Stage 5: Control flow and input
def test_stage_5_control_flow_and_input(interpreter, capsys, monkeypatch):
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
