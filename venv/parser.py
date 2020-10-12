from lex import l

file_path = "input.txt"

file = open(file_path, 'r')

status = []

for token in l.lex(file.read()):
    switch = {
        'VAR_NAME' : VarState(token.value)
    }


def VarState(value)
