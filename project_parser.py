from lex import l
import TokenStatus as ts
from itertools import chain

# file_path = "wee.txt"
#
# file = open(file_path, 'r')
#
# tokens = list(l.lex(file.read()))
# # for token in tokens:
# #     print(token.value)
# # tokens = list(l.lex('Put_Line("Gaming"); Put_Line("More Gaming"); Put_Line("Surprise Surprise, " & "Yet More Gaming" & ", Wouldn\'t you know it");'))
# status = ts.TokenStatus(tokens)
#
# declared_vars = dict()
#
# parsing = True


class ParserBoi:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, 'r')
        self.tokens = list(l.lex(self.file.read()))
        self.status = ts.TokenStatus(self.tokens)
        self.declared_vars = dict()

    def restart(self):
        self.status = ts.TokenStatus(self.tokens)

    def parse(self, as_parser=True):
        self.block(self.status, as_parser)

    def show_declared_vars(self):
        for i in self.declared_vars:
            print(i, self.declared_vars[i])

    #block needs some way to exit; isn't end all be all of all code
    def block(self, tokenStatus, as_parser = True):
        global parsing
        parsing = as_parser

        originalStatus = tokenStatus
        if parsing:
            print("<block> -> <statement>")
        tokenStatus = self.statement(tokenStatus)



        try:
            tokenStatus.getCurrentToken()
        except(Exception):
            print("\nReached end of file\n")
            return tokenStatus

        # if tokenStatus.getCurrentToken() != None:
        if parsing:
            print("<block> -> <statement> <block>")
        self.block(tokenStatus, as_parser)
        return tokenStatus

    #region Statements

    def statement(self, tokenStatus):
        originalStatus = tokenStatus

        if parsing:
            print("<statement> -> <print_statement>")
        tokenStatus = self.print_statement(tokenStatus)
        if tokenStatus != originalStatus:
            return tokenStatus

        if parsing:
            print("<statement> -> <declaration_statement>")
        tokenStatus = self.declaration_statement(tokenStatus)
        if tokenStatus != originalStatus:
            return tokenStatus

        if parsing:
            print("<statement> -> <assignment_statement>")
        tokenStatus = self.assignment_statement(tokenStatus)
        if tokenStatus != originalStatus:
            return tokenStatus

        raise Exception("Unrecognized Statement Type at " + str(originalStatus.getCurrentToken().source_pos))

    # <print_statement> -> Put_Line ( <string_expression> ) ;
    def print_statement(self, tokenStatus):
        originalStatus = tokenStatus
        # Checking if the first token is putline
        if tokenStatus.getCurrentToken().name == 'PRINT':
            tokenStatus = tokenStatus.goNext()
            if parsing:
                print("<print_statement> -> Put_Line ( <string_expression> ) ;")
        else:
            if parsing:
                print("Expected 'Put_Line', did not receive it, must not be print statment")
            return originalStatus

        # checking if the second token is left parentheses
        if tokenStatus.getCurrentToken().name == 'LPAREN':
            tokenStatus = tokenStatus.goNext()
        else:
            self.unexpected_token_exception(tokenStatus, "(")

        # checking if the third-plus token is a string expression
        priorTokenStatus = tokenStatus
        tokenStatus = self.string_expression(tokenStatus)
        if tokenStatus == priorTokenStatus:
            self.unexpected_token_exception(tokenStatus, "<string_expression>")

        # checking if the fourth token is a right parentheses
        if tokenStatus.getCurrentToken().name == 'RPAREN':
            tokenStatus = tokenStatus.goNext()
        else:
            self.unexpected_token_exception(tokenStatus, ")")

        # checking if the final token is a semicolon
        if tokenStatus.getCurrentToken().name == 'END_INSTRUCTION':
            #Statement valid, executing:
            if not parsing:
                print(tokenStatus.value)

            return tokenStatus.goNext()
        else:
            self.unexpected_token_exception(tokenStatus, ";")

    # <declaration statement> -> <Var_Name> : <Type_Name> ; | <Var_Name> : <Type_Name> := <expression> ;
    def declaration_statement(self, tokenStatus):
        originalStatus = tokenStatus
        #Checks that the first token is a variable
        if tokenStatus.getCurrentToken().name == 'VAR_NAME':
            var_name = tokenStatus.getCurrentToken().value
            tokenStatus = tokenStatus.goNext()
        else:
            if parsing:("No variable name, must not be declaration statement")
            return originalStatus

        #Checks that the next token is a colon
        if tokenStatus.getCurrentToken().name == 'TYPE_DECLARATION':
            tokenStatus = tokenStatus.goNext()
        else:
            return originalStatus

        # Checks for if the next token is a typename
        priorTokenStatus = tokenStatus
        tokenStatus = self.type_name(tokenStatus)
        if tokenStatus == priorTokenStatus:
            self.unexpected_token_exception(tokenStatus, "<TYPE_NAME>")
        var_type = tokenStatus.getPrevToken().value

        #Assigns the default value for its data type to the variable
        self.declared_vars[var_name] = {"type": var_type, "value": self.getDefaultValue(var_type)}


        # checks if the next token is either a semicolon (done) or a walrus (do the partial assignment)
        if tokenStatus.getCurrentToken().name == "END_INSTRUCTION":
            if parsing:
                if parsing:("<declaration_statement> -> VAR_NAME:" + var_name + " : TYPE_NAME:" + var_type + " ;")
            return tokenStatus.goNext()
        elif tokenStatus.getCurrentToken().name == "ASSIGNMENT":
            if parsing:
                print("<declaration_statement> -> VAR_NAME:" + var_name + " : TYPE_NAME:" + var_type + " := <expression> ;")
            #Know assignment_statement will go to the halfway; therefore will either throw error or complete, no change check needed
            tokenStatus = self.assignment_statement(tokenStatus, var_name)
            return tokenStatus
        else:
            self.unexpected_token_exception(tokenStatus, ";")



    def getDefaultValue(self, data_type):
        if (data_type == "String"):
            return None
        elif (data_type == "Integer"):
            return 0
        elif (data_type == "Float"):
            return 0.0
        elif (data_type == "Boolean"):
            return False
        elif (data_type == "Character"):
              return "z"

    # <assignment_statement> -> <Var_Name>:= <expression>
    def assignment_statement(self, tokenStatus, var_name = None):
        originalStatus = tokenStatus

        #when coming out of a declaration statement, this will not be done
        if var_name == None:
            #var_name not assigned, we are not coming out of a declaration statement; must check if the token is a variable name
            if parsing:
                print("<assignment_statement> -> <var_name> := <expression>")
            name = tokenStatus.getCurrentToken().name
            if name != "VAR_NAME":
                return originalStatus
            var_name = tokenStatus.getCurrentToken().value

            #Makes sure the variable has been declared
            try:
                self.declared_vars[var_name]
            except KeyError:
                self.undeclared_variable_exception(tokenStatus)
            tokenStatus = tokenStatus.goNext()

        #Either coming from declaration or had a variable name; now MUST be assignment statement
        if tokenStatus.getCurrentToken().name == "ASSIGNMENT":
            tokenStatus = tokenStatus.goNext()
        else:
            self.unexpected_token_exception(tokenStatus, ":=")

        var_type = self.declared_vars[var_name]["type"]
        # Expression must be checked based on the typename
        priorTokenStatus = tokenStatus
        # if var_type == "Float":
        #     tokenStatus = float_expression(tokenStatus)
        if var_type == "Integer":
            tokenStatus = self.int_expression(tokenStatus, ["END_INSTRUCTION"])
        elif var_type == "String":
            tokenStatus = self.string_expression(tokenStatus)
        elif var_type == "Boolean":
            tokenStatus = self.bool_expression(tokenStatus, ["END_INSTRUCTION"])
        # elif var_type == "Character":
        #     tokenStatus.char_expression(tokenStatus)
        else:
            raise BaseException("Invalid data type!")

        #AFTER ANY EXPRESSION, tokenStatus.value SHOULD BE EQUAL TO WHAT THE EXPRESSION EVALUATES AS
        if tokenStatus == priorTokenStatus:
            self.unexpected_token_exception(tokenStatus, "<" + var_type + ">")

        #Updates the stored value of the variables
        self.declared_vars[var_name] = {"type": var_type, "value":  tokenStatus.value}


        if tokenStatus.getCurrentToken().name == "END_INSTRUCTION":
            return tokenStatus.goNext()
        else:
            self.unexpected_token_exception(tokenStatus, ";")

    #endregion

    #region Expressions
    #AFTER ANY EXPRESSION, tokenStatus.value SHOULD BE EQUAL TO WHAT THE EXPRESSION EVALUATES AS

    # <string expression> -> <string> | <string> & <string expression>
    def string_expression(self, tokenStatus):
        originalStatus = tokenStatus
        string = None
        # first ensures that the first token is a string literal
        # WILL NEED TO ADD CHECKING IF IT IS A VARIABLE WITH A STRING VALUE ATTACHED
        if tokenStatus.getCurrentToken().name == 'STRING_LITERAL':
            string = tokenStatus.getCurrentToken().value.replace("\"", "")
            tokenStatus = tokenStatus.goNext()
        elif tokenStatus.getCurrentToken().name == 'VAR_NAME':
            try:
                var = self.declared_vars[tokenStatus.getCurrentToken().value]
                var = self.declared_vars[tokenStatus.getCurrentToken().value]
            except KeyError:
                self.undeclared_variable_exception(tokenStatus)
            if var["type"] == "String":
                string = var["value"]
                tokenStatus = tokenStatus.goNext()
            else:
                return originalStatus
        # If converting from number into string
        # Might add floats later
        elif tokenStatus.getCurrentToken().name in ['INTEGER_TYPENAME', 'FLOAT_TYPENAME', 'BOOLEAN_TYPENAME']:
            try:
                type = tokenStatus.getCurrentToken().name
                tokenStatus.expect(["APOSTROPHE_OPERATOR"])
                tokenStatus = tokenStatus.goNext()
            except Exception:
                return originalStatus

            #Have used the apostrophe operator, now it MUST be a string conversion
            tokenStatus.expect(['IMAGE'])
            tokenStatus = tokenStatus.goNext()
            tokenStatus.expect(["LPAREN"])
            tokenStatus = tokenStatus.goNext()
            priorTokenStatus = tokenStatus
            if type == "INTEGER_TYPENAME":
                tokenStatus = self.int_expression(tokenStatus, expectedTerminals="RPAREN")
            elif type == "BOOLEAN_TYPENAME":
                tokenStatus = self.bool_expression(tokenStatus, expectedTerminals="RPAREN")
            if priorTokenStatus == tokenStatus:
                self.unexpected_token_exception(tokenStatus, "<int_expression>")
            string = str(tokenStatus.value)
            if parsing:
                print("<string_expression> -> " + type + "'Image(<num_expression>)")
        else:
            return originalStatus

        # checks if the next character is an ampersand (concatenation)
        if tokenStatus.getCurrentToken().name == 'CONCATENATION':
            # concatenating, next token must also be string_expression
            tokenStatus = tokenStatus.goNext()
            if parsing:
                print("<string_expression> -> " + originalStatus.getCurrentToken().value + " & <string_expression>")
        else:
            tokenStatus.value = string
            if parsing:
                print("<string_expression> -> " + originalStatus.getCurrentToken().value)
            return tokenStatus

        # now must have another string expression next, recursing
        tokenStatus = self.string_expression(tokenStatus)
        tokenStatus.value = (string + tokenStatus.value)
        return tokenStatus

    # <int_expression> -> (<Integer_Literal> | <Integer_Var>) [<Arithmetic_Op> <int_expression>]
    def int_expression(self, tokenStatus, expectedTerminals, useStack = True):
        """

        :param tokenStatus: general iterator
        :param expectedTerminals: list of strings to stop the evaluation on
        :param useStack: bool, must be set to false on internal recursion, true otherwise
        :return: modified tokenStatus
        """
        originalStatus = tokenStatus
        lhs = "<int_expression> -> "
        try:
            expressionTokens = self.getTokensTillTerminal(tokenStatus, expectedTerminals, useStack)
        except Exception:
            return originalStatus

        # Paren are acceptable becuase it implies returning from another int_expression, which will leave the parenthese
        acceptableNumberTypes = ["VAR_NAME", "INTEGER_LITERAL", "LPAREN"]
        unary = self.unary_arithmetic_op_names[0]

        #chain.from_iterable converts from being nested to all being in the base level of a list; allows 'in'
        #to check if in list
        binary = list(chain.from_iterable(self.binary_arithmetic_op_names))
        binaryOrEnd = list(binary).extend(expectedTerminals)
        ops = []
        nums = []
        num_strings = []

        #Checks if it should convert any binary minuses into unary negatives
        pastFirstToken = False
        tempStatus = tokenStatus
        for i in expressionTokens:
            if i.name == "MINUS" and (not pastFirstToken or not tempStatus.getPrevToken().name in acceptableNumberTypes):
                i.name = "NEGATIVE"
            pastFirstToken = True
            tempStatus = tempStatus.goNext()

        pastFirstToken = False
        while tokenStatus.getCurrentToken() in expressionTokens:
            if tokenStatus.getCurrentToken().name in unary:
                if not tokenStatus.getNextTokenNotIn(unary).name in acceptableNumberTypes:
                    self.unaccepted_operand_exception(tokenStatus.getCurrentToken(), [tokenStatus.getNextTokenNotIn(unary)])
                else:
                    ops.append(tokenStatus.getCurrentToken())
                    if parsing:
                        print("<int_expression> -> <unary_arithmetic_op>")
                        print("<unary_arithmetic_op> -> " + tokenStatus.getCurrentToken().name)
            elif tokenStatus.getCurrentToken().name in binary:
                if not pastFirstToken:
                    Exception("Operator '" + tokenStatus.getCurrentToken().value + "' not unary")
                elif (not tokenStatus.getPrevToken().name in acceptableNumberTypes and tokenStatus.getPrevToken().name != "RPAREN") \
                    or not tokenStatus.getNextTokenNotIn(unary).name in acceptableNumberTypes:
                        self.unaccepted_operand_exception(tokenStatus.getCurrentToken(), [tokenStatus.getPrevToken(), tokenStatus.getNextToken()])
                ops.append(tokenStatus.getCurrentToken())
                if parsing:
                    print("<int_expression> -> <binary_arithmetic_op>")
                    print("<binary_arithmetic_op> -> " + tokenStatus.getCurrentToken().name)
            elif tokenStatus.getCurrentToken().name == "VAR_NAME":
                try:
                    if self.declared_vars[tokenStatus.getCurrentToken().value]["type"] != "Integer":
                        self.incorrect_variable_type_exception(tokenStatus, "<Integer>")
                    val = self.declared_vars[tokenStatus.getCurrentToken().value]["value"]
                    nums.append(val)
                    num_strings.append(str(val))
                    tokenStatus.expect(binaryOrEnd)
                    if parsing:
                        print("<int_expression> -> VAR_NAME:" + tokenStatus.getCurrentToken().value +":" + self.declared_vars[tokenStatus.getCurrentToken().value]["type"] + ":" + str(self.declared_vars[tokenStatus.getCurrentToken().value]["value"]))
                except Exception:
                    self.undeclared_variable_exception(tokenStatus)
            elif tokenStatus.getCurrentToken().name == "INTEGER_LITERAL":
                nums.append(int(tokenStatus.getCurrentToken().value))
                num_strings.append(tokenStatus.getCurrentToken().value)
                tokenStatus.expect(binaryOrEnd)
                if parsing:
                    print("<int_expression> -> INTEGER_LITERAL:" + tokenStatus.getCurrentToken().value)
            elif tokenStatus.getCurrentToken().name == "LPAREN":
                tokenStatus = tokenStatus.goNext()
                currentToken = tokenStatus.getCurrentToken()
                priorStatus = tokenStatus
                if parsing:
                    print("<int_expression> -> ( <int_expression> )")
                tokenStatus = self.int_expression(tokenStatus, ["RPAREN"], False)
                if tokenStatus == priorStatus:
                    self.unexpected_token_exception(priorStatus, "<int_expression>")

                nums.append(tokenStatus.value)
                num_strings.append(tokenStatus.message)
                tokenStatus.expect(binaryOrEnd)
            elif not pastFirstToken:
                currentToken = tokenStatus.getCurrentToken()
                if parsing:
                    print("Unexpected token, must not be int_expression")
                return originalStatus
            else:
                self.unexpected_token_exception(tokenStatus, "<Integer>")

            tokenStatus = tokenStatus.goNext()

        #All unary ops are in all_arithmetic ops first, will be executed first(for now)
        #going to track tree by using a mirroring list
        for opType in self.all_arithmetic_op_names:
            numsIndex = 0
            for op in ops:
                if op.name in opType:
                    if op.name in unary:
                        nums[numsIndex] = self.calculate(nums[numsIndex], None, op.name)
                        num_strings[numsIndex] = op.value + "(" + num_strings[numsIndex] + ")"
                    else:
                        nums[numsIndex] = self.calculate(nums[numsIndex], nums[numsIndex + 1], op.name)
                        nums.remove(nums[numsIndex + 1])
                        num_strings[numsIndex] = op.value + "(" + num_strings[numsIndex] + "," + num_strings[numsIndex + 1] + ")"
                        num_strings.remove(num_strings[numsIndex + 1])
                elif op.name in binary:
                    numsIndex += 1
            for op in ops:
                if op.name in opType:
                    ops.remove(op)

        if len(nums) > 1:
            raise Exception("Incorrect number of arguments!")
        tokenStatus.value = nums[0]
        tokenStatus.message = num_strings[0]
        if parsing:
            print(lhs + num_strings[0])
        tokenStatus.expect(None)
        return tokenStatus

    # <boolean> -> [!](<boolean_literal> | <boolean_var> | <int_expression> <relop> <int_expression>)
    def boolean(self, tokenStatus, expectedTerminals):
        originalStatus = tokenStatus

        lhs = "<boolean> -> "
        hasNot = False
        if (tokenStatus.getCurrentToken().name == "NOT"):
            hasNot = True
            tokenStatus = tokenStatus.goNext()
            lhs = lhs + "not "

        #Checks the next token for literal, variable, or int_expression
        if tokenStatus.getCurrentToken().name == "BOOLEAN_LITERAL":
            if tokenStatus.getCurrentToken().value == "false":
                tokenStatus.value = False
            else:
                tokenStatus.value = True
            if parsing:
                print(lhs + "BOOLEAN_LITERAL:" + tokenStatus.getCurrentToken().value)
            message = tokenStatus.getCurrentToken().value
            tokenStatus = tokenStatus.goNext()

        elif tokenStatus.getCurrentToken().name == "VAR_NAME":
            try:
                if self.declared_vars[tokenStatus.getCurrentToken().value]["type"] == "Boolean":
                    tokenStatus.value = bool(self.declared_vars[tokenStatus.getCurrentToken().value]["value"])
                    message = self.declared_vars[tokenStatus.getCurrentToken().value]["value"]
                    tokenStatus = tokenStatus.goNext()
                else:
                    self.incorrect_variable_type_exception(tokenStatus, "<Boolean>")
            except:
                self.undeclared_variable_exception(tokenStatus)
        elif tokenStatus.getCurrentToken().name == "LPAREN":
            tokenStatus = tokenStatus.goNext()
            priorStatus = tokenStatus
            if parsing:
                print(lhs + " (<bool_expression>)")
            tokenStatus = self.bool_expression(tokenStatus, ["LPAREN"])
            message = tokenStatus.message
            if tokenStatus == priorStatus:
                self.unexpected_token_exception(tokenStatus, "<bool_expression>")
            tokenStatus.expect(["RPAREN"])
            tokenStatus = tokenStatus.goNext()
        else:
            # Tries to parse as int_expression
            priorStatus = tokenStatus
            relops = list(chain.from_iterable(self.binary_relational_op_names))
            if parsing:
                print(lhs + "<int_expression> <relop> <int_expression>")
            tokenStatus = self.int_expression(tokenStatus, relops)
            if tokenStatus == priorStatus:
                return originalStatus

            firstVal = tokenStatus.value
            message = tokenStatus.message
            op = tokenStatus.getCurrentToken().name
            if tokenStatus.getCurrentToken().name not in relops:
                self.unexpected_token_exception(tokenStatus, relops)
            if parsing:
                print("<relop> -> " + op)
            tokenStatus = tokenStatus.goNext()
            priorStatus = tokenStatus
            tokenStatus = self.int_expression(tokenStatus, expectedTerminals)
            if tokenStatus == priorStatus:
                self.unexpected_token_exception(tokenStatus, "<int_expression>")
            secondVal = tokenStatus.value
            tokenStatus.value = self.calculate_relop(firstVal, secondVal, op)
            message = op + "(" + message + "," + tokenStatus.message + ")"

        #Nots that value if it is present
        if hasNot:
            tokenStatus.value = self.calculate_boolop(tokenStatus.value, None, "NOT")
            message = "NOT(" + message + ")"

        tokenStatus.message = message
        return tokenStatus

    def bool_expression(self, tokenStatus, expectedTerminals):
        originalStatus = tokenStatus
        lhs = "<bool_expression> -> "
        if parsing:
            print("<bool_expression> -> <boolean>")
        logop = list(chain.from_iterable(self.binary_logical_op_names))
        firstTerminals = logop
        firstTerminals.extend(expectedTerminals)
        tokenStatus = self.boolean(tokenStatus, firstTerminals)
        val1 = tokenStatus.value
        message = tokenStatus.message
        if tokenStatus == originalStatus:
            return originalStatus

        logop = list(chain.from_iterable(self.binary_logical_op_names))
        if tokenStatus.getCurrentToken().name in logop:
            op = tokenStatus.getCurrentToken().name
            if parsing:
                print("<bool_expression> -> <boolean> LOGOP:" + op + " <boolean>")
            tokenStatus = tokenStatus.goNext()
            priorStatus = tokenStatus
            tokenStatus = self.boolean(tokenStatus, expectedTerminals)
            if tokenStatus == priorStatus:
                self.unexpected_token_exception(tokenStatus, "<boolean>")

            val2 = tokenStatus.value
            message = str(op) + "(" + str(message) + "," + str(tokenStatus.message) + ")"
            tokenStatus.value = self.calculate_boolop(val1, val2, op)


        if parsing:
            print(lhs + message)
        tokenStatus.message = message
        return tokenStatus



    #endregion

    #region Operators/Short Types

    def arithmetic_op(self, tokenStatus):
        name = tokenStatus.getCurrentToken().name
        if (name == 'PLUS' or name == 'MINUS' or name == 'DIVISION' or name == 'MULTIPLICATION' or name == 'MODULO'):
            tokenStatus = tokenStatus.goNext()

        return tokenStatus


    #Operator names are nested so that groups can be done in the same pass; causes multiplication and modulus to be done
    #left to right while all being done before addition and subtraction
    binary_logical_op_names = [['AND', 'XOR', 'OR']]
    binary_relational_op_names = [['EQUAL_TO', 'INEQUAL_TO', 'LESS_THAN', 'LESS_EQUAL', 'GREATER_THAN', 'GREATER_EQUAL']]
    unary_arithmetic_op_names = [['NEGATIVE']]
    binary_arithmetic_op_names = [['MODULO', 'DIVISION', 'MULTIPLICATION'], ['MINUS', 'PLUS']]
    all_arithmetic_op_names = list(unary_arithmetic_op_names)
    all_arithmetic_op_names.extend(binary_arithmetic_op_names)

    def relop(self, tokenStatus):
        name = tokenStatus.getCurrentToken().name
        if(name == 'GREATER_THEN' or name == 'LESS_THEN' or name == 'GREATER_EQUAL' or name == 'LESS_EQUAL'):
            tokenStatus = tokenStatus.goNext()

        return tokenStatus

    def type_name(self, tokenStatus):
        name = tokenStatus.getCurrentToken().name
        if name == 'FLOAT_TYPENAME' or \
                name == 'INTEGER_TYPENAME' or \
                name == 'STRING_TYPENAME' or \
                name == 'CHARACTER_TYPENAME' or \
                name == 'BOOLEAN_TYPENAME':
            return tokenStatus.goNext()
        else:
            return tokenStatus

    #endregion

    #region Exceptions
    def unexpected_token_exception(self, tokenStatus, expected):
        raise Exception("Expected '" + expected + "' at " + str(tokenStatus.getCurrentToken().source_pos) + ", received '" + tokenStatus.getCurrentToken().value + "'")

    def undeclared_variable_exception(self, tokenStatus):
        raise Exception("'" + tokenStatus.getCurrentToken().value + "' has not been declared.")

    def incorrect_variable_type_exception(self, tokenStatus, expectedType):
        raise Exception("Expected '" + tokenStatus.getCurrentToken().value + "' to have type '" + expectedType, "', found type <" + self.declared_vars[tokenStatus.getCurrentToken().value]["type"] + ">")

    def unaccepted_operand_exception(self, operator, operands):
        message = "Operator '" + operator.name + "' not accepted on operand(s) "
        isFirst = True
        for operand in operands:
            if not isFirst:
                message += ", "
            message += operand.name
            isFirst = False
        raise Exception(message)

    #endregion

    #region Helper Methods
    def getTokensTillTerminal(self, tokenStatus, terminalTokenNames, useStack = True):

        tokens = [tokenStatus.getCurrentToken()]
        useParenStack = False
        if terminalTokenNames.__contains__("RPAREN"):
            useParenStack = True
        tokenIter = tokenStatus
        tokenIter = tokenIter.goNext()
        parenStack = []
        while not (tokenIter.getCurrentToken().name in terminalTokenNames) or (useStack and (useParenStack and len(parenStack) > 0)):
            tokens.append(tokenIter.getCurrentToken())
            if useParenStack:
                if (tokenIter.getCurrentToken().name == "LPAREN"):
                    parenStack.append(tokenIter.getCurrentToken().name)
                elif tokenIter.getCurrentToken().name == "RPAREN":
                    parenStack.pop()
            tokenIter = tokenIter.goNext()

        return tokens

    def calculate(self, val1, val2, operator):
        if operator == "MODULO":
            return val1 % val2
        elif operator == "MULTIPLICATION":
            return val1 * val2
        elif operator == "DIVISION":
            return val1 // val2
        elif operator == "PLUS":
            return val1 + val2
        elif operator == "MINUS":
            return val1 - val2
        elif operator == "NEGATIVE":
            return -1 * val1

    def calculate_boolop(self, val1, val2, operator):
        if operator == "AND":
            return val1 and val2
        elif operator == "XOR":
            return val1 != val2
        elif operator == "OR":
            return val1 or val2
        elif operator == "NOT":
            return not val1

    def calculate_relop(self, val1, val2, operator):
        if operator == "GREATER_EQUAL":
            return val1 >= val2
        elif operator == "LESS_EQUAL":
            return val1 >= val2
        elif operator == "GREATER_THAN":
            return val1 > val2
        elif operator == "LESS_THAN":
            return val1 < val2
        elif operator == "EQUAL_TO":
            return val1 == val2


    #endregion

    # block(status, False)
    # #int_expression(status, "END_INSTRUCTION")