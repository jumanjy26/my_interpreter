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
        # Store global variables and their values here
        self.global_vars = {}

    def visit(self, node):
        # Build method name like 'visit_Num' or 'visit_VarAssign'
        method_name = 'visit_' + type(node).__name__
        # Get the method by name; if not found, raise exception
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise Exception(f"No visit method for node type: {type(node).__name__}")
        # Call the method and return its result
        return visitor(node)

    def visit_Num(self, node):
        # Return the numeric value of a number node
        return node.value

    def visit_Bool(self, node):
        # Return the boolean value of a boolean node
        return node.value

    def visit_String(self, node):
        # Return the string value of a string node
        return node.value

    def visit_VarAccess(self, node):
        # Access the value of a variable from globals dictionary
        name = node.name
        if name not in self.global_vars:
            raise Exception(f"Variable '{name}' is not defined")
        return self.global_vars[name]

    def visit_VarAssign(self, node):
        # Evaluate the right-hand side expression
        value = self.visit(node.value)
        # Store value in the variable name in globals
        self.global_vars[node.name] = value
        return value

    def visit_PrintStmt(self, node):
        # Evaluate expression to print
        value = self.visit(node.expr)
        # Print the value to console
        print(value)

    def visit_IfStmt(self, node):
        # Evaluate the if condition
        condition = self.visit(node.condition)
        if condition:
            # If true, visit all statements in true_block
            for stmt in node.true_block:
                self.visit(stmt)
        elif node.false_block is not None:
            # If false and else block exists, visit else block
            for stmt in node.false_block:
                self.visit(stmt)

    def visit_WhileStmt(self, node):
        # Loop while condition is true
        while self.visit(node.condition):
            # Execute all statements inside the loop body
            for stmt in node.body:
                self.visit(stmt)

    def visit_InputExpr(self, node):
        # Read input from user and return as string
        return input()

    def visit_BinOp(self, node):
        # Visit left and right subexpressions
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type

        # Handle addition operator
        if op_type == TT_PLUS:
            # If both operands are strings, concatenate
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            # Disallow mixing string with non-string
            if isinstance(left, str) != isinstance(right, str):
                raise Exception(f"TypeError: unsupported operand types for +: '{type(left).__name__}' and '{type(right).__name__}'")
            # Otherwise numeric addition
            return left + right

        # Handle multiplication operator
        if op_type == TT_MUL:
            # Support string repetition
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(right, str) and isinstance(left, int):
                return right * left
            # Ensure numeric multiplication only otherwise
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise Exception(f"TypeError: unsupported operand types for *: '{type(left).__name__}' and '{type(right).__name__}'")
            return left * right

        # Ensure numeric operands for subtraction and division
        if op_type in {TT_MINUS, TT_DIV}:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise Exception(f"TypeError: unsupported operand types for {node.op.value}: '{type(left).__name__}' and '{type(right).__name__}'")

        # Handle subtraction
        if op_type == TT_MINUS:
            return left - right
        # Handle division, protect division by zero
        elif op_type == TT_DIV:
            if right == 0:
                raise Exception("Division by zero undefined")
            return left / right
        # Handle equality check
        elif op_type == TT_EQ:
            return left == right
        # Handle inequality check
        elif op_type == TT_NE:
            return left != right
        # Less than
        elif op_type == TT_LT:
            return left < right
        # Less than or equal
        elif op_type == TT_LTE:
            return left <= right
        # Greater than
        elif op_type == TT_GT:
            return left > right
        # Greater than or equal
        elif op_type == TT_GTE:
            return left >= right
        # Logical AND (boolean)
        elif op_type == TT_AND:
            return bool(left) and bool(right)
        # Logical OR (boolean)
        elif op_type == TT_OR:
            return bool(left) or bool(right)
        else:
            # Unknown operator error
            raise Exception(f"Unknown binary operator {op_type}")

    def visit_UnaryOp(self, node):
        # Visit the operand expression
        val = self.visit(node.expr)
        op_type = node.op.type
        # Unary plus returns the value unchanged
        if op_type == TT_PLUS:
            return +val
        # Unary minus negates the value
        elif op_type == TT_MINUS:
            return -val
        # Logical NOT negates the boolean value
        elif op_type == TT_NOT:
            return not val
        else:
            raise Exception(f"Unknown unary operator {op_type}")

    def interpret(self, statements):
        # Interpret a list of AST statements in order
        result = None
        for stmt in statements:
            val = self.visit(stmt)
            # Keep last evaluated non-None result
            if val is not None:
                result = val
        # Print last evaluated result if exists
        if result is not None:
            print(result)
        return result

if __name__ == '__main__':
    # Entry point for interactive interpreter session
    interpreter = Interpreter()
    print("Stage 5 Interpreter - supports full language features\n")

while True:
    try:
        text = input('> ').strip()
        if text.lower() in ('exit', 'quit'):
            print("\n---Goodbye!---\n")
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        statements = parser.parse()
        interpreter.interpret(statements)

    except Exception as e:
        print(f"Error: {e}")
