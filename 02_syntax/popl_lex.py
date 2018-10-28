#!/usr/bin/env python3
import sys, ply.lex, datetime

states = (
  ('COMMENT','exclusive'),
)

# reserved words (each identified as a token) are:
reserved = {
    #'FALSE': 'FALSE',
    #'NONE': 'NONE',
    #'TRUE': 'TRUE',
    #'AND' : 'AND',
    #'AS' : 'AS',
    #'ASSERT' : 'ASSERT',
    #'ASYNC': 'ASYNC',
    #'AWAIT': 'AWAIT',
    #'BREAK': 'BREAK',
    #'CLASS': 'CLASS',
    #'CONTINUE': 'CONTINUE',
    #'DEF': 'DEF',
    #'DEL': 'DEL',
    'DO' : 'DO',
    #'ELIF' : 'ELIF',
    'ELSE' : 'ELSE',
    'END' : 'END',
    'ENDIF' : 'ENDIF',
    'ENDWHILE' : 'ENDWHILE',
    #'EXCEPT' : 'EXCEPT',
    #'FINALLY' : 'FINALLY',
    #'FOR': 'FOR',
    #'FROM': 'FROM',
    'FUNCTION' : 'FUNCTION',
    #'GLOBAL': 'GLOBAL',
    'IF' : 'IF',
    #'IMPORT': 'IMPORT',
    #'IN': 'IN',
    'IS' : 'IS',
    #'LAMBDA': 'LAMBDA',
    #'NONLOCAL': 'NONLOCAL',
    #'NOT': 'NOT',
    #'OR': 'OR',
    #'PASS': 'PASS',
    #'RAISE': 'RAISE',
    'RETURN' : 'RETURN',
    'THEN' : 'THEN',
    #'TRY' : 'TRY',
    'WHILE' : 'WHILE',
    #'WITH': 'WITH',
    'VAR': 'VAR',
    #'YIELD': 'YIELD'

}

#tokens list
tokens = [ 'LARROW', 'RARROW', 'LPAREN', 'RPAREN', 'COMMA', 'DOT', 'APOSTROPHE', \
           'SEMICOLON', 'EQ', 'NOTEQ', 'LT', 'LTEQ','GT', 'GTEQ', \
           'PLUS', 'MINUS', 'MULT', 'DIV', 'DAY_LITERAL', 'NUMBER_LITERAL', \
           'STRING_LITERAL', 'varIDENT', 'funcIDENT', 'ID'] + list(reserved.values())

##tokens definition

#nested comments
def t_COMMENT(t):
    r'\['
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    #print(t.lexer.level)
    t.lexer.begin('COMMENT')
    if(t.lexer.level != 1):
        t_COMMENT_eof()


def t_COMMENT_LBRACKET(t):
    r'\['
    t.lexer.level +=1
    #print(t.lexer.level)

def t_COMMENT_RBRACKET(t):
    r'\]'
    t.lexer.level -=1
    #print(t.lexer.level)
    # If closing brace, return the code fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
         #t.type = "CCODE"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')
         #return t


def t_COMMENT_CONTENT(t):
    r'[^\[\]]+'
    #r'(.|\n)+'
    #print(t.lexer.level)
    pass


def t_COMMENT_eof(t):
    if t.lexer.level != 0:
        raise Exception("Parentesis are not balanced at line {}".format( t.lexer.lineno))

def t_COMMENT_error(t):
    if t.lexer.level != 0:
        raise Exception("Parentesis are not balanced at line {}".format(t.lexer.lineno))


#nested comments end




# non-tokens

#** empty space, tabulator(\t) and newline(\n)/linefeed(\r)
#are accepted but ignored in the input (for each newline
#keep a line count to get better error messages) **
def t_WHITESPACE(t):
    r'[ \t\n\r]+'
    t.lexer.lineno += t.value.count('\n')


#** anything between square brackets [ ]
#are accepted but ignored **
#def t_COMMENT(t):
#    r'\[(.|\n)*?\]'
#    t.lexer.lineno += t.value.count('\n')



# one and two letter tokens:
t_LARROW = r'<-'
t_RARROW = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','
t_DOT    = r'\.'
t_APOSTROPHE = r"\'"
t_SEMICOLON  = r';'

t_EQ    = r'='
t_NOTEQ = r'!='
t_LT    = r'<'
t_LTEQ  = r'<='
t_GT    = r'>'
t_GTEQ  = r'>='
t_PLUS  = r'\+'
t_MINUS = r'\-'
t_MULT  = r'\*'
t_DIV   = r'/'


# longer tokens

#** date in ISO format, four numerical digits followed by minus
#followed by two digits followed by minus followed by
#two digits. E.g. 2018-09-27 ***
def t_DAY_LITERAL(t):
    r'\d\d\d\d-\d\d-\d\d(?!\d)'
    try:
        t.value = datetime.datetime.strptime( t.value, '%Y-%m-%d').date()
        return t
    except ValueError:
        raise Exception("Illegal date format at line '{}'".format( t.lexer.lineno))


#** one or more numerical digits **
def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


#** any number of characters inside vertical double
#quotation marks.  E.g.  "merkkijono" **
def t_STRING_LITERAL(t):
    r'\".*?\"'
    t.value = t.value.replace('"', '')
    return t

#** a variable name starts with a lowercase letter (a-z) and
#must be followed by at least one character in
#set( 'a-z', 'A-Z', '0-9', '_' ). In addition the last
#character can be question mark. NOTE that this does not allow
#one letter variable names. E.g. valid varIDENT:
#ab, iI, i9_abc, a9? **
t_varIDENT = r'[a-z]\w+\?{0,1}'

#** a function name starts with an uppercase letter (A-Z) and
#must be followed by at least one character in
#set( 'a-z', '0-9', '_' ). NOTE that this does not allow
#one letter function names. E.g. valid funcIDENT:
#Foo, J00, S_o_m_e **
t_funcIDENT = r'[A-Z][a-z0-9_]+'

def t_ID(t):
    r'[A-Z][A-Z]+'
    t.type = reserved.get(t.value)    # Check for reserved words
    if t.type == None:
        t_error(t)
    else:
        return t



def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( t.value[0], t.lexer.lineno ) )

# define lexer in module level so it can be used after 
# importing this module:
lexer = ply.lex.lex()

# if this module/file is the first one started (the main module)
# then run:
if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print( '246258 Joonas Jäppinen')
        print('262767 Pino Surace')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            
            data = INFILE.read() 

        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )

