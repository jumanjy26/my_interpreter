from lexer import Lexer
from my_parser import Parser
from my_parser import (
    Num, Bool, BinOp, UnaryOp, String,
    VarAssign, VarAccess, PrintStmt,
    IfStmt, WhileStmt, InputExpr
)
from lexer import (
    TT_PLUS, TT_MINUS, TT_MUL, TT_DIV,
    TT_EQ, TT_NE, TT_LT, TT_LTE,
    TT_GT, TT_GTE, TT_AND, TT_OR, TT_NOT
)

class Interpreter:
    def __init__(self):
        self.global_vars = {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise Exception(f"No visit method for node type: {type(node).__name__}")
        return visitor(node)

    def visit_Num(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_VarAccess(self, node):
        name = node.name
        if name not in self.global_vars:
            raise Exception(f"Variable '{name}' is not defined")
        return self.global_vars[name]

    def visit_VarAssign(self, node):
        value = self.visit(node.value)
        self.global_vars[node.name] = value
        return value

    def visit_PrintStmt(self, node):
        value = self.visit(node.expr)
        print(value)

    def visit_IfStmt(self, node):
        condition = self.visit(node.condition)
        if condition:
            for stmt in node.true_block:
                self.visit(stmt)
        elif node.false_block is not None:
            for stmt in node.false_block:
                self.visit(stmt)

    def visit_WhileStmt(self, node):
        while self.visit(node.condition):
            for stmt in node.body:
                self.visit(stmt)

    def visit_InputExpr(self, node):
        return input()

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type

        # Addition handling, including strict string + string only
        if op_type == TT_PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if isinstance(left, str) != isinstance(right, str):
                raise Exception(f"TypeError: unsupported operand types for +: '{type(left).__name__}' and '{type(right).__name__}'")
            return left + right

        # Multiplication handling with string repetition support
        if op_type == TT_MUL:
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(right, str) and isinstance(left, int):
                return right * left
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise Exception(f"TypeError: unsupported operand types for *: '{type(left).__name__}' and '{type(right).__name__}'")
            return left * right

        # Other arithmetic must be numeric only
        if op_type in {TT_MINUS, TT_DIV}:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise Exception(f"TypeError: unsupported operand types for {node.op.value}: '{type(left).__name__}' and '{type(right).__name__}'")

        if op_type == TT_MINUS:
            return left - right
        elif op_type == TT_DIV:
            if right == 0:
                raise Exception("Division by zero undefined")
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

    def interpret(self, statements):
        result = None
        for stmt in statements:
            val = self.visit(stmt)
            if val is not None:
                result = val
        if result is not None:
            print(result)
        return result

if __name__ == '__main__':
    interpreter = Interpreter()
    print("Stage 5 Interpreter - supports full language features\n")

    while True:
        try:
            print("> Enter your code (blank line to run, 'exit' to quit):")
            lines = []
            while True:
                line = input('> ').strip()
                if line.lower() in ('exit', 'quit'):
                    print("\n---Goodbye!---\n")
                    exit()
                if not line:
                    break
                lines.append(line)

            text = '\n'.join(lines)
            if not text.strip():
                continue

            lexer = Lexer(text)
            parser = Parser(lexer)
            statements = parser.parse()
            interpreter.interpret(statements)

        except Exception as e:
            print(f"Error: {e}")
