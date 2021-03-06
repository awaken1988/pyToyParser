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

        assignment = self.ebnf_assignment();
        
        if assignment:
            ret = assignment;
        elif self.check(Token.SYMBOL, "for"):
            node_for = AstNode( self.nextToken() )

            #start loop expression
            node_expr_start = self.ebnf_assignment()
            if not node_expr_start: self.error()

            if not self.check(Token.SYMBOL, "to"):
                self.error()
            self.nextToken()

            #end loop expression
            node_expr_end = self.ebnf_expression(1)
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
        elif self.check(Token.SYMBOL, "if"):
            ret = AstNode( self.nextToken() )
            
            node_left = self.ebnf_expression()
            if not node_left:
                self.error()
            
            node_comp  = self.ebnf_compare()
            if not node_comp:
                self.error()
                
            node_right = self.ebnf_expression()
            if not node_right:
                self.error()
            
            
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
                
            ret.addNode(node_comp)
            ret.addNode(node_left)
            ret.addNode(node_right)
            for i in nodes_inner:
                ret.addNode(i)                
    
            
             
        return ret

    def ebnf_compare(self):
        comp = "<=", ">=", "==", "<", ">";
        
        for i in comp:
            if self.check(Token.SYMBOL, i):
                return AstNode( self.nextToken() )
        return None
            
    def ebnf_assignment(self):
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
            return ret;
        else:
            return None
        

    OP_PRECEDENCE = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
    }

    def ebnf_expression(self):
        return self.ebnf_expression_inner(self.ebnf_numericitem(), 1)


    def ebnf_expression_inner(self, lhs, curr_prec):
        while True:
            op = self.ebnf_operator(peek=True)
            if not op:
                return lhs
            
            op_prec = int(self.OP_PRECEDENCE[op.token.content])

            if op_prec > curr_prec:
                lhs = self.ebnf_expression_inner(lhs, op_prec)
                continue
            elif op_prec < curr_prec:
                return lhs
            
            self.ebnf_operator()    #consume next token

            op.addNode( lhs )
            rhs = self.ebnf_expression_inner(self.ebnf_numericitem(), curr_prec)
            if not rhs: self.error()
            op.addNode( rhs )

            lhs = op
    
        return lhs

    def ebnf_numericitem(self):
        if self.check(Token.NUMBER) or self.check(Token.IDENTIFIER):
            return AstNode( self.nextToken() )
        return None

    def ebnf_operator(self, peek=False):
        check = None
        for iOp in Parser.MATH_OPERATORS:
            check = self.check(Token.SYMBOL, iOp)
            if check: break;
        if not peek: self.nextToken()
        return check

if __name__ == "__main__":
    Parser()
