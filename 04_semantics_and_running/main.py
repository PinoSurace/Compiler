#!/usr/bin/env python3

from ply import yacc
import popl_lex # previous phase example snippet code
from tree_print import treeprint

from semantics_common import SemData

from semantics_check import check_semantics

from semantics_run import run_program


# tokens are defined in lex-module, but needed here also in syntax rules
tokens = popl_lex.tokens

class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr


# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors

#program ::= codeitem { codeitem }
def p_program1(p):
    '''program : codeitem'''
    p[0] = ASTnode('program')
    p[0].children_codeitems = [p[1]]
    #print( 'program' )

def p_program2(p):
    '''program : program codeitem'''
    p[0] = p[1]
    p[0].children_codeitems.append(p[2])


#codeitem ::= var_definition | func_definition | statement_seq
def p_codeitem(p):
    '''codeitem : var_definition
                | func_definition
                | statement_seq'''
    p[0] = p[1]
   #print( 'codeitem' )

#var_definition ::= VAR varIDENT IS expr SEMICOLON
def p_var_definition(p):
    '''var_definition : VAR varIDENT IS expr SEMICOLON'''
    #print( 'var_definition( '+p[2]+' )' )
    p[0] = ASTnode('var_definition')
    #p[0].child_var_name = p[2]
    p[0].child_var_name = ASTnode('identifier')
    p[0].child_var_name.value = p[2]
    p[0].child_value = p[4]


#func_definition ::= FUNCTION funcIDENT LPAREN [ formals ] RPAREN fbody
def p_func_definition1(p):
    '''func_definition : FUNCTION funcIDENT LPAREN formals RPAREN fbody'''
    #print( 'func_definition( ' +p[2]+ ' )' )
    p[0] = ASTnode('func_definition')
    p[0].child_func_name = ASTnode('identifier')
    p[0].child_func_name.value = p[2]
    p[0].child_func_body = p[6]
    p[0].child_func_params = p[4]


def p_func_definition2(p):
    '''func_definition : FUNCTION funcIDENT LPAREN empty RPAREN fbody'''
    # print( 'func_definition( ' +p[2]+ ' )' )
    p[0] = ASTnode('func_definition')
    p[0].child_func_name =  ASTnode('identifier')
    p[0].child_func_name.value = p[2]
    p[0].child_func_body = p[6]

#formals ::= varIDENT { COMMA varIDENT }
def p_formals1(p):
    '''formals : varIDENT'''
    #print( 'formals' )
    p[0] = ASTnode('formals')
    node = ASTnode('identifier')
    node.value = p[1]
    p[0].children_args = []
    p[0].children_args.append(node)

def p_formals2(p):
    '''formals : formals COMMA varIDENT'''
    #print( 'formals' )
    p[0] = p[1]
    node = ASTnode('identifier')
    node.value = p[3]
    p[0].children_args.append(node)


#fbody ::= RARROW statement_seq END SEMICOLON
def p_fbody(p):
    '''fbody : RARROW statement_seq END SEMICOLON'''
    #print( 'fbody' )
    p[0] = p[2]

#statement_seq ::= statement SEMICOLON { statement SEMICOLON }
def p_statement_seq1(p):
    '''statement_seq : statement SEMICOLON'''
    #print( 'statement_seq' )
    p[0] = ASTnode('statement_seq')
    p[0].children_statements = [p[1]]

def p_statement_seq2(p):
    '''statement_seq : statement_seq statement SEMICOLON'''
    #print( 'statement_seq' )
    p[0] = p[1]
    p[0].children_statements.append(p[2])


#statement ::= assignment | return_statement | **if_statement**
#            | **while_statement** | **function_call**
def p_statement(p):
    '''statement : assignment
                 | return_statement
                 | if_statement
                 | while_statement
                 | do_while_statement
                 | function_call'''
    #print( 'statement' )
    p[0] = p[1]

#return_statement ::= RETURN expr
def p_return_statement(p):
    '''return_statement : RETURN expr'''
    #print( 'return_statement' )
    p[0] = ASTnode('return_statement')
    p[0].child_value = p[2]

