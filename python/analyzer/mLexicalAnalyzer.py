import ply.lex as lex

class LexicalAnalyzer:
    #tokens = []
    def __init__(self):
        # Tokens
        self.tokens = ['ID', 'RESERVED', 'MAIN', 'RETURN','DATA_TYPE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
                       'PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'EQUAL', 'EQUAL_EQUAL', 'MINUS_MINUS', 'PLUS_PLUS',
                       'LESS_THAN','GREATER_THAN', 'EXCLAMATION', 'QUESTION','IMPORT', 'FIMPORT', 'INTEGER', 'FLOAT', 
                       'SEMICOLON', 'PERIOD', 'COLON', 'COMMA', 'FUNCTION_TYPE', 'STATIC', 'LOGIC',
                       'CCOMILLAS',#'SCOMILLAS', 'CCOMILLAS', 
                       'SSTRING', 'CSTRING', 'EQUAL_LESS_THAN','EQUAL_GREATER_THAN','NOEQUAL']

        # Expresiones Regulares
        #self.t_DATA_TYPE = r'\b(int|float|string|bool|char)\b'
        self.t_LPAREN = r'\('
        self.t_RPAREN = r'\)'
        self.t_LBRACKET = r'\['
        self.t_RBRACKET = r'\]'
        self.t_LBRACE = r'\{'
        self.t_RBRACE = r'\}'
        self.t_MINUS_MINUS = r'--'
        self.t_PLUS_PLUS = r'\+\+'
        self.t_EQUAL_EQUAL = r'=='
        self.t_LESS_THAN = r'<'
        self.t_GREATER_THAN = r'>'
        self.t_EQUAL_LESS_THAN = r'=<'
        self.t_EQUAL_GREATER_THAN = r'>='
        self.t_EXCLAMATION = r'!'
        self.t_QUESTION = r'\?'
        self.t_PLUS = r'\+'
        self.t_MINUS = r'-'
        self.t_TIMES = r'\*'
        self.t_DIVIDE = r'/'
        self.t_NOEQUAL = r'!='
        self.t_EQUAL = r'='
        self.t_SEMICOLON = r';'
        self.t_COMMA = r','
        self.t_PERIOD = r'\.'
        self.t_COLON = r':'
        self.t_SSTRING = r"'[^']*'"
        self.t_CSTRING = r'"[^"]*"'
        #self.t_SCOMILLAS = r"'"
        self.t_CCOMILLAS = r'"[^"]*"'

        self.reserved = {
            #Rerserved
            'public': 'RESERVED',
            'for': 'RESERVED',
            'while': 'RESERVED',
            'print': 'RESERVED',
            'println': 'RESERVED',
            'out': 'RESERVED',
            'System': 'RESERVED',
            'private': 'RESERVED',
            'protect': 'RESERVED',
            'if': 'RESERVED',
            'else': 'RESERVED',
            'do': 'RESERVED',
            'input': 'RESERVED',
            'class': 'RESERVED',

            'main': 'MAIN',
            #Palabras especiales
            'return': 'RETURN',
            
            #static
            'static': 'STATIC',
            
            #LOGIC
            'and': 'LOGIC',
            'or': 'LOGIC',
            'not': 'LOGIC',
            #Import
            'from': 'FIMPORT',
            'import': 'IMPORT',
            'args': 'RESERVED',
            
            #Data type
            'void': 'FUNCTION_TYPE',
            'var': 'DATA_TYPE',
            'const': 'DATA_TYPE',
            'let': 'DATA_TYPE',
            'int': 'FUNCTION_TYPE',
            'float': 'DATA_TYPE',
            'String': 'DATA_TYPE',
            'char': 'DATA_TYPE',
            'double': 'DATA_TYPE'
        }

        # VARIABLES PARA GUARDAR
        self.states_list = []
        self.current_line = 1

        # Instancia del analizador léxico de ply
        self.lexer = lex.lex(module=self)

    def t_ID(self, t):
        r'\b(main|HolaMundo|([a-zA-Z]|_)\w*)\b'
        t.type = self.reserved.get(t.value, 'ID')
        return t
    
    def t_FLOAT(self, t):
        r'\b\d+\.\d+\b'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\b\d+\b'
        t.value = int(t.value)
        return t

    t_ignore = ' \t'

    def t_error(self, t):
        if t.value[0] != '\n':
            self._state_list("Caracter ilegal", t.value[0], self.current_line)
        else:
            self.current_line += 1
        t.lexer.skip(1)

    def _state_list(self, token, lexema, linea):
        token = token.replace('_', ' ')
        self.states_list.append({"token": token, "lexema": lexema, "linea": linea})

    def analyzer(self, data):
        self.lexer.input(data)
        while True:
            token = self.lexer.token()
            if not token:
                break
            self._state_list(token.type, token.value, self.current_line)

    def delete(self):
        self.states_list = []
        self.current_line = 1

