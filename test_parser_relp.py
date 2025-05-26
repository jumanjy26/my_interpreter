from lexer import Lexer
from my_parser import Parser

def run_parser_test():
    print("Enter expressions to parse (type 'exit' to quit):\n")
    while True:
        text = input("> ")
        if text.strip().lower() in ('exit', 'quit'):
            print("---\nGoodbye!---\n")
            break
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()
            print("Parsed AST:", ast)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run_parser_test()
