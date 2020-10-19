from flask import Flask, render_template, request
import ply.lex as lex

app = Flask(__name__)

# Список заявленных имен токенов
tokens = (
    'KEYWORD',
    'IDENTIFIER',
    'HEX_NUMBER',
    'ASSIGN',
    'DELIMITER',
    'COMPARISON'
)

reserved = {'for': 'KEYWORD', 'do': 'KEYWORD'}

# Правила для простых токенов
t_ASSIGN = r'\:\='
t_COMPARISON = r'\<|\>|\='
t_DELIMITER = r'\;|\(|\)'
t_HEX_NUMBER = r'\d+[0-9abcdef]*'


# Правила для токенов с обработкой
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# Правило для подсчета количества строк
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Игнорируем пробелы и табуляции
t_ignore = ' \t'


# Правило для обработки ошибок
def t_error(t):
    print(f"Недопустимая лексема '{t.value[0]}' в строке {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


def lex_analysis(text):
    lexer.input(text)
    for tok in lexer:
        yield tok.value, tok.type


@app.route('/', methods=['GET', 'POST'])
def index():
    prog_text = None
    lex_table = None
    if request.method == 'POST':
        path = request.form['path']
        with open(path) as file, open(path) as mirror:
            prog_text = file.readlines()
            data = mirror.read()
        lex_table = lex_analysis(data)
    return render_template('index.html', prog_text=prog_text, lex_table=lex_table)

