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

def block(tokenStatus):
    originalStatus = tokenStatus
    print("<block> -> <statement>")
    tokenStatus = statement(tokenStatus)

    if tokenStatus.getCurrentToken() != None:
        print("<block> -> <statement> <block>")
        block(tokenStatus)
    return tokenStatus

def statement(tokenStatus):
    originalStatus = tokenStatus
    print("<statement> -> <print_statement>")
    tokenStatus = print_statement(tokenStatus)
    if tokenStatus != originalStatus:
        return tokenStatus
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


def int_expression(tokenStatus):
    originalStatus = tokenStatus

    if tokenStatus.getCurrentToken().name == 'INTEGER_LITERAL':
        tokenStatus = tokensStaus.goNext()
    else:
        return originalStatus

    if tokenStatus.getCurrentToken.name == 'LPAREN':
        #INSERT LOGIC TO GET THE STUFF INBETWEEN
        if tokenStatus.getNextToken().name != 'RPAREN':
            raise Exception("No RPAREN")

    return int_expression(tokenStatus)


'''
def bool_expression(tokenStatus):
    originalStatus = tokenStatus
    name = tokenStatus.getCurrentToken().name

    if name  == 'BOOLEAN_LITERAL':
        tokenStatus = tokenStatus.goNext()
        return tokenStatus
    else:
        return originalStatus

    if name == 'INTEGER_LITERAL':
        tokenStatus = tokenStatus.goNext()
        #MAY BE ABLE TO USE RELOP STATEMENT INSIDE THIS INSTEAD OF DOING AN IF THING
        relop()
    else:
        return originalStatus

#SPACE FOR RELOP STUFF IF TOO LAZY TO FIGURE OUT IF I CAN USE RELOP FUNCTION
    if name == '
'''

def arithmetic_op(tokenStatus):
    name = tokenStatus.getCurrentToken().name
    if (name == 'PLUS' or name == 'MINUS' or name == 'DIVISION' or name == 'MULTIPLICATION' or name = 'MODULO'):
        tokenStatus = tokenStatus.goNext()

    return tokenStatus

def relop(tokenStatus):
    name = tokenStatus.getCurrentToken().name
    if(name == 'GREATER_THEN' or name == 'LESS_THEN' or name == 'GREATER_EQUAL' or name == 'LESS_EQUAL')
        tokenStatus = tokenStatus.goNext()

    return tokenStatus

#<assignment_statement> -> <Var_Name>:= <expression>
def assignment_statement(tokenStatus):
    originalStatus = tokenStatus
    name = tokenStatus.getCurrentToken().name
    if(name = 'ASSIGNMENT')
        tokenStatus = string_expression(tokenStatus)
        if(tokenStatus == originalStatus)
            unexpected_char_exception(tokenStatus, "<string_expression>")
        '''
        tokenStatus = bool_expression(tokenStatus)
        if(tokenStatus == originalStatus)
            unexpected_char_exception(tokenStatus, "<bool_expression>")

        tokenStatus = int_expression(tokenStatus)
        if(tokenStatus == originalStatus)
            unexpected_char_exception(tokenStatus, "<int_expression>")

        tokenStatus = float_expression(tokenStatus)
        if(tokenStatus == originalStatus)
            unexpected_char_exception(tokenStatus, "<float_expression>")
        '''
def unexpected_char_exception(tokenStatus, expected):
    raise Exception("Expected '" + expected + "' at " + str(tokenStatus.getCurrentToken().source_pos) + ", received '" + tokenStatus.getCurrentToken().value + "'")

block(status)