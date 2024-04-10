import ply.yacc as yacc
from analyzer.mLexicalAnalyzer import LexicalAnalyzer

# Crear una instancia del analizador léxico
lexer = LexicalAnalyzer()
tokens = lexer.tokens

# Definir las reglas de la gramática
def p_program(p):
    '''program : import_statement'''
    p[0] = p[1]

# Definir las reglas de importacion
def p_import_statement(p):
    '''import_statement : IMPORT ID
                        | IMPORT ID import_statement
                        | FIMPORT ID IMPORT ID
                        | FIMPORT ID IMPORT ID import_statement
                        | function_main'''
    #Si hay una funcion
    if len(p) == 2 :
        p[0] = p[1]
    elif len(p)== 3: # si hay import ID
        p[0] = (p[1], p[2])
    elif len(p) == 4: #si hay import ID import_statement
        p[0] = (p[1], p[2], p[3]) 
    elif len(p) == 5: #si hay from ID import ID
        p[0] = (p[1], p[2], p[3], p[4])
    elif len(p) == 6: #si hay from ID import ID import_statement
        p[0] = (p[1], p[2], p[3], p[4], p[5])

# Definir las reglas del bloque principal
def p_function_main(p):
    '''function_main : function HARUMI MAIN LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE
                     | function VALERIA_Y_AMORES MAIN LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE'''
        
    if len(p) == 13: #si hay function static int ID (parameters){ RETURN exp}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11],  p[12])

# Definir las reglas de las funciones, hay un error conflico aqui   
def p_function(p):
    '''function : STATIC FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RBRACE
                | STATIC FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RBRACE function
                | STATIC FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE
                | STATIC FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE function
                | FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RBRACE
                | FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RBRACE function
                | FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE
                | FUNCTION_TYPE ID LPAREN parameters RPAREN LBRACE moreCode RETURN exp SEMICOLON RBRACE function
                | vars function
                | vars'''
        
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 9: #si hay int ID (parameters){}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
    elif len(p) == 10: #si hay int ID (parameters){ return exp;}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
    elif len(p) == 11: #si hay int ID (parameters){}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])
    elif len(p) == 12: #si hay static int ID (parameters){ return exp;}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])
    elif len(p) == 13: #si hay static int ID (parameters){ return exp;}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12])
    elif len(p) == 14: #si hay static int ID (parameters){ return exp;}
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13])
        
#Gramatica para parameters de una funcion static void main(parameters){}
def p_parameters(p):
    '''parameters : empty
                  | DATA_TYPE ID
                  | DATA_TYPE ID COMMA parameters
                  | DATA_TYPE ID EQUAL exp
                  | DATA_TYPE ID EQUAL exp COMMA parameters
                  | DATA_TYPE ID EQUAL LBRACKET RBRACKET
                  | DATA_TYPE ID EQUAL LBRACKET RBRACKET COMMA parameters
                  '''
    # Manejo de parámetros simples: int hola
    if len(p) == 3:
        p[0] = (p[1], p[2])
    # Manejo de parámetros con coma: int hola, int ci
    elif len(p) == 5 and p[3] == ',':
        p[0] = (p[1], p[2], p[3], p[4])
    # Manejo de parámetros con asignación de valor inicial: int hola = 1
    elif len(p) == 5 and p[3] == '=':
        p[0] = (p[1], p[2], p[3], p[4])
    # Manejo de parámetros con asignación de valor inicial: int hola = 1, int hola...
    elif len(p) == 7 and p[3] == '=' and p[5] == ',':
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])
    # Manejo de parámetros que son arreglos: int se = []
    elif len(p) == 6 and p[4] == '[' and p[5] == ']':
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    # Manejo de parámetros que son arreglos y tienen coma: int se = [], int hola
    elif len(p) == 8 and p[4] == '[' and p[5] == ']' and p[6] == ',':
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 2:
        p[0] = None

#Gramatica para variables var c, ...; o var c = ...
def p_vars_assignment(p):
    '''vars : empty
            | DATA_TYPE ID SEMICOLON
            | DATA_TYPE ID COMMA varsmore
            | DATA_TYPE ID EQUAL exp SEMICOLON
            | DATA_TYPE ID EQUAL exp COMMA varsmore
            | DATA_TYPE ID EQUAL LBRACKET RBRACKET SEMICOLON
            | DATA_TYPE ID EQUAL LBRACKET RBRACKET COMMA varsmore'''
    
    if len(p) == 4: # Manejo de variable int a;
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 5: # Manejo de variable int a, ...
        p[0] = (p[1], p[2], p[3], p[4])
    elif len(p) == 6: # Manejo de variable int a = exp, ...
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 7 : # Manejo de variable int a = [];
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])
    elif len(p) == 8: # Manejo de variable int a = [], ...
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 2:
        p[0] = None
     
