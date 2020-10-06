from lex import l

for token in l.lex("hel2LO <= 1.1 + 2 * lad \"Get utterly destroyed, scrub\""):
    print(token)