# lexer.py

# Token types for numbers, strings, operators, parentheses, booleans, etc.
TT_INT     = 'INT'
TT_FLOAT   = 'FLOAT'
TT_STRING  = 'STRING'      # Token type for string literals
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

# Keywords mapping for booleans and logical operators
KEYWORDS = {
    'true': TT_BOOLEAN,
    'false': TT_BOOLEAN,
    'and': TT_AND,
    'or': TT_OR,
    'not': TT_NOT,
}

DIGITS = '0123456789'  # Valid digit characters for numbers

class Token:
    def __init__(self, type_, value=None):
        self.type = type_     # Token type (e.g., INT, PLUS, STRING)
        self.value = value    # Optional value (e.g., 123, "hello")
    
    def __repr__(self):
        # Display token nicely for debugging
        if self.value is not None:
            return f'Token({self.type}, {self.value})'
        return f'Token({self.type})'

class Lexer:
    def __init__(self, text):
        self.text = text          # Input text to tokenize
        self.pos = 0              # Current position in text
        self.current_char = self.text[self.pos] if self.text else None  # Current character
    
    def advance(self):
        # Move to next character in input
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        # Skip over whitespace characters like spaces, tabs, newlines
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        # Parse integer or float literals (e.g., 123, 45.67)
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:  # Only one dot allowed in number
                    break
                dot_count += 1
            result += self.current_char
            self.advance()
        if result.startswith('.') or result.endswith('.'):
            raise Exception(f"Malformed number '{result}'")  # Invalid float syntax
        if dot_count == 0:
            return Token(TT_INT, int(result))   # Integer token
        else:
            return Token(TT_FLOAT, float(result))  # Float token

    def make_identifier(self):
        # Parse keywords and identifiers (variable names)
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        token_type = KEYWORDS.get(id_str.lower(), TT_IDENTIFIER)  # Check if keyword
        value = None
        if token_type == TT_BOOLEAN:
            # Convert "true"/"false" to boolean values True/False
            value = True if id_str.lower() == 'true' else False
        return Token(token_type, value)

    def make_string(self):
        # Parse string literals enclosed in double quotes ("...")
        self.advance()  # Skip opening quote
        string_value = ''
        while self.current_char is not None and self.current_char != '"':
            # Handle escape sequences like \" \n \t
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
            raise Exception("Unterminated string literal")  # Missing closing quote
        self.advance()  # Skip closing quote
        return Token(TT_STRING, string_value)

    def get_next_token(self):
        # Main method: get the next token from input
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

            # Operators and punctuation tokens
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

            # Catch invalid characters
            invalid_chars = ''
            while self.current_char is not None and not self.current_char.isspace() and not self.current_char.isdigit() and not self.current_char.isalpha() and self.current_char not in '+-*/()=!<>"':
                invalid_chars += self.current_char
                self.advance()
            
            if invalid_chars:
                raise Exception(f'Invalid characters: {invalid_chars}')

        return Token(TT_EOF, None)  # End of input

if __name__ == '__main__':
    # Simple interactive testing of lexer tokens
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