#assignment ::= varIDENT [ DOT varIDENT ] LARROW expr
def p_assignment1(p):
    '''assignment : varIDENT DOT varIDENT LARROW expr'''
    #print( 'assignment( '+p[1]+' )' )
    p[0]  = ASTnode('assignment')
    #p[0].children_op = [p[1]]
    #p[0].children_var.append(p[3])
    p[0].child_var = ASTnode('binary_op')
    p[0].child_var.value = p[2]
    p[0].child_var.child_idx1 = ASTnode('identifier')
    p[0].child_var.child_idx1.value = p[1]
    p[0].child_var.child_idx2 = ASTnode('attribute')
    p[0].child_var.child_idx2.value = p[3]
    p[0].child_value = p[5]


def p_assignment2(p):
    '''assignment : varIDENT empty LARROW expr'''
    #print( 'assignment( '+p[1]+' )' )
    p[0] = ASTnode('assignment')
    p[0].child_var = ASTnode('identifier')
    p[0].child_var.value = p[1]
    p[0].child_value = p[4]

#expr ::= simple_expr [ ( EQ | NOTEQ | LT | LTEQ | GT | GTEQ ) simple_expr ]
def p_expr1(p):
    '''expr : simple_expr'''
    p[0] = p[1]
    #print( 'expr' )

def p_expr2(p):
    '''expr : simple_expr EQ simple_expr
            | simple_expr NOTEQ simple_expr
            | simple_expr LT simple_expr
            | simple_expr LTEQ simple_expr
            | simple_expr GT simple_expr
            | simple_expr GTEQ simple_expr'''
    #p[0] = ASTnode('expr')
    #p[0].child_op = p[2]
    #p[0].children_simple_expr =[p[1]]
    #p[0].children_simple_expr.append(p[3])
    p[0] = ASTnode('binary_op')
    p[0].value = p[2]
    p[0].child_idx1 = p[1]
    p[0].child_idx2 = p[3]

#simple_expr ::= term { ( PLUS | MINUS ) term }
def p_simple_expr1(p):
    '''simple_expr : term'''
    p[0] = p[1]
    #p[0] = ASTnode('simple_expr')
    #p[0].children_terms = [p[1]]
    #print( 'simple_expr' )

def p_simple_expr2(p):
    '''simple_expr : simple_expr PLUS term
                   | simple_expr MINUS term'''
    #print( 'simple_expr' )
    #p[0] = p[1]
    #p[0].children_terms.append(p[3])
    #p[0].child_op = p[2]
    p[0] = ASTnode('binary_op')
    p[0].value = p[2]
    p[0].child_idx1 = p[1]
    p[0].child_idx2 = p[3]


#term ::= factor { ( MULT | DIV ) factor }
def p_term1(p):
    '''term : simple_term'''
    p[0] = p[1]

    #print( 'term' )
    #p[0] = ASTnode('term')
    #p[0].children_simple_terms = [p[1]]

def p_term2(p):
    '''term : term  MULT  simple_term
            | term  DIV  simple_term'''
    #print( 'term' )
    #p[0] = p[1]
    #p[0].children_simple_terms.append(p[3])
    #p[0].child_op = p[2]
    p[0] = ASTnode('binary_op')
    p[0].value = p[2]
    p[0].child_idx1 = p[1]
    p[0].child_idx2 = p[3]

def p_simple_term1(p):
    '''simple_term : factor'''
    p[0] = p[1]
    #p[0] = ASTnode('simple_term')
    #p[0].children_factors = [p[1]]

def p_simple_term2(p):
    '''simple_term : simple_term  POW  factor'''
    p[0] = ASTnode('binary_op')
    p[0].value = p[2]
    p[0].child_idx1 = p[1]
    p[0].child_idx2 = p[3]

#factor ::= [ MINUS ] atom
def p_factor1(p):
    '''factor : MINUS atom'''
    p[0] = ASTnode('unary_op')
    p[0].child_atom = p[2]
    p[0].value = p[1]
    #print( 'factor' )

def p_factor2(p):
    '''factor : empty atom'''
    p[0] = p[2]

