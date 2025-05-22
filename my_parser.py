from lexer import Lexer, Token

class AST:                      #a base “marker” class for all our AST nodes.
    pass

class BinOp(AST):               #represents a binary operation (like left + right).
    def __init__(self, left, op, right):
        self.left = left            ##for ATS node, left
        self.token = self.op = op   #token -a PLUS or STAR.
        self.right = right          #for ATS node, right 
        self.right = right          #for ATS node, right

class Num(AST):                     #number literal.
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):        # enforces that the next token must be of the indicated type.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()              # otherwise we throw a syntax error.

    def factor(self):                 # bare number, which becomes a Num(token)
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Num(token)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node

    def term(self):                 # handles * and /, which bind more tightly than + and –.
        node = self.factor()

        while self.current_token.type in ('STAR', 'SLASH'):
            token = self.current_token
            if token.type == 'STAR':
                self.eat('STAR')
            elif token.type == 'SLASH':
                self.eat('SLASH')

            node = BinOp(left=node, op=token, right=self.factor())

        return node             # returns a subtree that groups all the *// operation

    def expr(self):
        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')

            node = BinOp(left=node, op=token, right=self.term())

        return node

if __name__ == '__main__':
    text = input('Enter expression: ')
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.expr()
    print(ast)