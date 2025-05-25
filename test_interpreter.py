from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter

def test_stage_1_to_3(interpreter):
    print("Testing Stage 1-3 features (arithmetic, booleans, strings)...")
    test_cases = [
        "3 + 4",
        "10 - 2 * 3",
        "(5 + 6) * 2",
        "true and false",
        "not false or true",
        '"hello" + " world"',
        '"repeat" * 3',
        '"foo" + 123',
    ]
    for expr in test_cases:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        # parser returns a list, interpret each node
        for node in ast:
            result = interpreter.visit(node)
        print(f"Expression: {expr}")
        print(f"Result: {result}")
        print("---")

def test_stage_4(interpreter):
    print("Testing Stage 4 features (variables, assignment, print)...")
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
    interpreter.interpret(ast)

def test_stage_5(interpreter):
    print("Testing Stage 5 features (control flow and input)...")

    # Input simulation: override input() in interpreter temporarily
    inputs = iter(["Alice"])  # simulate user input

    original_input = __builtins__.input
    __builtins__.input = lambda: next(inputs)

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

    try:
        lexer = Lexer(program)
        parser = Parser(lexer)
        ast = parser.parse()
        interpreter.interpret(ast)
    finally:
        __builtins__.input = original_input  # restore input

if __name__ == '__main__':
    interpreter = Interpreter()
    test_stage_1_to_3(interpreter)
    print("\n")
    test_stage_4(interpreter)
    print("\n")
    test_stage_5(interpreter)