#atom ::= NUMBER_LITERAL | DAY_LITERAL | STRING_LITERAL
#       | varIDENT [ APOSTROPHE varIDENT ]
#       | **function_call** | LPAREN expr RPAREN
def p_atom1(p):
    '''atom : function_call
            | LPAREN expr RPAREN'''

    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]
    #print('atom( ' + str(p[1]) + ' )')

def p_atom2(p):
    '''atom : NUMBER_LITERAL
            | DAY_LITERAL
            | STRING_LITERAL'''

    p[0] = ASTnode('literal')
    p[0].value = p[1]


def p_atom3(p):
    '''atom :  varIDENT APOSTROPHE varIDENT
            | varIDENT empty'''

    if len(p) == 4:
        p[0] = ASTnode('binary_op')
        p[0].value = p[2]
        p[0].child_idx1 = ASTnode('identifier')
        p[0].child_idx1.value = p[1]
        p[0].child_idx2 = ASTnode('attribute')
        p[0].child_idx2.value = p[3]

    else:
        p[0] = ASTnode('identifier')
        p[0].value = p[1]


#** function_call ** is either just a function name (funcIDENT) or
#function name followed by one or more comma-separated argument expressions
#inside parenthesis.
def p_function_call(p):
    '''function_call : funcIDENT
                     | funcIDENT LPAREN comma_sep_expr RPAREN'''
    #print( 'function_call' )
    p[0] = ASTnode('function_call')
    p[0].child_func_name = ASTnode('identifier')
    p[0].child_func_name.value = p[1]

    if len(p) == 5:
        p[0].child_args = p[3]



def p_comma_sep_expr1(p):
    '''comma_sep_expr : expr'''
    p[0] = ASTnode('comma_sep_expr')
    p[0].children_expr = [p[1]]

def p_comma_sep_expr2(p):
    '''comma_sep_expr : comma_sep_expr COMMA expr'''
    p[0] = p[1]
    p[0].children_expr.append(p[3])

#** if_statement ** begins with keyword IF, followed by a condition,
#which is any expression. Then comes keyword THEN, followed by a
#sequence of statements. Finally there can be an else-part which begins
#with keyword ELSE, again followed by a sequence of statements.
#The if statement always ends with keyword ENDIF.
def p_if_statement(p):
    '''if_statement : IF expr THEN statement_seq ENDIF
                    | IF expr THEN statement_seq ELSE statement_seq ENDIF'''
    #print( 'if_statement' )
    p[0] = ASTnode('if_statement')
    p[0].child_condition = p[2]
    p[0].child_then = p[4]

    if len(p) == 8:
        p[0].child_else = p[6]

#** while_statement ** begins with keyword WHILE, followed by a condition,
#which is any expression. Loop body begins with keyword DO, followed by a
#sequence of statements. Loop body always ends with keyword ENDWHILE.
def p_while_statement(p):
    '''while_statement : WHILE expr loop_body'''
    #print( 'while_statement' )
    p[0] = ASTnode('while_statement')
    p[0].child_condition = p[2]
    p[0].child_loop_body = p[3]

def p_do_while_statement(p):
    '''do_while_statement : DO statement_seq WHILE expr'''
    #print( 'do_while_statement' )
    p[0] = ASTnode('do_while_statement')
    p[0].child_condition = p[4]
    p[0].child_loop_body = p[2]

def p_loop_body(p):
    '''loop_body : DO statement_seq ENDWHILE'''
    #print('loop_body')
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass




# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( str(p.lineno)+':Syntax Error (token: \''+ str(p.value) + "\')" )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    arg_parser.add_argument('--tree', action='store_true', help='print syntax tree before semantic checks')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print('246258 Joonas Jäppinen')
        print('262767 Pino Surace')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=popl_lex.lexer, debug=False)
        if ns.tree == True:
          treeprint(ast_tree, outformat)

        semdata = SemData()
        check_semantics(ast_tree, semdata)
        if semdata.errors:
            print("Semantic errors:")
            for err in semdata.errors:
                print(err)
        else:
            print("Semantics ok, running:")
            run_program(ast_tree, semdata)






