from lex import l
from project_parser import ParserBoi

file_path = "parser_text_input.txt"

file = open(file_path, 'r')

for token in l.lex(file.read()):
    print("{}       {}".format(token,token.source_pos))

p = ParserBoi(file_path)
p.parse(True)
p.show_declared_vars()
p.restart()
p.parse(False)


