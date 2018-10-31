#!/usr/bin/env python3

from ply import yacc
import popl_lex # previous phase example snippet code

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = popl_lex.tokens

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors

#program ::= codeitem { codeitem }
def p_program(p):
    '''program : codeitem
               | program codeitem'''
    #print( 'program' )

#codeitem ::= var_definition | func_definition | statement_seq
def p_codeitem(p):
    '''codeitem : var_definition
                | func_definition
                | statement_seq'''
   #print( 'codeitem' )

#var_definition ::= VAR varIDENT IS expr SEMICOLON
def p_var_definition(p):
    '''var_definition : VAR varIDENT IS expr SEMICOLON'''
    print( 'var_definition( '+p[2]+' )' )

#func_definition ::= FUNCTION funcIDENT LPAREN [ formals ] RPAREN fbody
def p_func_definition(p):
    '''func_definition : FUNCTION funcIDENT LPAREN formals RPAREN fbody
                       | FUNCTION funcIDENT LPAREN empty RPAREN fbody'''
    print( 'func_definition( ' +p[2]+ ' )' )

#formals ::= varIDENT { COMMA varIDENT }
def p_formals(p):
    '''formals : varIDENT
               | varIDENT COMMA varIDENT
               | formals COMMA varIDENT'''
    #print( 'formals' )

#fbody ::= RARROW statement_seq END SEMICOLON
def p_fbody(p):
    '''fbody : RARROW statement_seq END SEMICOLON'''
    #print( 'fbody' )

#statement_seq ::= statement SEMICOLON { statement SEMICOLON }
def p_statement_seq(p):
    '''statement_seq : statement SEMICOLON
                     | statement_seq statement SEMICOLON'''
    print( 'statement_seq' )


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

#return_statement ::= RETURN expr
def p_return_statement(p):
    '''return_statement : RETURN expr'''
    print( 'return_statement' )

#assignment ::= varIDENT [ DOT varIDENT ] LARROW expr
def p_assignment(p):
    '''assignment : varIDENT DOT varIDENT LARROW expr
                  | varIDENT empty LARROW expr'''
    print( 'assignment( '+p[1]+' )' )

#expr ::= simple_expr [ ( EQ | NOTEQ | LT | LTEQ | GT | GTEQ ) simple_expr ]
def p_expr(p):
    '''expr : simple_expr
            | simple_expr EQ simple_expr
            | simple_expr NOTEQ simple_expr
            | simple_expr LT simple_expr
            | simple_expr LTEQ simple_expr
            | simple_expr GT simple_expr
            | simple_expr GTEQ simple_expr'''
    print( 'expr' )

#simple_expr ::= term { ( PLUS | MINUS ) term }
def p_simple_expr(p):
    '''simple_expr : term
                   | term PLUS term
                   | term MINUS term
                   | simple_expr PLUS term
                   | simple_expr MINUS term'''
    #print( 'simple_expr' )


#term ::= factor { ( MULT | DIV ) factor }
def p_term(p):
    '''term : simple_term
            | simple_term  MULT  simple_term
            | simple_term  DIV  simple_term
            | term  MULT  simple_term
            | term  DIV  simple_term'''
    print( 'term' )

def p_simple_term(p):
    '''simple_term : factor
                   | factor  POW  factor
                   | simple_term  POW  factor'''


#factor ::= [ MINUS ] atom
def p_factor(p):
    '''factor : MINUS atom
              | empty atom'''
    print( 'factor' )


#atom ::= NUMBER_LITERAL | DAY_LITERAL | STRING_LITERAL
#       | varIDENT [ APOSTROPHE varIDENT ]
#       | **function_call** | LPAREN expr RPAREN
def p_atom_1(p):
    '''atom : NUMBER_LITERAL
            | DAY_LITERAL
            | STRING_LITERAL
            | varIDENT empty'''

    print('atom( ' + str(p[1]) + ' )')


def p_atom_2(p):
    '''atom :  varIDENT APOSTROPHE varIDENT
            | function_call
            | LPAREN expr RPAREN'''

    print('atom')
    




#** function_call ** is either just a function name (funcIDENT) or
#function name followed by one or more comma-separated argument expressions
#inside parenthesis.
def p_function_call(p):
    '''function_call : funcIDENT
                     | funcIDENT LPAREN comma_sep_expr RPAREN'''
    print( 'function_call' )



def p_comma_sep_expr(p):
    '''comma_sep_expr : expr
                      | comma_sep_expr COMMA expr'''
    #print('comma_sep_expr')

#** if_statement ** begins with keyword IF, followed by a condition,
#which is any expression. Then comes keyword THEN, followed by a
#sequence of statements. Finally there can be an else-part which begins
#with keyword ELSE, again followed by a sequence of statements.
#The if statement always ends with keyword ENDIF.
def p_if_statement(p):
    '''if_statement : IF expr THEN statement_seq ENDIF
                    | IF expr THEN statement_seq ELSE statement_seq ENDIF'''
    print( 'if_statement' )


#** while_statement ** begins with keyword WHILE, followed by a condition,
#which is any expression. Loop body begins with keyword DO, followed by a
#sequence of statements. Loop body always ends with keyword ENDWHILE.
def p_while_statement(p):
    '''while_statement : WHILE expr loop_body'''
    print( 'while_statement' )

def p_do_while_statement(p):
    '''do_while_statement : DO statement_seq WHILE expr'''
    print( 'do_while_statement' )

def p_loop_body(p):
    '''loop_body : DO statement_seq ENDWHILE'''
    #print('loop_body')

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
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('246258 Joonas Jäppinen')
        print('262767 Pino Surace')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=popl_lex.lexer, debug=False)
        #if result is None:
        #    print( 'syntax OK' )

