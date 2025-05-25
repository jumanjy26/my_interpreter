from lexer import Lexer

class Num:
    def __init__(self, token):
        self.value = token.value

class Bool:
    def __init__(self, token):
        self.value = token.value

class String:
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

class VarAssign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAccess:
    def __init__(self, name):
        self.name = name

class PrintStmt:
    def __init__(self, expr):
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
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_statement(self):
        if self.current_token.type == 'PRINT':
            self.eat('PRINT')
            expr = self.parse_or()
            if self.current_token.type == 'SEMI':
                self.eat('SEMI')
            return PrintStmt(expr)
        
        if self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.eat('IDENTIFIER')
            if self.current_token.type == 'ASSIGN':
                self.eat('ASSIGN')
                expr = self.parse_or()
                if self.current_token.type == 'SEMI':
                    self.eat('SEMI')
                return VarAssign(var_name, expr)
            else:
                return VarAccess(var_name)
        
        expr = self.parse_or()
        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
        return expr

    def parse_or(self):
        node = self.parse_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.eat('OR')
            node = BinOp(node, op, self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.eat('AND')
            node = BinOp(node, op, self.parse_not())
        return node

    def parse_not(self):
        if self.current_token.type == 'NOT':
            op = self.current_token
            self.eat('NOT')
            return UnaryOp(op, self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self):
        node = self.parse_arith()
        if self.current_token.type in ('EQ', 'NE', 'LT', 'LTE', 'GT', 'GTE'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_arith())
        return node

    def parse_arith(self):
        node = self.parse_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_factor())
        return node

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

        if token.type == 'STRING':
            self.eat('STRING')
            return String(token)

        if token.type == 'IDENTIFIER':
            var_name = token.value
            self.eat('IDENTIFIER')
            return VarAccess(var_name)

        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_or()
            self.eat('RPAREN')
            return node

        self.error(f'Unexpected token {token.type}')
