from rply import LexerGenerator

lg = LexerGenerator()

lg.add('NUMBER', r'\d+(\.\d+)?')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('IFSTATEMENT', r'if')

lg.ignore(r'\s+')
l = lg.build()

for token in l.lex('25.9 - 12 + 15 + 1.7.3'):
    print(token)