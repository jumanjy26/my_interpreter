# lexer.py
# Performs lexical analysis: converts input source code text into a stream of tokens.
# Tokens are the basic building blocks (numbers, keywords, operators) for the parser.

# --- Token type (TT) constants ---
# Define all token types that the lexer can produce.
TT_INT     = 'INT'         # Integer literal, e.g., 42
TT_FLOAT   = 'FLOAT'       # Floating-point literal, e.g., 3.14
TT_STRING  = 'STRING'      # String literal enclosed in double quotes
TT_PLUS    = 'PLUS'        # '+' operator
TT_MINUS   = 'MINUS'       # '-' operator
TT_MUL     = 'MUL'         # '*' operator
TT_DIV     = 'DIV'         # '/' operator
TT_LPAREN  = 'LPAREN'      # '(' left parenthesis
TT_RPAREN  = 'RPAREN'      # ')' right parenthesis
TT_BOOLEAN = 'BOOLEAN'     # Boolean literal: true or false
TT_AND     = 'AND'         # Logical AND keyword 'and'
TT_OR      = 'OR'          # Logical OR keyword 'or'
TT_NOT     = 'NOT'         # Logical NOT keyword 'not'
TT_EQ      = 'EQ'          # Equality operator '=='
TT_NE      = 'NE'          # Not-equal operator '!='
TT_LT      = 'LT'          # Less than operator '<'
TT_LTE     = 'LTE'         # Less than or equal '<='
TT_GT      = 'GT'          # Greater than operator '>'
TT_GTE     = 'GTE'         # Greater than or equal '>='
TT_IDENTIFIER = 'IDENTIFIER'  # Variable/function names
TT_ASSIGN  = 'ASSIGN'      # Assignment operator '='
TT_SEMI    = 'SEMI'        # Semicolon ';' statement terminator
TT_PRINT   = 'PRINT'       # 'print' keyword
TT_IF      = 'IF'          # 'if' keyword
TT_ELSE    = 'ELSE'        # 'else' keyword
TT_WHILE   = 'WHILE'       # 'while' keyword
TT_INPUT   = 'INPUT'       # 'input' keyword
TT_LBRACE  = 'LBRACE'      # Left curly brace '{' block start
TT_RBRACE  = 'RBRACE'      # Right curly brace '}' block end
TT_EOF     = 'EOF'         # End-of-file/input token

# Mapping reserved words to their token types
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

DIGITS = '0123456789'  # Allowed digits for numbers

class Token:
    """
    Represents a token produced by the lexer.
    Attributes:
        type: The token's type (one of the TT_* constants)
        value: The literal value of the token (if any), e.g., 42 for INT tokens
    """
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        # Format token for debugging, e.g. Token(INT, 42)
        if self.value is not None:
            return f'Token({self.type}, {self.value})'
        return f'Token({self.type})'

class Lexer:
    """
    The Lexer class reads the input source code character by character,
    producing tokens that the parser will consume.
    """
    def __init__(self, text):
        self.text = text          # Input string to tokenize
        self.pos = 0              # Current position index in text
        self.current_char = self.text[self.pos] if self.text else None  # Current character or None if done

    def advance(self):
        """
        Advance the position pointer by one character.
        Update current_char to new character or None if end reached.
        """
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """
        Skip whitespace characters (space, tab, newline) until
        a non-whitespace character is found or input ends.
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """
        Lex a number literal (integer or floating point).
        Allows digits and a single decimal dot.
        Raises Exception on malformed numbers (e.g., '12.' or '.5').
        Returns a Token of type INT or FLOAT.
        """
        result = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break  # Only one dot allowed
                dot_count += 1
            result += self.current_char
            self.advance()

        # Malformed numbers with leading/trailing dot are invalid
        if result.startswith('.') or result.endswith('.'):
            raise Exception(f"Malformed number '{result}'")

        if dot_count == 0:
            return Token(TT_INT, int(result))
        else:
            return Token(TT_FLOAT, float(result))

    def make_identifier(self):
        """
        Lex an identifier or keyword.
        Identifiers contain letters, digits, or underscores.
        Recognizes reserved keywords by checking KEYWORDS dict.
        Returns appropriate Token.
        """
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()

        token_type = KEYWORDS.get(id_str.lower(), TT_IDENTIFIER)
        value = id_str if token_type == TT_IDENTIFIER else None

        # Convert 'true'/'false' keywords to boolean values
        if token_type == TT_BOOLEAN:
            value = True if id_str.lower() == 'true' else False

        return Token(token_type, value)

    def make_string(self):
        """
        Lex a string literal enclosed in double quotes.
        Supports basic escape sequences: \", \n, \t.
        Raises Exception if string literal is unterminated.
        """
        self.advance()  # Skip opening quote
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
                    # Unknown escape sequence; preserve backslash
                    string_value += '\\' + (self.current_char or '')
                self.advance()
                continue

            string_value += self.current_char
            self.advance()

        if self.current_char != '"':
            raise Exception("Unterminated string literal")

        self.advance()  # Skip closing quote
        return Token(TT_STRING, string_value)

    def get_next_token(self):
        """
        Core method of the lexer.
        Returns the next token found in input.
        Skips whitespace and handles:
            - Numeric literals (ints/floats)
            - Identifiers and keywords
            - String literals
            - Operators and punctuation
            - EOF at end of input
        """
        while self.current_char is not None:
            # Skip any whitespace first
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Number literal
            if self.current_char.isdigit():
                return self.number()

            # Identifier or keyword
            if self.current_char.isalpha():
                return self.make_identifier()

            # String literal
            if self.current_char == '"':
                return self.make_string()

            # Single-character tokens/operators
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

            # Two-character operators or assignment
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

            # Unknown/unexpected character
            raise Exception(f'Invalid character: {self.current_char}')

        # If reached end of input
        return Token(TT_EOF, None)


# Run lexer in interactive mode if executed directly
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