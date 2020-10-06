from lex import l

file_path = "input.txt"

file = open(file_path, 'r')

for token in l.lex(file.read()):
    print(token)

for token in l.lex("hel2LO <= 1.1 + 2 * lad \"Get utterly destroyed, scrub\""):
    print(token.source_pos)