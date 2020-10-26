from lex import l
import TokenStatus as ts

file_path = "parser_text_input.txt"

file = open(file_path, 'r')

status = []

tokens = list(l.lex(file.read()))
# for token in tokens:
#     print(token.value)
# tokens = list(l.lex('Put_Line("Gaming"); Put_Line("More Gaming"); Put_Line("Surprise Surprise, " & "Yet More Gaming" & ", Wouldn\'t you know it");'))
status = ts.TokenStatus(tokens)

#block needs some way to exit; isn't end all be all of all code
def block(tokenStatus):
    originalStatus = tokenStatus
    print("<block> -> <statement>")
    tokenStatus = statement(tokenStatus)

    try:
        tokenStatus.getCurrentToken()
    except(Exception):
        print("Reached end of file")
        return tokenStatus

    # if tokenStatus.getCurrentToken() != None:
    print("<block> -> <statement> <block>")
    block(tokenStatus)
    return tokenStatus

def statement(tokenStatus):
    originalStatus = tokenStatus

    print("<statement> -> <print_statement>")
    tokenStatus = print_statement(tokenStatus)
    if tokenStatus != originalStatus:
        return tokenStatus

    print("<statement> -> <declaration_statement>")
    tokenStatus = declaration_statement(tokenStatus)
    if tokenStatus != originalStatus:
        return tokenStatus

    raise Exception("Unrecognized Statement Type at " + str(originalStatus.getCurrentToken().source_pos))

# <print_statement> -> Put_Line ( <string_expression> ) ;
def print_statement(tokenStatus):
    originalStatus = tokenStatus
    # Checking if the first token is putline
    if tokenStatus.getCurrentToken().name == 'PRINT':
        tokenStatus = tokenStatus.goNext()
        print("<print_statement> -> Put_Line ( <string_expression> ) ;")
    else:
        print("Expected 'Put_Line', did not receive it, must not be print statment")
        return originalStatus

    # checking if the second token is left parentheses
    if tokenStatus.getCurrentToken().name == 'LPAREN':
        tokenStatus = tokenStatus.goNext()
    else:
        unexpected_char_exception(tokenStatus, "(")

    # checking if the third-plus token is a string expression
    priorTokenStatus = tokenStatus
    tokenStatus = string_expression(tokenStatus)
    if tokenStatus == priorTokenStatus:
        unexpected_char_exception(tokenStatus, "<string_expression>")

    # checking if the fourth token is a right parentheses
    if tokenStatus.getCurrentToken().name == 'RPAREN':
        tokenStatus = tokenStatus.goNext()
    else:
        unexpected_char_exception(tokenStatus, ")")

    # checking if the final token is a semicolon
    if tokenStatus.getCurrentToken().name == 'END_INSTRUCTION':
        return tokenStatus.goNext()
    else:
        unexpected_char_exception(tokenStatus, ";")

# <declaration statement> -> <Var_Name> : <Type_Name> ; | <Var_Name> : <Type_Name> := <expression> ;
def declaration_statement(tokenStatus):
    originalStatus = tokenStatus

    #Checks that the first token is a variable
    if tokenStatus.getCurrentToken().name == 'VAR_NAME':
        tokenStatus = tokenStatus.goNext()
    else:
        print("No variable name, must not be declaration statement")
        return originalStatus

    #Checks that the next token is a colon
    if tokenStatus.getCurrentToken().name == 'TYPE_DECLARATION':
        tokenStatus = tokenStatus.goNext()
    else:
        return originalStatus

    # Checks for if the next token is a typename
    priorTokenStatus = tokenStatus
    tokenStatus = type_name(tokenStatus)
    if tokenStatus == priorTokenStatus:
        unexpected_char_exception(tokenStatus, "<TYPE_NAME>")

    # checks if the next token is either a semicolon (done) or a walrus
    if tokenStatus.getCurrentToken().name == "END_INSTRUCTION":
        print("<declaration_statement> -> <var_name> : <type_name> ;")
        return tokenStatus.goNext()
    elif tokenStatus.getCurrentToken().name == "ASSIGNMENT_OPERATOR":
        print("<declaration_statement> -> <var_name> : <typename> := <expression> ;")
        tokenStatus = tokenStatus.goNext()
    else:
        unexpected_char_exception(tokenStatus, "';' or ':='")

    # Expression must be checked based on the typename

    return tokenStatus


def type_name(tokenStatus):
    name = tokenStatus.getCurrentToken().name
    if name == 'FLOAT_TYPENAME' or \
            name == 'INTEGER_TYPENAME' or \
            name == 'STRING_TYPENAME' or \
            name == 'CHARACTER_TYPENAME' or \
            name == 'BOOLEAN_TYPENAME':
        return tokenStatus.goNext()
    else:
        return tokenStatus

# <string expression> -> <string> | <string> & <string expression>
def string_expression(tokenStatus):
    originalStatus = tokenStatus
    # first ensures that the first token is a string literal
    # WILL NEED TO ADD CHECKING IF IT IS A VARIABLE WITH A STRING VALUE ATTACHED
    if tokenStatus.getCurrentToken().name == 'STRING_LITERAL':
        tokenStatus = tokenStatus.goNext()
    else:
        return originalStatus

    # checks if the next character is an ampersand (concatenation)
    if tokenStatus.getCurrentToken().name == 'CONCATENATION':
        # concatenating, next token must also be string_expression
        tokenStatus = tokenStatus.goNext()
        print("<string_expression> -> " + originalStatus.getCurrentToken().value + " & <string_expression>")
    else:
        print("<string_expression> -> " + originalStatus.getCurrentToken().value)
        return tokenStatus

    # now must have another string expression next, recursing
    return string_expression(tokenStatus)

def arithmetic_op(tokenStatus):
    name = tokenStatus.getCurrentToken().name
    if (name == 'PLUS' or name == 'MINUS' or name == 'DIVISION' or name == 'MULTIPLICATION'):
        tokenStatus = tokenStatus.goNext()

    return tokenStatus

def unexpected_char_exception(tokenStatus, expected):
    raise Exception("Expected '" + expected + "' at " + str(tokenStatus.getCurrentToken().source_pos) + ", received '" + tokenStatus.getCurrentToken().value + "'")

block(status)