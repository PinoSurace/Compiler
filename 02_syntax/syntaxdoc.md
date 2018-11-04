# TIE-20306 Principles of Programming Languages, autumn 2018 / PoPL_phase2

## Questions

### 1. What is syntax analysis and how is it related to other parts in compilation?
Syntax analysis is the process of parsing the input symbols and check if they respect the formal grammar
defined by the programming language.
It is executed after the lexical analysis and before the interpretation process.

### 2. How is the syntactic structure of the language expressed in the PLY tool? I.e., what parts are
### needed in the code and how are they related to syntactic rules of the language?
It is expressed as a set of rules that define the grammar of the programming language. Rules are defined
using python functions, that take p as parameter. If the syntax of the program doesn’t match the rules,
an error is raised.
### 3. Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form):
#### a. Variable definitions:
Variable definition begins with keyword VAR, followed by a variable name (varIDENT).
Then there is the keyword IS followed by an expression and at the end there is the SEMICOLON
#### b. Function definitions
Function definition begins with keyword FUNCTION, followed by a function name
(funcIDENT). Then there are formals between RPAREN and RPARENT snf at the end the
function body that starts with RARROW followed by a statement sequence and end with
the keyword END and the semicolon.
#### c. Assignment
Assignment starts with a variable name (varIDENT) either followed by DOT varIDENT or
nothing. It ends with LARROW followed by an expression.
#### d. Expressions
Expression consists of wither just a simple expression or a simple expression followed by
one between the keywords EQ,NOTEQ,LT, LTEQ, GT, GTEQ and another simple
expression.
### 4. Answer the following based on the syntax definition:
#### e. Is it possible to have an assignment where you assign try to assign to a function
instead of a variable? Why?No it is not possible, because in the assignment only varIdent and combination of it are
allowed.
#### f.Is it possible to have a function definition with no statements (i.e. empty function
body)? Why?
No , the body is mandatory and it is filled with the following elements: RARROW
statement_seq END SEMICOLON
#### g. Does this syntax suffer from the "dangling else" problem (see course material)? Why?
No, because there is the ENDIF word that indentify the end of if/if else statements, so it is
always known to which if statement the else statement is referred.
h. Are the following allowed by the syntax: xx--yy and --xx? Why?
Xx - - yy is allowed by the syntax because it is considered as subtraction between two
terms:
Xx - - yy --> atom(Xx) MINUS MINUS yy --> factor MINUS MINUS atom(yy) --> term MINUS
MINUS atom(yy) --> term MINUS factor --> term MINUS term --> simple_expr
- - xx is not allowed because MINUS factor is not allowed in the syntax.
#### i. Is the following allowed by the syntax: 1 <= xx <= 3? Why?
No, because it is only allowed to have <= only between two simple_expr and it this case it
would be:
Simple_expr LEQ simple_expr LEQ simple_expr -->
Expr LEQ simple_expr --> not allowed.
#### j. How is it ensured that addition/subtraction are done after multiplication/division?
Addition/subtraction are made between terms, and terms consist of multiplication/division
of factors, so it is not possible that addition/subtraction are made before
multiplication/division.
### 5. Did you implement any extras? If so explain them (what and how)
Yes, the extra parts are:
• Define and accept new loop structure: DO ... WHILE expr;
This has been done using a simple rule in the syntax check.
• Define and accept x ** y (x to the power y) which has higher priority
than multiplication and division
This has been done defining the rule POW in the lexer that matches the
‘**’ and adding another rule that matches POW before MULT and DIV.6. 

### What did you think of this assignment? What was difficult? What was easy? Did you learn
anything useful?
I think this assignment is really good to learn the different phases of compilation process. Moreover
dealing with different problem caused from errors, made us really understand things.
