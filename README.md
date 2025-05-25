README: My Interpreter Project (Stages 1 to 5)
Hi! This is my programming language interpreter that I built step-by-step as part of my course work. It supports arithmetic, booleans, strings, variables, control flow, and user input.

What It Does
Stage 1: Basic arithmetic like addition, subtraction, multiplication, division, and parentheses.

Stage 2: Boolean logic (true, false, and, or, not) and comparisons (==, >, <, etc.).

Stage 3: Text strings with double quotes, string concatenation, and repetition.

Stage 4: Variables, assignment, and print statements for storing and displaying values.

Stage 5: Control flow with if statements (including else), while loops, and user input with input().

How It Works
The lexer breaks your input code into tokens — like words and symbols.
The parser turns those tokens into a structured representation called an Abstract Syntax Tree (AST).
The interpreter walks the AST to execute your code: calculating expressions, storing variables, running loops, printing output, and reading input.

How To Use It
Run the interpreter by typing

python interpreter.py
in your terminal or command prompt.

Type your code or expressions and press Enter.
Use exit or quit to leave the interpreter.

Examples for All Stages:

Stage 1: Basic Arithmetic
3 + 4
10 - 2 * 3
(5 + 6) * 2
100 / 5
-7 + 8

Stage 2: Boolean Logic and Comparisons
true and false
not false
5 > 3
10 == 10
(4 <= 5) or false

Stage 3: Strings and Concatenation
"hello" + " world"
"repeat" * 3
"foo" + 123
"newline:\n" + "yes"

Stage 4: Variables, Assignment, and Printing
x = 10 + 5;
y = "hello ";
z = y + "world";
print x;
print z;
w = x * 2;
print w;

Stage 5: Control Flow and Input
x = 2;
while (x > 0) {
    print x;
    x = x - 1;
}
if (x == 0) {
    print "Blast off!";
} else {
    print "Counting down...";
}
print "Enter your name:";
name = input();
print "Hello, " + name;

Thanks for checking out my interpreter project! Feel free to reach out if you want to see the code or have questions.