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
