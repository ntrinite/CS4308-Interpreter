from lex import l

file_path = "input.txt"

file = open(file_path, 'r')

for token in l.lex(file.read()):
    print("{}       {}".format(token,token.source_pos))


