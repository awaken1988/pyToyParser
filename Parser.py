#TODO: show more helpful parser errors
#TODO: epxression like a = x * y doesn't work because last symbol is no number?
#

from Lexer import *

class AstNode:
    def __init__(self,aToken=None):
        self.token      = aToken
        self.children   = []

    def addNode(self, aNode):
        if not isinstance(aNode, AstNode):
            raise Exception("aNode must be AstNode")

        self.children.append(aNode)

    def _stringify(self, aDepth):
        outstr  = aDepth * "   "
        outstr += str(self.token)
        outstr += "\n"
        for i in self.children:
            outstr += i._stringify(aDepth+1)
        return outstr;

    def __str__(self):
        return self._stringify(1)

class Parser:
    MATH_OPERATORS = ["+", "-", "*", "/"]
    ASSIGNMENT     = "="

    def __init__(self, aProgramText):
        lexer = Lexer(aProgramText)
        self.content = lexer.tokens       #Array of Token
        print("-------------------------------")
        self.ast = self.ebnf_progam()

        print( self.ast )



    #only for testing
    #def __init__(self):
    #    lexer = Lexer(testCode)
    #    self.content = lexer.tokens       #Array of Token
    #    print("-------------------------------")
    #    a = self.ebnf_progam()

    def error(self):
        errStr = "error:"
        errStr += " Type="       + str(self.content[0].type)
        errStr += "; Content="    + str(self.content[0].content)
        errStr += "\nTextPos: " + str(self.content[0])
        return errStr

    def error(self):
        raise Exception(self.getToken())

    def getToken(self):
        return self.content[0]

    def nextToken(self):
        """
            Pop and return the next token
        """
        return self.content.pop(0)

    def check(self, aTokenType, aTokenContent=None):
         isType     = self.content[0].type == aTokenType
         isContent  = self.content[0].content == aTokenContent

         strOut = "Expecting: Type={} Content={}        -       ".format(aTokenType, aTokenContent)
         strOut += str(self.content[0])

         if isType and ( aTokenContent==None or isContent ):
             print("accept: "+strOut)
             return AstNode( self.content[0] )
         else:
            print("notaccept: "+strOut)
            return None

    def ebnf_progam(self):
        node_root = AstNode( Token("root", "root") )

        while not self.check(Token.EOF):
            node_block = self.ebnf_block()
            if not node_block: self.error()

            if not self.check(Token.SYMBOL, ";"):
                self.error()

            node_root.addNode(node_block)

            self.nextToken()

        return node_root

    def ebnf_block(self):
        ret = None

        if self.check(Token.IDENTIFIER):
            node_identifier = AstNode( self.nextToken() )

            node_assignment = self.check(Token.SYMBOL, Parser.ASSIGNMENT);
            self.nextToken()
            if not node_assignment: self.error()

            node_expr = self.ebnf_expression()
            if not node_expr: self.error()

            ret = node_assignment
            ret.addNode(node_identifier)
            ret.addNode(node_expr)
        elif self.check(Token.SYMBOL, "for"):
            node_for = AstNode( self.nextToken() )

            #start loop expression
            node_expr_start = self.ebnf_expression()
            if not node_expr_start: self.error()

            if not self.check(Token.SYMBOL, "to"):
                self.error()
            self.nextToken()

            #end loop expression
            node_expr_end = self.ebnf_expression()
            if not node_expr_end: self.error()

            if not self.check(Token.SYMBOL, "{"):
                self.error()
            self.nextToken()

            #inner loop
            nodes_inner = []
            while True:
                node_inner_tmp = self.ebnf_block()
                if not node_inner_tmp:
                    if len(nodes_inner) < 1 :
                        self.error()
                    break
                nodes_inner.append(node_inner_tmp)

                if not self.check(Token.SYMBOL, ";"):
                    self.error()
                self.nextToken()



            if not self.check(Token.SYMBOL, "}"):
                self.error()
            self.nextToken()

            node_for.addNode(node_expr_start)
            node_for.addNode(node_expr_end)
            for i in nodes_inner:
                node_for.addNode(i)

            ret = node_for
        return ret

    def ebnf_expression(self):
        result = self.ebnf_numericitem()
        if not result:
            return None

        operator = self.ebnf_operator()
        if operator:
            operator.addNode(result)
            nextRec = self.ebnf_expression()
            if not nextRec: self.error()
            operator.addNode(nextRec)

            result = operator

        return result


    def ebnf_numericitem(self):
        if self.check(Token.NUMBER) or self.check(Token.IDENTIFIER):
            return AstNode( self.nextToken() )
        return None

    def ebnf_operator(self):
        for iOp in Parser.MATH_OPERATORS:
            if self.check(Token.SYMBOL, iOp):
                return AstNode( self.nextToken() )
        return None

if __name__ == "__main__":
    Parser()
