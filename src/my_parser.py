# my_parser.py
# Recursive descent parser: converts tokens into AST nodes representing the program structure.

from src.lexer import Lexer

# === AST Node Classes ===
# Each class represents a different type of syntax node in the language.

class Num:
    def __init__(self, token):
        self.value = token.value  # Numeric literal value (int or float)
    def __repr__(self):
        return f"Num({self.value})"

class Bool:
    def __init__(self, token):
        self.value = token.value  # Boolean literal (True or False)
    def __repr__(self):
        return f"Bool({self.value})"

class String:
    def __init__(self, token):
        self.value = token.value  # String literal value
    def __repr__(self):
        # Use repr() to show string quotes and escape sequences
        return f"String({repr(self.value)})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left          # Left operand (AST node)
        self.op = op              # Operator token
        self.right = right        # Right operand (AST node)
    def __repr__(self):
        return f"BinOp({self.left}, {self.op.value}, {self.right})"

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op              # Unary operator token
        self.expr = expr          # Expression it applies to
    def __repr__(self):
        return f"UnaryOp({self.op.value}, {self.expr})"

class VarAssign:
    def __init__(self, name, value):
        self.name = name          # Variable name (string)
        self.value = value        # Expression node assigned to the variable
    def __repr__(self):
        return f"VarAssign({self.name}, {self.value})"

class VarAccess:
    def __init__(self, name):
        self.name = name          # Variable name being accessed
    def __repr__(self):
        return f"VarAccess({self.name})"

class PrintStmt:
    def __init__(self, expr):
        self.expr = expr          # Expression to print
    def __repr__(self):
        return f"PrintStmt({self.expr})"

class IfStmt:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition      # Condition expression node
        self.true_block = true_block    # List of statements if condition is True
        self.false_block = false_block  # List of statements if False (optional)
    def __repr__(self):
        if self.false_block:
            return f"IfStmt({self.condition}, {self.true_block}, {self.false_block})"
        else:
            return f"IfStmt({self.condition}, {self.true_block})"

class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition  # Condition expression node for loop
        self.body = body            # List of statements inside the while loop
    def __repr__(self):
        return f"WhileStmt({self.condition}, {self.body})"

class InputExpr:
    def __init__(self):
        pass                      # Represents a call to input() with no arguments
    def __repr__(self):
        return "InputExpr()"

# === Parser Class ===
# Implements recursive descent parsing for the language grammar.

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()  # Get first token

    def error(self, msg='Invalid syntax'):
        """
        Raise an exception with a descriptive error message including
        the current token type and value.
        """
        token = self.current_token
        raise Exception(f"{msg} at token {token.type} with value '{token.value}'")

    def eat(self, token_type: str):
        """
        Consume the current token if it matches the expected type.
        Otherwise, raise a syntax error.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def parse(self):
        """
        Parse a sequence of statements until EOF.
        Returns a list of AST nodes representing the statements.
        """
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_block(self):
        """
        Parse a block of statements enclosed in braces { ... }.
        Returns a list of statement AST nodes inside the block.
        """
        self.eat('LBRACE')  # Expect '{' to start block
        statements = []

        # Continue parsing statements until closing brace or EOF
        while self.current_token.type != 'RBRACE' and self.current_token.type != 'EOF':
            statements.append(self.parse_statement())

        self.eat('RBRACE')  # Expect '}' to close block
        return statements

    def parse_statement(self):
        """
        Parse a single statement.
        Supports print, if, while, input, variable assignment/access,
        or falls back to parsing an expression.
        """
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

    # === Expression parsing follows operator precedence ===

    def parse_or(self):
        """
        Parse logical OR expressions.
        Grammar: or_expr -> and_expr ('OR' and_expr)*
        """
        node = self.parse_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.eat('OR')
            node = BinOp(node, op, self.parse_and())
        return node

    def parse_and(self):
        """
        Parse logical AND expressions.
        Grammar: and_expr -> not_expr ('AND' not_expr)*
        """
        node = self.parse_not()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.eat('AND')
            node = BinOp(node, op, self.parse_not())
        return node

    def parse_not(self):
        """
        Parse unary NOT expressions or fallback to comparison parsing.
        Grammar: not_expr -> 'NOT' not_expr | comparison
        """
        if self.current_token.type == 'NOT':
            op = self.current_token
            self.eat('NOT')
            return UnaryOp(op, self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self):
        """
        Parse comparison expressions.
        Grammar: comparison -> arith_expr (('EQ'|'NE'|'LT'|'LTE'|'GT'|'GTE') arith_expr)?
        """
        node = self.parse_arith()
        if self.current_token.type in ('EQ', 'NE', 'LT', 'LTE', 'GT', 'GTE'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_arith())
        return node

    def parse_arith(self):
        """
        Parse addition and subtraction.
        Grammar: arith_expr -> term (('PLUS'|'MINUS') term)*
        """
        node = self.parse_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        """
        Parse multiplication and division.
        Grammar: term -> factor (('MUL'|'DIV') factor)*
        """
        node = self.parse_factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        """
        Parse unary operators and primary expressions.
        Grammar:
            factor -> ('PLUS' | 'MINUS') factor
                    | 'INT' | 'FLOAT' | 'BOOLEAN' | 'STRING' | 'INPUT'
                    | 'IDENTIFIER'
                    | '(' or_expr ')'
        """
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

        if token.type == 'INPUT':
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

        self.error('Unexpected token')

# Quick interactive test when running this file directly
if __name__ == '__main__':
    from src.lexer import Lexer
    while True:
        try:
            text = input("Enter expression or statement (or 'exit' to quit): ")
            if text.strip().lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            parser = Parser(Lexer(text))
            ast = parser.parse()
            print("Parsed AST:", ast)
        except Exception as e:
            print(f"Error: {e}")