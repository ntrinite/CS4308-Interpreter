import rply as rp;

lg = rp.LexerGenerator()

lg.add('NUMBER', r'\d+')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')

lg.ignore(r'\s+')
l = lg.build()

for token in l.lex('256 - 12 + 15'):
    print(token)
git