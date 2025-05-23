from lexer import Lexer

# AST node classes
class Num:
    def __init__(self, token):
        self.value = token.value

class Bool:
    def __init__(self, token):
        self.value = token.value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg='Invalid syntax'):
        raise Exception(msg)

    def eat(self, token_type: str):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def parse(self):
        """Entry point: parse a full expression and ensure we've consumed all tokens."""
        node = self.parse_or()
        if self.current_token.type != 'EOF':
            self.error('Unexpected token after expression')
        return node

    # Lowest-precedence: OR
    def parse_or(self):
        node = self.parse_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.eat('OR')
            node = BinOp(node, op, self.parse_and())
        return node

    # Next: AND
    def parse_and(self):
        node = self.parse_not()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.eat('AND')
            node = BinOp(node, op, self.parse_not())
        return node

    # Next: NOT (unary)
    def parse_not(self):
        if self.current_token.type == 'NOT':
            op = self.current_token
            self.eat('NOT')
            return UnaryOp(op, self.parse_not())
        return self.parse_comparison()

    # Comparisons: ==, !=, <, <=, >, >=
    def parse_comparison(self):
        node = self.parse_arith()
        if self.current_token.type in ('EQ', 'NE', 'LT', 'LTE', 'GT', 'GTE'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_arith())
        return node

    # Arithmetic addition/subtraction
    def parse_arith(self):
        node = self.parse_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_term())
        return node

    # Arithmetic multiplication/division
    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type in ('STAR', 'SLASH'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    # Unary +, -, numbers, booleans, and parenthesised expressions
    def parse_factor(self):
        token = self.current_token

        if token.type in ('PLUS', 'MINUS'):
            self.eat(token.type)
            return UnaryOp(token, self.parse_factor())

        if token.type in ('INT', 'FLOAT'):
            self.eat(token.type)
            return Num(token)

        if token.type == 'BOOLEAN':
            self.eat('BOOLEAN')
            return Bool(token)

        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_or()
            self.eat('RPAREN')
            return node

        self.error(f'Unexpected token {token.type}')


# Example usage:
if __name__ == '__main__':
     from lexer import Lexer
     text = input('Enter expression: ')
     parser = Parser(Lexer(text))
     ast = parser.parse()
     print(ast)
