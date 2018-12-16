# TIE-20306 Principles of Programming Languages, autumn 2018 / PoPL_phase4

## Overview

* The checks part has been done applying functions to the nodes using the visit_tree already made function, so that checks are done for node types. The run part has been done interpreting the program using an eval_node function that contains if/else statements, so that depending on the node different operations are executed. For both checks and run parts, it has been used a symbol table defined in the semantics_common.py file. Moreover to execute some binary operations another structure defined in the semantics_common.py file has been used, so that through lambda functions the operations are executed. Below is described how all the elements of the semantic are done and it is done taking as reference the levels of implementation and the semantics checks described in the course website.

## Levels of implementation

### 1. Evaluation of expressions consisting of arithmetic expressions and integer literals. Also, calls to built-in function "Print" work for at least integers and strings (can be implemented as a special case so that it's the only function call that works).

* It has been implemented using the function eval_node in the semantic_run.py file. Arithmetic expressions are evaluated calling the lambda function relative to each operator contained in the binary structure defined in the semantic_common.py file. The Print function has been implemented so that when calling the eval_node function, if the nodetype is a function call, if the function name is equal to ‘Print’ then all the arguments of the function are printed. If the print function has not arguments, then just an empty line is printed.

### 2. Additionally, using integer variables works (i.e., definition, assignment, reading the value).

* In the eval_node function, when we have a variable definition node, the name of the variable is added to the symtbl. When we have an assignment, in case we have an attribute then it is supposed to be a date, so the corrispondent method for the date is called and updated (day, month or year), otherwise just the value in the symtbl is updated. The reading value is handled using the “identifier” case, where the variable name is got from the symtbl and returned.

### 3. In addition to integer arithmetic+variables, also date arithmetic (date+int and date-date) work, as well as date and string variables.

* In the eval_node function exceptions are handled using if statements so that if the children of a binary operator are of types date and int or date and date, the operation is done considering them as described in the documentation. Same thing for the aphostrophe operator (‘) and dot operator(.), in fact they are evaluated in a different way, using the date libraries so execute the operations.

### 4. Control structures IF and WHILE, and comparison operators also work.

* Comparison operators are handled as simple binary operators, in the binary structure. IF statement works so that if the condition is true, then the ‘then’ branch is executed, otherwise if there is an ‘else’ branch, it will be evaluated using the eval_node function. WHILE statement works so that if the condition is true, then the loop body is evaluated using the eval_node function. DO_WHILE  statement works so that first the loop body is evaluated using the eval_node function, then if the condition is still true, a while loop as described above is executed.

### 5. In addition to above, function definitions, function calls and parameter passing works.

* As it has been done with variables, also for functions when there is a definition then the information about functions are stored in the symboltable, but nothing is evaluated before the function call. When a function is called, then parameters are stored as normal variables in the symbol table  and the arguments values are assigned to them in the respective order. After that the function body is evaluated.

### 6. Additionally RETURN can be used to return a value and finish the execution of function.

* In the statement_seq node, if the return value is not None, than it means it comes from a function(in fact return value can only be used insde a function and should return something that is not None) so the value is returned and the statement sequence of the function is stopped there.

## Semantic checks

### Names (variables, parameters, and functions)

#### A variable/parameter/function has to be defined before it is used.

* This check has been done so that when a variable or function is defined, variable, function and its parameters are added to the symbol table. If they are used, first it is checked they are in the symbol table otherwise an error is returned.

#### Already defined variable/parameter/function name cannot be defined again.

* In the same way as described above, when a variable or function is defined, first it is checked if it is already in the symbol table and in that case an error is returned, otherwise it will be added to the symbol table.

### Functions

#### Function parameters can only be used inside its own function.

* This has not been implemented.

#### A function call has to have the correct number of parameters (compared to its definition).

* A check is made when a function_call nodetype is encountered. It is checked if the number of parameters saved during the definition of the function is equal to the number of arguments passed during the call. In case they are different then an error is given.

### Other

#### In the form variable'attribute, the attribute has to be one of "day", "month", "year", "isLeapYear?", and "isWorkday?" (or one of your own attributes). Similarly in the form variable.attrbute, the attribute has to be one of "day", "month", and "year".

* A check is made so that when the nodetype is a binary operator  dot or aphostrophe, then the attribute should be one of those listed in the description. In particular, if the operator is the apostrophe then the attribute should be one of "day", "month", "year", "isLeapYear?", and "isWorkday?", instead if the operator is the dot, then the attribute should be one of  "day", "month", and "year".

## Summary of the things completed

### Datatypes (as described in the course webpage)

### Statements (WHILE, IF and DO_WHILE)

### Functions (Pass-by-value and everything as described in the course webpage except for “A function parameter name can be used only inside the respective function.”)

### Built-ins (Print, Input)

## The test file can be found at the following path: /04_test/levels_of_implementation.popl

* This assignment has been very interesting and useful to understand how compilers work and all the phases of compilation. I found this really helpful to understand the theory and it makes the topic more interesting.