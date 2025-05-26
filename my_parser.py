# my_parser.py
# Recursive descent parser: converts tokens into AST nodes representing the program structure.

from lexer import Lexer

# === AST Node Classes ===
# Each class corresponds to a kind of syntax node in your language.

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
        return f"String({repr(self.value)})"  # repr for readable quotes and escapes

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
        self.value = value        # Expression node assigned
    def __repr__(self):
        return f"VarAssign({self.name}, {self.value})"

class VarAccess:
    def __init__(self, name):
        self.name = name          # Variable name accessed
    def __repr__(self):
        return f"VarAccess({self.name})"

class PrintStmt:
    def __init__(self, expr):
        self.expr = expr          # Expression to print
    def __repr__(self):
        return f"PrintStmt({self.expr})"

class IfStmt:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition      # Condition expression
        self.true_block = true_block    # List of statements if True
        self.false_block = false_block  # List of statements if False (optional)
    def __repr__(self):
        if self.false_block:
            return f"IfStmt({self.condition}, {self.true_block}, {self.false_block})"
        else:
            return f"IfStmt({self.condition}, {self.true_block})"

class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition  # Loop condition expression
        self.body = body            # List of statements inside loop
    def __repr__(self):
        return f"WhileStmt({self.condition}, {self.body})"

class InputExpr:
    def __init__(self):
        pass                      # Represents input() call with no args
    def __repr__(self):
        return "InputExpr()"

# === Parser Class ===
# Implements recursive descent parsing with operator precedence

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()  # Initialize first token

    def error(self, msg='Invalid syntax'):
        token = self.current_token
        raise Exception(f"{msg} at token {token.type} with value '{token.value}'")

    def eat(self, token_type: str):
        """
        Consume current token if it matches token_type.
        Otherwise raise syntax error.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def parse(self):
        """
        Parse multiple statements until EOF.
        Returns a list of AST statement nodes.
        """
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_block(self):
        """
        Parse a block of statements inside braces { ... }.
        Returns a list of statement nodes inside the block.
        """
        self.eat('LBRACE')  # Consume '{'
        statements = []

        # Loop until matching '}' or EOF (avoid infinite loop)
        while self.current_token.type != 'RBRACE' and self.current_token.type != 'EOF':
            statements.append(self.parse_statement())

        self.eat('RBRACE')  # Consume '}'
        return statements

    def parse_statement(self):
        """
        Parse a single statement.
        Supports print, if, while, input, variable assignment, or expression.
        """

        # Print statement: print expr;
        if self.current_token.type == 'PRINT':
            self.eat('PRINT')
            expr = self.parse_or()
            if self.current_token.type == 'SEMI':
                self.eat('SEMI')
            return PrintStmt(expr)

        # If statement: if (condition) { true_block } [ else { false_block } ]
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

        # While loop: while (condition) { body }
        elif self.current_token.type == 'WHILE':
            self.eat('WHILE')
            self.eat('LPAREN')
            condition = self.parse_or()
            self.eat('RPAREN')
            body = self.parse_block()
            return WhileStmt(condition, body)

        # input(): input()
        elif self.current_token.type == 'INPUT':
            self.eat('INPUT')
            self.eat('LPAREN')
            self.eat('RPAREN')
            return InputExpr()

        # Variable assignment or access: var = expr; or var
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

        # Otherwise parse as an expression (with optional trailing semicolon)
        else:
            expr = self.parse_or()
            if self.current_token.type == 'SEMI':
                self.eat('SEMI')
            return expr

    # === Expression Parsing by Precedence ===

    def parse_or(self):
        """
        Parse OR expressions (lowest precedence for boolean ops).
        or_expr -> and_expr ('OR' and_expr)*
        """
        node = self.parse_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.eat('OR')
            node = BinOp(node, op, self.parse_and())
        return node

    def parse_and(self):
        """
        Parse AND expressions.
        and_expr -> not_expr ('AND' not_expr)*
        """
        node = self.parse_not()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.eat('AND')
            node = BinOp(node, op, self.parse_not())
        return node

    def parse_not(self):
        """
        Parse unary NOT or fall back to comparisons.
        not_expr -> 'NOT' not_expr | comparison
        """
        if self.current_token.type == 'NOT':
            op = self.current_token
            self.eat('NOT')
            return UnaryOp(op, self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self):
        """
        Parse comparison expressions.
        comparison -> arith_expr (('EQ'|'NE'|'LT'|'LTE'|'GT'|'GTE') arith_expr)?
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
        arith_expr -> term (('PLUS'|'MINUS') term)*
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
        term -> factor (('MUL'|'DIV') factor)*
        """
        node = self.parse_factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        """
        Parse unary operators and primary expressions:
        factor -> ('PLUS'|'MINUS') factor
                | 'INT' | 'FLOAT' | 'BOOLEAN' | 'STRING' | 'INPUT'
                | 'IDENTIFIER'
                | '(' or_expr ')'
        """
        token = self.current_token

        if token.type in ('PLUS', 'MINUS'):  # Unary plus or minus
            self.eat(token.type)
            return UnaryOp(token, self.parse_factor())

        if token.type in ('INT', 'FLOAT'):  # Numeric literals
            self.eat(token.type)
            return Num(token)

        if token.type == 'BOOLEAN':  # Boolean literals
            self.eat('BOOLEAN')
            return Bool(token)

        if token.type == 'STRING':  # String literals
            self.eat('STRING')
            return String(token)

        if token.type == 'INPUT':  # input() call
            self.eat('INPUT')
            self.eat('LPAREN')
            self.eat('RPAREN')
            return InputExpr()

        if token.type == 'IDENTIFIER':  # Variable access
            var_name = token.value
            self.eat('IDENTIFIER')
            return VarAccess(var_name)

        if token.type == 'LPAREN':  # Parenthesized expression
            self.eat('LPAREN')
            node = self.parse_or()
            self.eat('RPAREN')
            return node

        self.error('Unexpected token')

# Quick interactive test when running this file directly
if __name__ == '__main__':
    from lexer import Lexer
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
