# interpreter.py

from lexer import Lexer
from my_parser import Parser
from my_parser import Num, Bool, BinOp, UnaryOp, String
from lexer import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_EQ, TT_NE, TT_LT, TT_LTE, TT_GT, TT_GTE, TT_AND, TT_OR, TT_NOT

class Interpreter:
    def visit(self, node):
        # Dispatch method based on node class name, e.g. visit_Num, visit_BinOp
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise Exception(f"No visit_{type(node).__name__} method")
        return visitor(node)

    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_String(self, node):
        # Return the string literal's value
        return node.value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type

        if op_type == TT_PLUS:
            # If either operand is string, convert both to string and concatenate
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif op_type == TT_MINUS:
            return left - right
        elif op_type == TT_MUL:
            return left * right
        elif op_type == TT_DIV:
            if right == 0:
                raise Exception("Division by zero")
            return left / right
        elif op_type == TT_EQ:
            return left == right
        elif op_type == TT_NE:
            return left != right
        elif op_type == TT_LT:
            return left < right
        elif op_type == TT_LTE:
            return left <= right
        elif op_type == TT_GT:
            return left > right
        elif op_type == TT_GTE:
            return left >= right
        elif op_type == TT_AND:
            return bool(left) and bool(right)
        elif op_type == TT_OR:
            return bool(left) or bool(right)
        else:
            raise Exception(f"Unknown binary operator {op_type}")

    def visit_UnaryOp(self, node):
        val = self.visit(node.expr)
        op_type = node.op.type

        if op_type == TT_PLUS:
            return +val
        elif op_type == TT_MINUS:
            return -val
        elif op_type == TT_NOT:
            return not val
        else:
            raise Exception(f"Unknown unary operator {op_type}")

if __name__ == '__main__':
    interpreter = Interpreter()
    print("Stage 3 Interpreter \nType 'exit' or 'quit' to leave.")
    while True:
        try:
            text = input('> ').strip()
            if text.lower() in ('exit', 'quit'):
                print("\nGoodbye!")
                break
            if not text:
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()
            result = interpreter.visit(ast)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
