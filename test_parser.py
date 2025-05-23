from lexer import Lexer
from my_parser import Parser

def test_parser():
    while True:
        try:
            text = input('Enter expression (or "exit" to quit): ')
            if text.strip().lower() == 'exit':
                print('Exiting parser test.')
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()    # note: calling parse() here, not expr()
            print('Parsed AST:', ast)
        except Exception as e:
            print('Error:', e)

if __name__ == '__main__':
    test_parser()
