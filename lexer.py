class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    
    def __repr__(self):                        # object represented as a string.
        return f'Token({self.type}, {self.value})'


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
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token('NUMBER', float(result))   # Converts the string to a float and returns a NUMBER token with that value.

    def get_next_token(self):                   # main method to return the next token from input.
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            
            if self.current_char == '*':
                self.advance()
                return Token('STAR', '*')
            
            if self.current_char == '/':
                self.advance()
                return Token('SLASH', '/')
            
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            
            # Collect consecutive invalid characters into one string
            invalid_chars = ''
            while self.current_char is not None and not self.current_char.isspace() and not self.current_char.isdigit() and self.current_char not in '+-*/()':
                invalid_chars += self.current_char
                self.advance()
            
            if invalid_chars:
                raise Exception(f'Invalid characters: {invalid_chars}')

        return Token('EOF', None)

if __name__ == '__main__':
    text = input('Enter expression: ')
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()