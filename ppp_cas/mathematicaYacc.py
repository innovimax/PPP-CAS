import ply.yacc as yacc
from .mathematicaLex import tokens
from .mathematicaTree import Plus, Minus, Times, Opp, FunctionCall, List, Divide, Diff, Eq, Pow, Id, Fact
from sympy import latex

precedence = (
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'ID'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'UMINUS'),
    ('left', 'UPLUS'),
    ('right', 'POW'),
    ('left', 'EXCL'),
    ('nonassoc', 'RPAREN'),
    ('nonassoc', 'LPAREN'),
    ('nonassoc', 'RBRACE'),
    ('nonassoc', 'LBRACE'),
    ('nonassoc', 'RBRACKET'),
    ('nonassoc', 'LBRACKET'),
    ('nonassoc', 'COMMA'),
)

start = 'expression'

def p_expr_uminus(p):
    '''expression : MINUS expression %prec UMINUS
                    | PLUS expression %prec UPLUS'''
    if p[1]=='-':
        p[0] = Opp(p[2])
    else:
        p[0] = p[2]

def p_expression_arith(p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression POW expression %prec POW
                    | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = Plus(p[1], p[3])
    elif p[2] == '-':
        p[0] = Minus(p[1], p[3])
    elif p[2] == '*':
        p[0] = Times(p[1], p[3])
    elif p[2] == '/':
        p[0] = Divide(p[1], p[3])
    elif p[2] == '^':
        p[0] = Pow(p[1], p[3])
        
def p_expression_fact(p):
    '''expression : expression EXCL'''
    p[0] = Fact(p[1])

def p_expression_term(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_function_call_arg(p):
    '''expression : expression LBRACKET expression_list RBRACKET'''
    p[0] = FunctionCall(p[1], List(p[3]))
    
def p_function_call_arg_diff(p):
    '''expression : expression APOSTROPHE LBRACKET expression_list RBRACKET'''
    p[0] = Diff(FunctionCall(p[1], List(p[4])),1)
    
def p_function_call_arg_diff_diff(p):
    '''expression : expression APOSTROPHE APOSTROPHE LBRACKET expression_list RBRACKET'''
    p[0] = Diff(FunctionCall(p[1], List(p[4])),2)

def p_function_call_empty(p):
    '''expression : expression LBRACKET RBRACKET'''
    p[0] = FunctionCall(p[1], List([]))

def p_expression_list(p):
    '''expression_list : expression'''
    p[0] = List([p[1]])

def p_expression_list_rec(p):
    '''expression_list : expression_list COMMA expression'''
    p[0] = p[1] + List([p[3]])

def p_expression_num(p):
    '''expression : NUMBER'''
    p[0] = Id(p[1])
    
def p_expression_id(p):
    '''expression : ID'''
    p[0] = Id(p[1])
    
def p_list_empty(p):
    '''expression : LBRACE RBRACE'''
    p[0] = List([])
    
def p_list(p):
    '''expression : LBRACE expression_list RBRACE'''
    p[0] = List(p[2])

def p_error(p):
    pass

mathematicaParser = yacc.yacc()
