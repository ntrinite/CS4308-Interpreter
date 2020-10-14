from lex import l

file_path = "input.txt"

file = open(file_path, 'r')

status = []

for token in l.lex(file.read()):
    print(token.name)