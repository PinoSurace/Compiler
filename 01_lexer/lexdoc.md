1. What is lexical analysis and how is it related to other parts in compilation? 

Lexical analysis is the process of the parsing through the code file and it’s lines of the code. The compilation is done after lexical analysis when the comments and other stuff are parsed away. 

2. How is the lexical structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to lexical rules of the language? 

The needed parts are the  rules (simple or complex) that matches some regex and represent a token defined in the token list. Moreover if a matched regex is not a token then an error is raised.

3. Explain how the following are recognized and handled in your code: 
 a) Keywords 

Keywords are recognized in the rule t_ID .  If the regex matches more than two consecutive uppercase characters, then it checks if the matched word is in the reserved list (where all the keywords are stored)  and if yes returns the token , otherwise returns an error 
 
b) Comments 

Comments are checked using the t_COMMENT rule, that matches code betweed square brackets [ ] and returns the corresponding token. More about this is explained in the part regarding extras. 

Multiline and nested comments are also checked, so the basic case is handled in them. 
 
c) Whitespace between tokens 

Whitespaces are all matched in the rule t_WHITESPACE, and if the character is equal to “\n”, the current line is updated. Nothing is returned. 
 
d) Operators & delimiters (<-, parenthesis, etc.) 

Operators & delimiters are matched as simple tokens, so if the exact string is matched then they return the corresponding code. There are not problems to handle “<-” respect to “<”, because simple tokens are automatically sorted by ply, where the longest regex are checked first. 
 
e) Date literals 

Date literals are recognized by the rule t_DAY_LITERAL. Then the string matched is transformed in date and checks on its value are done using the function strptime. If the value is correct then it returns the corresponding token, otherwise it returns an error 
 
f) Integer literals 

Integer literals are recognized by the simple rule t_NUMBER_LITERAL, that matches a sequence of numbers and transform it in integers, returning the corresponding token. 
 
g) String literals 

String literals are recognized using the rule  t_STRING_LITERAL, that matches characters between two double quotes. The  double quotes are removed using the replace method, and the corresponding token is returned. 
 
h) Function and variable names 

Function names are recognized using the rule t_funcIDENT, that matches the characters corresponding to it and returns the corresponding token. 

Variable names are recognized using the rule t_varIDENT, that matches the characters corresponding to it and returns the corresponding token. 

4. How can the lexer distinguish between the following lexical elements: 
a) Function names & variable names 

Function names start with an uppercase letter (A-Z), instead variable names start with a lowercase letter (a-z) 
 
b) Integer literals & date literals 

Integers are represented as a sequence of integers. Date literals are in the exact form where there are 4 integers followed by (-)  followed by 2 integers, followed by (-), followed by two integers. 
 
c) Keywords & function names 

Keywords are represented as words composed by 2 to 8 uppercase characters, instead in the functions only the first character can be uppercase. 
 
d) Operators < (less than) & <= (less or equal) 

PLY sorts the simple tokens so that longest regex are checked first. In this way “<=” is checked before “<”; so if there is not “= ”after “<”, then only “<” is matched. 
 
e) String literals & variables names 

String literals are represented inside vertical double quotation marks, instead variables name cannot start or end with a double quotation mark. 
 
f) Comments & other code 

Comments are represented between square brackets ([ ]) and the other code is not. 

5. Did you implement any extras? If so explain them (what and how) 
a) Implement comment in a way that it can span multiple lines. 

This has been done matching the “\n” character inside the brackets “[]” 
 
b) Accept nested comments ( [ start [ inside ] out again ] )

This has been implemented using an exclusive state called COMMENT. 

It starts when the first “\[” is matched and there is a variable that keeps memory of the balance between brackets (t.lexer.level): when this variable is equal to zero, that means brackets are balanced and it has matched nested comments, otherwise if the end of the file is matched, then it means that the brackets are not balanced, so it gives an error. 
 
c) Verify that the token recognized as DAY is an actual date. 

This has been done using the following line of code: 

datetime.datetime.strptime( t.value, '%Y-%m-%d').date() 

The function strptime checks if the input is in the isoformat and if the date is not valid it gives an error 

6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful? 

This assignment was very interesting and not too difficult. I think it helped a lot to understand deeply lexical analysis. 

 

 

 
