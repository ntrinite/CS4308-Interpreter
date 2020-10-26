class TokenStatus:

    def __init__(self, tokens, index=0):
        self.tokens = tokens
        self.tokenIndex = index

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

    def getPrevToken(self):
        if self.tokenIndex - 1 >= len(self.tokens) or self.tokenIndex - 1 < 0:
            return None
        else:
            return self.tokens[self.tokenIndex - 1]

    def goNext(self):
        newStatus = TokenStatus(self.tokens, self.tokenIndex + 1)
        # if self.getNextToken() is None:
        #     raise Exception("Unexpected end of file after " + str(self.tokens[self.tokenIndex]))
        return newStatus
