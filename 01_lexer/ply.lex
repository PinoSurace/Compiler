#!/usr/bin/env python3
import sys, ply.lex, datetime

reserved = {
    'VAR' : 'VAR',
    'IS' : 'IS',
    'IF' : 'IF',
    'THEN' : 'THEN',
    'ELSE' : 'ELSE',
    'ENDIF' : 'ENDIF',
    'WHILE' : 'WHILE',
    'DO' : 'DO',
    'ENDWHILE' : 'ENDWHILE',
    'FUNCTION' : 'FUNCTION',
    'RETURN' : 'RETURN'
}

#keywords = ('VAR', 'IS', 'IF', 'THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO', \
#            'ENDWHILE', 'FUNCTION', 'RETURN', 'END')
tokens = [ 'LARROW', 'RARROW', 'LPAREN', 'RPAREN', 'COMMA', 'DOT', 'APOSTROPHE', \
           'SEMICOLON', 'EQ', 'NOTEQ', 'LT', 'LTEQ','GT', 'GTEQ', \
           'PLUS', 'MINUS', 'MULT', 'DIV', 'DAY_LITERAL', 'NUMBER_LITERAL', \
           'STRING_LITERAL', 'varIDENT', 'funcIDENT', 'ID'] + list(reserved.values())

##tokens definition


# non-tokens

#** empty space, tabulator(\t) and newline(\n)/linefeed(\r)
#are accepted but ignored in the input (for each newline
#keep a line count to get better error messages) **
def t_WHITESPACE(t):
    r'[ \t\n\r]+'
    t.lexer.lineno += t.value.count('\n')


#** anything between square brackets [ ]
#are accepted but ignored **
def t_COMMENT(t):
    r'\[(.|\n)*\]'
    t.lexer.lineno += t.value.count('\n')


# reserved words (each identified as a token) are:
#VAR, IS, IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE,
#FUNCTION, RETURN, END
#t_VAR = r'VAR'
#t_IS  = r'IS'
#t_IF  = r'IF'
#t_THEN = r'THEN'
#t_ELSE = r'ELSE'
#t_ENDIF = r'ENDIF'
#t_WHILE = r'WHILE'
#t_DO    = r'DO'
#t_FUNCTION = r'FUNCTION'
#t_RETURN = r'RETURN'
#t_END = r'END'


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
    r'\d\d\d\d-\d\d-\d\d'
    date = t.value.split("-")
    t.value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    #t.value = date.isoformat()
    return t


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

##tokens definition end



def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( t.value[0], t.lexer.lineno ) )

# define lexer in module level so it can be used after 
# importing this module:
lexer = ply.lex.lex(debug = 0)

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
        print( '85471 Jyke Savia' )
        print( '88888 Ahto Simakuutio' )
        print( '------ Joonas Jäppinen')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            # TODO: limit the file size to 100MB?
            data = INFILE.read() 

        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )

