class TokenStatus:

    def __init__(self, tokens, index=0, value=None, message=None):
        self.tokens = tokens
        self.tokenIndex = index
        self.value = value
        self.message = message
        self.expected = None

    def getCurrentToken(self):
        if self.tokenIndex >= len(self.tokens):
            raise Exception("Unexpected end of file after " + str(self.getPrevToken()))
            # return None
        else:
            return self.tokens[self.tokenIndex]

    def getNextToken(self):
        if self.tokenIndex + 1 >= len(self.tokens):
            return None
        else:
            return self.tokens[self.tokenIndex + 1]

    def getNextTokenNotIn(self, nameSet):
        for i in range(self.tokenIndex + 1, len(self.tokens)):
            if not nameSet.__contains__(self.tokens[i].name):
                return self.tokens[i]
        return None

    def getPrevTokenNotIn(self, nameSet):
        for i in reversed(range(0, self.tokenIndex - 1)):
            if not nameSet.__contains__(self.tokens[i].name):
                return self.tokens[i]
        return None

    def getPrevToken(self):
        if self.tokenIndex - 1 >= len(self.tokens) or self.tokenIndex - 1 < 0:
            return None
        else:
            return self.tokens[self.tokenIndex - 1]

    def goNext(self):
        if self.expected is not None and not self.expected.__contains__(self.getNextToken().name):
            raise Exception("Expected " + str(self.expected) + " at " + str(self.getNextToken().source_pos) + ", received " + str(self.getNextToken().value))
        newStatus = TokenStatus(self.tokens, self.tokenIndex + 1, self.value, self.message)
        # if self.getNextToken() is None:
        #     raise Exception("Unexpected end of file after " + str(self.tokens[self.tokenIndex]))
        return newStatus

    def expect(self, name):
        self.expected = name
