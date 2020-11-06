from rply import LexerGenerator

lg = LexerGenerator()

lg.add("BEGIN_STATEMENT", r"begin")
lg.add("END_STATEMENT", r"end")
lg.add("FLOAT_LITERAL", r"\d+\.\d+")
lg.add("INTEGER_LITERAL", r"[0-9]+")
lg.add("STRING_LITERAL", r"\"[^\"]*\"")
lg.add("CHARACTER_LITERAL", r"\'.\'")
lg.add("BOOLEAN_LITERAL", r"(true)|(false)")
lg.add("FLOAT_TYPENAME", r"Float")
lg.add("INTEGER_TYPENAME", r"Integer")
lg.add("STRING_TYPENAME", r"String")
lg.add("CHARACTER_TYPENAME", r"Character")
lg.add("BOOLEAN_TYPENAME", r"Boolean")
lg.add("PLUS", r"\+")
lg.add("MINUS", r"\-")
lg.add("MULTIPLICATION", r"\*")
lg.add("CONCATENATION", r"&")
lg.add("DIVISION", r"/")
lg.add("MODULO", r"mod")
lg.add("ASSIGNMENT", r":=")
lg.add("TYPE_DECLARATION", r":")
lg.add("EQUALS", r"=")
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("LBRACE", r"\{")
lg.add("RBRACE", r"\}")
lg.add("IF_CONDITIONAL", r"if")
lg.add("THEN_CONDITIONAL", r"then")
lg.add("ELSE", r"else")
lg.add("ELSIF", r"elsif")
lg.add("GREATER_EQUAL", r">=")
lg.add("LESS_EQUAL", r"<=")
lg.add("GREATER_THAN", r">")
lg.add("LESS_THAN", r"<")
lg.add("INEQUAL_TO", r"\\=")
lg.add("EQUAL_TO", r"=")
lg.add("NOT", "not")
lg.add("AND", r"and")
lg.add("XOR", r"xor")
lg.add("OR", r"or")
lg.add("PRINT", r"Put_Line")
lg.add("LOOP_STATEMENT", r"loop")
lg.add("IN", r"in")
lg.add("WHILE_STATEMENT", r"while")
lg.add("END_INSTRUCTION", r";")
lg.add("PROCEDURE_DECLARATION", r"procedure")
lg.add("IS", r"is")
lg.add("APOSTROPHE_OPERATOR", r"\'")
lg.add("DOT_OPERATOR", r"\.")
lg.add("VAR_NAME", r"[a-zA-Z_][a-zA-Z0-9_]*")

#ignores whitespce
lg.ignore(r"\s+")

l = lg.build()


