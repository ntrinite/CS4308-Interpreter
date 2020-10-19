from lex import l

file_path = "input.txt"

file = open(file_path, 'r')

status = []

tokens = l.lex(file.read())
currentTokenIndex = 0

# def block(nextToken)
#     print("<block> -> <statement>")
#     nextToken = statement(nextToken)
#
#     if nextToken != None:
#         print("<block> -> <statement> <block>")
#         valid block(nextToken)
#     return valid
#
# def statement(nextToken):
#     return True
#
# def arithmetic_op(nextToken):
#     name = tokens[currentTokenIndex].name
#     if (name == 'PLUS' or name == 'MINUS' or name == 'DIVISION' or name == 'MULTIPLICATION'):
#         nextToken
#         return nextToken
#     return nextToken