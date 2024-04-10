from flask import Flask, render_template, request
from analyzer.mLexicalAnalyzer import LexicalAnalyzer
from analizert import Parser
import config

app = Flask('__name__')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods = ['POST'])
def enviar():
    code = request.form['code']
    
    parser = Parser()
    _parser = parser.parse_input(code)
    lexical = LexicalAnalyzer()
    lexical.analyzer(code)
    _lexical = lexical.states_list
    print(code)
    return render_template('index.html', _lexical = _lexical, _code = code, _parser = _parser)

if __name__ == '__main__':
    app.run(debug = True)