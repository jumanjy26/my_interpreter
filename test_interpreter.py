from lexer import Lexer
from my_parser import Parser
from interpreter import Interpreter

def test_interpreter():
    print("Running Stage 2 and 3 tests...")
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
        '"\nrepeat " * 3',
        '"number " + 123',
    ]

    for expr in test_cases:
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.parse()
        # ast might be list or single node
        if isinstance(ast, list):
            for node in ast:
                result = interpreter.visit(node)
        else:
            result = interpreter.visit(ast)
        print(f'Expression: {expr}')
        print('Result:', result)
        print('---')

def test_interpreter_stage4():
    print("Running Stage 4 tests...")
    interpreter = Interpreter()  # single interpreter instance to preserve variables
    program = """
    x = 5 + 3;
    y = "hello" + " world";
    print x;
    print y;
    z = x * 2;
    print z;
    """
    lexer = Lexer(program)
    parser = Parser(lexer)
    ast = parser.parse()
    interpreter.interpret(ast)

if __name__ == '__main__':
    test_interpreter()
    test_interpreter_stage4()
