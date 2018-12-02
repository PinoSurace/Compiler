# TIE-20306 Principles of Programming Languages, autumn 2018 / PoPL_phase3

## Questions 
### 1. What is an (abstract) syntax tree and how is it related to other parts in compilation? 

* An abstract syntax tree is the parse tree derived from the syntactic structure of the code given as input. It is related to the syntax analysis, in fact it is created using the same rules and it comes before the semantic analysis and interpretation of the code. 

### 2. How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree? 

* It is generated using a set of rules that define the grammar of the programming language and when the rules a matched, nodes and links between the parent node and the children are created. 

* Everything is done using simple python functions, that match the rules and save the elements considering the hierarchy parent/ children nodes. If the syntax of the program doesn’t match the rules, an error is raised. 

### 3. Explain in English what kind of tree is formed in your code from the following syntactic elements: 

* Variable definitions: variable definition is the parent node. The children will be an “identifier” node with the name of the variable and another node with the value of the variable. The link arrows define which node is the var_name and which node is the value. 
* Function definitions: function definition is the parent node. If the function has some parameters then it will have 3 children: function name, function parameters and function body; otherwise it will have only 2: function name and function body.  
 
* Assignment: assignment is the parent node. If we have a simple assignment, then the parent will have a child for the variable name and another for the value assigned; 

* If an attribute of the variable is assigned, then the parent node will have a child represented by the binary operator (.) that has two children, idx1 represent the name of the variable and idx2 represents the name of the attribute. The other child of the parent node will be the value assigned. 

* While-statement: while statement is the parent node. It has two children: the condition node and the loop body node. 

### 4. Answer the following based on the syntax definition and your implementation: 

* In which cases is it possible in your implementation to end up with a tree with empty child attributes (somewhere in the tree there is a place for a child node (or nodes), but there is none)? I.e., in which situations you end up with tree nodes with child_... attribute being None, or children_... attribute being an empty list? 

  * In our implementation it seems there is not possibility to end up with a tree with empty child attributes. 

* Are there places in your implementation where you were able to "simplify" the tree by omitting trivial/non-useful nodes or by collecting a recursive repeating structure into a list of child nodes? 

  * Yes it has been done for the following nodes: -codeitem, fbody, statement, expr, simple_expr, term, simple_term, factor, atom, loop_body. 
  * These elements in the tree are represented by naming the links or omitted using directly their value. In the case of the expressions, terms, factors etc, the nodes have been replaced by the operation between the values, so that the tree becomes easier to understand. 

## What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful? 

* This assignment was really helpful to understand how the parse tree is generated and how it is related to the syntax. 
* This phase was pretty easy even if a bit confusing because there were many ways to do the tree and I hope ours is okay. Moreover I hope there won’t be mistakes related on name of the nodes or name of the links because there was not any guide for that, so it was pretty subjective. 

 

 
