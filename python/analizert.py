import ply.yacc as yacc
from analyzer.mLexicalAnalyzer import LexicalAnalyzer

class Parser:
    def __init__(self):
        # Crear una instancia del analizador léxico
        self.lexer = LexicalAnalyzer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    # Definir las reglas de la gramática
    def p_program(self, p):
        '''program : inicio'''
        p[0] = p[1]

    def p_inicio(self, p):
        '''inicio : RESERVED RESERVED ID LBRACE mas RBRACE'''
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

    #mas codigo
    def p_mas(self, p):
        '''mas : code
                | code mas'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2]) 

    def p_segundo(self, p):
        '''code : RESERVED STATIC FUNCTION_TYPE MAIN LPAREN args RPAREN LBRACE pp RBRACE'''
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])

    def p_pp(self, p):
        '''pp : pps'''
        
        p[0] = p[1]

            #mas codigo
    def p_args(self, p):
        '''args : cd
                | cd args'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])

    def p_argumento(self, p):
        '''cd : DATA_TYPE LBRACKET RBRACKET RESERVED'''
        p[0] = (p[1], p[2], p[3], p[4])

    def p_imp(self, p):
        '''pps : RESERVED PERIOD RESERVED PERIOD RESERVED LPAREN CCOMILLAS RPAREN SEMICOLON'''
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
          
    #Gramatica para determinar un vacio
    def p_empty(self, p):
        '''empty :'''
        pass
        
    def p_error(self, p):
        if p:
            raise SyntaxError("Error sintactico de tipo {} en el valor {}, se espera otro valor".format(str(p.type), str(p.value)))
        else:
            raise SyntaxError("Error sintactico, el bloque principal tiene error, asegurate que tenga la estructura  main(parametros){codigo}")

    # Construir el parser
    start = 'program'
    # Función para analizar una entrada
    def parse_input(self, input_string):
        try:
            return self.parser.parse(input_string)
        except SyntaxError as e:
            return e
        
"""
va = '''public class HolaMundo{
    public static void main(String[] args){
        System.out.println("hola m");
	}
}'''

print(va)
par = Parser()

print(par.parse_input(va))

        

"""