#Gramatica para variables ..., c, ... o ..., c = ..., ... 
def p_varsmore_assignment(p):
    '''varsmore : ID SEMICOLON
                | ID COMMA varsmore
                | ID EQUAL exp SEMICOLON
                | ID EQUAL exp COMMA varsmore
                | ID EQUAL LBRACKET RBRACKET SEMICOLON
                | ID EQUAL LBRACKET RBRACKET COMMA varsmore
                  '''
    
    if len(p) == 3: # Manejo de variable ..., a;
        p[0] = (p[1], p[2])
    elif len(p) == 4: # Manejo de variable ..., a, ...
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 5: # Manejo de variable ..., a = exp;
        p[0] = (p[1], p[2], p[3], p[4]) 
    elif len(p) == 6: # Manejo de variable ..., a = exp, ...  o ..., a = [];
        p[0] = (p[1], p[2], p[3], p[4], p[5])    
    elif len(p) == 7: # Manejo de variable ..., a = [], ...
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

#Gramatica para determinar el tipo de valor de una variable int i = exp
def p_exp_number(p):
    '''exp : INTEGER
           | FLOAT
           | CSTRING
           | SSTRING
           | exp PLUS exp
           | exp MINUS exp
           | exp DIVIDE exp
           | exp TIMES exp
           | ID'''
        
    if len(p) == 2:
        p[0] = p[1]
    elif len(p)==3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], p[2], p[3])

#Gramatica para definir mas codigo en una funcion static void main(int i = 0){moreCode}
def p_moreCode(p):
    '''moreCode : statement
                | statement moreCode'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])   

#Gramatica para definir variables en una funcion static void main(int i = 0){vars}
def p_statement_vars(p):
    '''statement : vars'''
    p[0] = p[1]

#Gramatica para la estrucutura de un bucle for, for(int i = 0; i < 2; i++){print(i);}
def p_statement_for(p):
    '''statement : RESERVED LPAREN fvar compare SEMICOLON incdec RPAREN LBRACE moreCode RBRACE'''
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])

#Gramatica para la estrucutura var c = 0; usadas en operadores obligatorios
def p_fvar(p):
    '''fvar : DATA_TYPE ID EQUAL exp SEMICOLON'''
    p[0] = (p[1], p[2], p[3], p[4], p[5])

#Gramatica para la estrucutura de comparacion 1 > 2
def p_compare(p):
    '''compare : exp EQUAL_EQUAL exp
               | exp EQUAL_EQUAL exp LOGIC compare
               | exp LESS_THAN exp
               | exp LESS_THAN exp LOGIC compare
               | exp GREATER_THAN exp
               | exp GREATER_THAN exp LOGIC compare
               | exp EQUAL_LESS_THAN exp
               | exp EQUAL_LESS_THAN exp LOGIC compare
               | exp EQUAL_GREATER_THAN exp
               | exp EQUAL_GREATER_THAN exp LOGIC compare
               | exp NOEQUAL exp
               | exp NOEQUAL exp LOGIC compare'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], p[2], p[3], p[4], p[5])

#Gramatica para la estrucutura de incremento o decremento ID++ o ID--
def p_incdec(p):
    '''incdec : ID PLUS_PLUS
              | ID MINUS_MINUS'''
    p[0] = (p[1], p[2])
    
#Gramatica para la estrucutura de valor
def p_value(p):
    '''value : ID
             | INTEGER
             | FLOAT'''
    p[0] = p[1]
#Gramatica para determinar un vacio
def p_empty(p):
    '''empty :'''
    pass
    
def p_error(p):
    print(p)
    """
    if p:
        resultado = "Error sintactico de tipo {} en el valor {}, se espera otro valor".format( str(p.type),str(p.value))
        print(resultado)
    else:
        resultado = "Error sintactico, el bloque no se ha cerrado '}'"
        print(resultado)
    """
    if p:
        raise SyntaxError("Error sintactico de tipo {} en el valor {}, se espera otro valor".format(str(p.type), str(p.value)))
    else:
        raise SyntaxError("Error sintactico, el bloque principal tiene error, asegurate que tenga la estructura melk main(parametros){codigo}")

# Construir el parser
parser = yacc.yacc()

# Función para analizar una entrada
def parse_input(input_string):
    return parser.parse(input_string)

if __name__ == "__main__":
    input_string = '''
    import x
    int hola(var in){
        var t = in; 
        for(var i = 0; i =< 2; i++){
            for(var i = 0; i =< 2; i++){}
        }
        return "hola mundo";
    }
    harumi main(var c = 0){
        for(var i = 0; i =< 2; i++){}
        return "hola mundo";
        
    }
    '''
    try:
        result = parse_input(input_string)
        print("Resultado:", result)
    except SyntaxError as e:
        print(e)