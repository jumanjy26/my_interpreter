from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter
import pytest
import builtins

@pytest.fixture
def interpreter():
    """
    Pytest fixture that provides a fresh Interpreter instance for each test.
    Ensures test isolation and no state leakage between tests.
    """
    return Interpreter()

def run_source(source, interpreter):
    """
    Helper function that lexes, parses, and interprets a source string.
    Returns the value of the last evaluated expression in the AST.
    """
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
    """
    Test arithmetic expressions with various operators and precedence.
    """
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
    """
    Test boolean logic operations and comparison expressions.
    """
    result = run_source(expr, interpreter)
    assert result == expected

# Stage 3: Strings and string operations
@pytest.mark.parametrize("expr, expected", [
    ('"hello" + " world"', "hello world"),
    ('"repeat" * 3', "repeatrepeatrepeat"),
])
def test_stage_3_strings(interpreter, expr, expected):
    """
    Test string concatenation and repetition.
    """
    result = run_source(expr, interpreter)
    assert result == expected

@pytest.mark.parametrize("expr", [
    '"foo" + 123',  # Mixed type addition should raise an error
])
def test_stage_3_strings_error(interpreter, expr):
    """
    Ensure that adding a string and a non-string raises an exception.
    """
    with pytest.raises(Exception):
        run_source(expr, interpreter)

# Stage 4: Variables and print statements
def test_stage_4_variables_and_print(interpreter):
    """
    Test variable assignment, string concatenation with variables,
    and printing variables to the console.
    """
    program = """
    x = 10 + 5;
    y = "hello ";
    z = y + "world";
    print x;
    print z;
    w = x * 2;
    print w;
    """
    # Run the program and verify no exceptions occur
    run_source(program, interpreter)

# Stage 5: Control flow and input handling
def test_stage_5_control_flow_and_input(interpreter, capsys, monkeypatch):
    """
    Test while loops, if-else statements, print statements, and input().
    Uses monkeypatch to simulate user input.
    """
    inputs = iter(["Alice"])
    # Override built-in input() to return predefined test input
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

    # Capture printed output and verify expected strings appear
    captured = capsys.readouterr()
    assert "2" in captured.out
    assert "1" in captured.out
    assert "Blast off!" in captured.out
    assert "Enter your name:" in captured.out
    assert "Hello, Alice" in captured.out

if __name__ == '__main__':
    pytest.main()