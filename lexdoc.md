Version: 1.0v (Joonas)

Version control: major_edit.minor_edit (editor)

In addition to the lexer code, the group submits a text document in either plain text (.txt), markdown (.md) or pdf (.pdf) format. It should contain answers to the following questions (again, in the groups own words, no copying from other sources):

1. What is lexical analysis and how is it related to other parts in compilation?
Lexical analysis is the part of the process being compiled. The analysis is done after preprocessing of the code (after removal of the whitespaces and any comments). The code (text) is processed and the different words are checked against predefined tokens. Other parts of the compilation can only be done after lexical analysis (partly because before lexical analysis, there is no idea what the programmer has coded).

2. How is the lexical structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to lexical rules of the language?
TODO: The lexical structure of the language is being expressed ...


3. Explain how the following are recognized and handled in your code:
        Keywords
	The keywords are first parsed from the code and later added to a list.

	Comments
	The comments are removed befored the lexical analysis

        Whitespace between tokens
	Whitespace is removed by splitting code lines by whitespace characters and checking the contains of the indexes.

        Operators & delimiters (<-, parenthesis, etc.)
	Currently no plan.

        Date literals
	Date literals are being checked against DD.MM.YYYY, MM.DD.YYYY and YYYY.MM.DD format.

        Integer literals
	Integer literals contain only numbers as characters and are not floats.
	
        String literals
	String literals contain any characters.
	
        Function and variable names 
	Function names have before the name def (shortened from definition). Variables do not have def written and have equal sign '=' after 		the name. 
	
4. How can the lexer distinguish between the following lexical elements:
	Function names & variable names
	Function names have def before them. Function names end before white space. Variable names do not have def written before them.

        Integer literals & date literals
	Integer are inputted containing no whitespaces nor anything else. Date literals can contain dots (.) or slashes (/).

        Keywords & function names
	TODO

        Operators < (less than) & <= (less or equal)
	TODO

        String literals & variables names
	TODO
 
        Comments & other code 
	TODO	

5. Did you implement any extras? If so explain them (what and how)
TODO: We implemented feature(s) X(s).

6. What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?
The assignment was very usefull and improved Python skills even further. The tasks were not difficult nor easy but well educating. The most usefull part was the handling of different tokens. 
