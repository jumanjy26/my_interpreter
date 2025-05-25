# my_parser.py
# Parses tokens into an Abstract Syntax Tree (AST) for interpretation.

from lexer import Lexer

# AST node classes

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
        self.left = left        # Left side expression node
        self.op = op            # Operator token
        self.right = right      # Right side expression node

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op            # Unary operator token
        self.expr = expr        # Expression node it operates on

class VarAssign:
    def __init__(self, name, value):
        self.name = name        # Variable name (string)
        self.value = value      # Expression node assigned to variable

class VarAccess:
    def __init__(self, name):
        self.name = name        # Variable name (string)

class PrintStmt:
    def __init__(self, expr):
        self.expr = expr        # Expression to print

class IfStmt:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition      # Expression node for if condition
        self.true_block = true_block    # List of statements if true
        self.false_block = false_block  # List of statements if false (optional)

class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition  # Expression node for loop condition
        self.body = body            # List of statements inside the loop

class InputExpr:
    def __init__(self):
        pass                        # Represents input() call (no children)

# Parser class using recursive descent parsing

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg='Invalid syntax'):
        raise Exception(msg)

    def eat(self, token_type: str):
        # Consume the current token if it matches expected type, else error
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def parse(self):
        # Parse a sequence of statements until EOF
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_block(self):
        # Parse a block of statements enclosed in { ... }
        self.eat('LBRACE')
        statements = []
        while self.current_token.type != 'RBRACE':
            statements.append(self.parse_statement())
        self.eat('RBRACE')
        return statements

    def parse_statement(self):
        # Determine statement type and parse accordingly
        if self.current_token.type == 'PRINT':
            self.eat('PRINT')
            expr = self.parse_or()
            if self.current_token.type == 'SEMI':
                self.eat('SEMI')
            return PrintStmt(expr)

        elif self.current_token.type == 'IF':
            self.eat('IF')
            self.eat('LPAREN')
            condition = self.parse_or()
            self.eat('RPAREN')
            true_block = self.parse_block()
            false_block = None
            if self.current_token.type == 'ELSE':
                self.eat('ELSE')
                false_block = self.parse_block()
            return IfStmt(condition, true_block, false_block)

        elif self.current_token.type == 'WHILE':
            self.eat('WHILE')
            self.eat('LPAREN')
            condition = self.parse_or()
            self.eat('RPAREN')
            body = self.parse_block()
            return WhileStmt(condition, body)

        elif self.current_token.type == 'INPUT':
            self.eat('INPUT')
            self.eat('LPAREN')
            self.eat('RPAREN')
            return InputExpr()

        elif self.current_token.type == 'IDENTIFIER':
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

        else:
            expr = self.parse_or()
            if self.current_token.type == 'SEMI':
                self.eat('SEMI')
            return expr

    # Parsing expressions by precedence levels

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

        if token.type == 'INPUT':   # <-- This is the fix added here
            self.eat('INPUT')
            self.eat('LPAREN')
            self.eat('RPAREN')
            return InputExpr()

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


if __name__ == '__main__':
    from lexer import Lexer
    while True:
        try:
            text = input("Enter expression (or 'exit' to quit): ")
            if text.strip().lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            parser = Parser(Lexer(text))
            ast = parser.parse()
            print("Parsed AST:", ast)
        except Exception as e:
            print(f"Error: {e}")
