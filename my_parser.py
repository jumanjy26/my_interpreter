# my_parser.py

from lexer import Lexer

# AST node classes representing parts of the expression tree
class Num:
    def __init__(self, token):
        self.value = token.value  # Numeric value

class Bool:
    def __init__(self, token):
        self.value = token.value  # Boolean value (True/False)

class String:
    def __init__(self, token):
        self.value = token.value  # String literal value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left          # Left operand node
        self.op = op              # Operator token (e.g., PLUS)
        self.right = right        # Right operand node

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op              # Operator token (e.g., MINUS, NOT)
        self.expr = expr          # Operand expression node

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg='Invalid syntax'):
        raise Exception(msg)

    def eat(self, token_type: str):
        # Consume the current token if it matches expected type; else error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def parse(self):
        # Entry point: parse a full expression and ensure no extra tokens remain
        node = self.parse_or()
        if self.current_token.type != 'EOF':
            self.error('Unexpected token after expression')
        return node

    def parse_or(self):
        # Parse logical OR expressions (lowest precedence)
        node = self.parse_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.eat('OR')
            node = BinOp(node, op, self.parse_and())
        return node

    def parse_and(self):
        # Parse logical AND expressions
        node = self.parse_not()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.eat('AND')
            node = BinOp(node, op, self.parse_not())
        return node

    def parse_not(self):
        # Parse logical NOT unary operator
        if self.current_token.type == 'NOT':
            op = self.current_token
            self.eat('NOT')
            return UnaryOp(op, self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self):
        # Parse comparison operators (==, !=, <, <=, >, >=)
        node = self.parse_arith()
        if self.current_token.type in ('EQ', 'NE', 'LT', 'LTE', 'GT', 'GTE'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_arith())
        return node

    def parse_arith(self):
        # Parse addition and subtraction, including string concatenation with '+'
        node = self.parse_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        # Parse multiplication and division
        node = self.parse_factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        token = self.current_token

        # Unary + or -
        if token.type in ('PLUS', 'MINUS'):
            self.eat(token.type)
            return UnaryOp(token, self.parse_factor())

        # Number literals
        if token.type in ('INT', 'FLOAT'):
            self.eat(token.type)
            return Num(token)

        # Boolean literals
        if token.type == 'BOOLEAN':
            self.eat('BOOLEAN')
            return Bool(token)

        # String literals (Stage 3)
        if token.type == 'STRING':
            self.eat('STRING')
            return String(token)

        # Parenthesized expressions
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_or()
            self.eat('RPAREN')
            return node

        self.error(f'Unexpected token {token.type}')