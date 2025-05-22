from parser import Parser
from lexer import Lexer

class Interpreter:
    def visit(self, node):                  # dispatcher method
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, None)
        
        if not visitor:
            raise Exception(f'No visit_{type(node).__name__} method')
        return visitor(node)
    
    def visit_BinOp(self, node):                #binary operations (+, -, *, /)
        if node.op.type == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == 'STAR':
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == 'SLASH':
            return self.visit(node.left) / self.visit(node.right)
        raise Exception(f'Unknown operator {node.op.type}')
    
    def visit_Num(self, node):      ## return its stored numeric value
        return node.value

if __name__ == '__main__':
    interpreter = Interpreter()
    print("Basic Calculator. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            text = input('> ').strip()

            # handle empty input or quit commands
            if not text or text.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break

            # run lexer, parser, interpreter
            lexer  = Lexer(text)
            parser = Parser(lexer)
            ast    = parser.expr()
            result = interpreter.visit(ast)
            print(result)

        except Exception as e:
            # catch any errors (invalid char, parse error, div by zero, etc)
            print(f"Error: {e}. Try again or type 'exit'.")