from my_parser import Parser
from lexer import Lexer

class Interpreter:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise Exception(f'No visit_{type(node).__name__} method')
        return visitor(node)

    def visit_BinOp(self, node):
        if node.op.type == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'STAR':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'SLASH':
            return self.visit(node.left) / self.visit(node.right)
        else:
            raise Exception(f'Unknown operator {node.op.type}')

    def visit_Num(self, node):
        return node.value

if __name__ == '__main__':
    interpreter = Interpreter()
    print("Basic Calculator.")
    print("Type 'exit' or 'quit' to leave.")
    while True:
        text = input("> ").strip()
        if text.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not text:
            continue
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.expr()
            result = interpreter.visit(ast)
            print(result)
        except Exception as e:
            print(f"Error: {e}. Try again or type 'exit'.")
