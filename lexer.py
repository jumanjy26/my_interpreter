# Token type constants
TT_INT     = 'INT'
TT_FLOAT   = 'FLOAT'
TT_PLUS    = 'PLUS'
TT_MINUS   = 'MINUS'
TT_MUL     = 'MUL'
TT_DIV     = 'DIV'
TT_LPAREN  = 'LPAREN'
TT_RPAREN  = 'RPAREN'
TT_BOOLEAN = 'BOOLEAN'
TT_AND     = 'AND'
TT_OR      = 'OR'
TT_NOT     = 'NOT'
TT_EQ      = 'EQ'    # ==
TT_NE      = 'NE'    # !=
TT_LT      = 'LT'    # <
TT_LTE     = 'LTE'   # <=
TT_GT      = 'GT'    # >
TT_GTE     = 'GTE'   # >=
TT_IDENTIFIER = 'IDENTIFIER'
TT_EOF     = 'EOF'

KEYWORDS = {
    'true': TT_BOOLEAN,
    'false': TT_BOOLEAN,
    'and': TT_AND,
    'or': TT_OR,
    'not': TT_NOT,
}

DIGITS = '0123456789'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):                        # object represented as a string.
        if self.value is not None:
            return f'Token({self.type}, {self.value})'
        return f'Token({self.type})'

class Lexer:                                    # creating lexer class
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
    
    def advance(self):
        self.pos += 1                           # moves the position forward by one character.
        if self.pos >= len(self.text):
            self.current_char = None            # if the end of the text is reached.
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):                  # skips over spaces, tabs, newlines etc. 
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):                           # reads consecutive digits and decimal points to form full numeric literals.
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            result += self.current_char
            self.advance()
        if result.startswith('.') or result.endswith('.'):
            raise Exception(f"Malformed number '{result}'")
        if dot_count == 0:
            return Token(TT_INT, int(result))   # Converts string to int if no dot.
        else:
            return Token(TT_FLOAT, float(result))   # Else float.

    def make_identifier(self):                  # read keywords and identifiers
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        token_type = KEYWORDS.get(id_str.lower(), TT_IDENTIFIER)
        value = None
        if token_type == TT_BOOLEAN:
            value = True if id_str.lower() == 'true' else False
        return Token(token_type, value)

    def get_next_token(self):                   # main method to return the next token from input.
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.make_identifier()
            
            if self.current_char == '+':
                self.advance()
                return Token(TT_PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TT_MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(TT_MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TT_DIV, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(TT_LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TT_RPAREN, ')')
            
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TT_EQ, '==')
                else:
                    raise Exception("Single '=' not supported")
            
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TT_NE, '!=')
                else:
                    raise Exception("Expected '=' after '!'")
            
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TT_LTE, '<=')
                else:
                    return Token(TT_LT, '<')
            
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TT_GTE, '>=')
                else:
                    return Token(TT_GT, '>')

            # Collect consecutive invalid characters into one string
            invalid_chars = ''
            while self.current_char is not None and not self.current_char.isspace() and not self.current_char.isdigit() and not self.current_char.isalpha() and self.current_char not in '+-*/()=!<>':
                invalid_chars += self.current_char
                self.advance()
            
            if invalid_chars:
                raise Exception(f'Invalid characters: {invalid_chars}')

        return Token(TT_EOF, None)

if __name__ == '__main__':
    while True:
        try:
            text = input('Enter expression: ')
            if not text:
                continue
            lexer = Lexer(text)
            token = lexer.get_next_token()
            while token.type != TT_EOF:
                print(token)
                token = lexer.get_next_token()
        except Exception as e:
            print(f"Error: {e}")
