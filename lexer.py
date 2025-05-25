# lexer.py
# Handles lexical analysis: turning input text into tokens for the parser.

# Token type constants
TT_INT     = 'INT'
TT_FLOAT   = 'FLOAT'
TT_STRING  = 'STRING'
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
TT_EQ      = 'EQ'
TT_NE      = 'NE'
TT_LT      = 'LT'
TT_LTE     = 'LTE'
TT_GT      = 'GT'
TT_GTE     = 'GTE'
TT_IDENTIFIER = 'IDENTIFIER'
TT_ASSIGN  = 'ASSIGN'
TT_SEMI    = 'SEMI'
TT_PRINT   = 'PRINT'
TT_IF      = 'IF'
TT_ELSE    = 'ELSE'
TT_WHILE   = 'WHILE'
TT_INPUT   = 'INPUT'
TT_LBRACE  = 'LBRACE'
TT_RBRACE  = 'RBRACE'
TT_EOF     = 'EOF'

# Keywords for language constructs and boolean values
KEYWORDS = {
    'true': TT_BOOLEAN,
    'false': TT_BOOLEAN,
    'and': TT_AND,
    'or': TT_OR,
    'not': TT_NOT,
    'print': TT_PRINT,
    'if': TT_IF,
    'else': TT_ELSE,
    'while': TT_WHILE,
    'input': TT_INPUT,
}

DIGITS = '0123456789'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f'Token({self.type}, {self.value})'
        return f'Token({self.type})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        # Move to the next character in the input
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Skip whitespace characters
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        # Parse an integer or float literal
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
            return Token(TT_INT, int(result))
        else:
            return Token(TT_FLOAT, float(result))

    def make_identifier(self):      # Parse identifiers and keywords
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        token_type = KEYWORDS.get(id_str.lower(), TT_IDENTIFIER)
        value = id_str if token_type == TT_IDENTIFIER else None
        if token_type == TT_BOOLEAN:
            value = True if id_str.lower() == 'true' else False
        return Token(token_type, value)

    def make_string(self):          # Parse a string literal, supporting basic escape sequences
        self.advance()              # Skip opening quote
        string_value = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == '"':
                    string_value += '"'
                elif self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                else:
                    string_value += '\\' + (self.current_char or '')
                self.advance()
                continue
            string_value += self.current_char
            self.advance()
        if self.current_char != '"':
            raise Exception("Unterminated string literal")
        self.advance()              # Skip closing quote
        return Token(TT_STRING, string_value)

    def get_next_token(self):       # Main lexer logic: returns the next token from the input
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.make_identifier()

            if self.current_char == '"':
                return self.make_string()

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

            if self.current_char == '{':
                self.advance()
                return Token(TT_LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(TT_RBRACE, '}')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TT_EQ, '==')
                else:
                    return Token(TT_ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(TT_SEMI, ';')

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

            raise Exception(f'Invalid character: {self.current_char}')

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