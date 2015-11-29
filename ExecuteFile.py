from Parser import AstNode
from Parser import Parser
import sys


class ExecuteAst:
    def __init__(self, aAst):
        self.identifiers = {}
        self.depth = -1

        self.call(self.exec, aAst)

        print(self.identifiers)


    #Fixme: throw error if func is not from this class
    def call(self, func, aBranch):
        self.depth += 1

        #debug
        children_val = [i.token.content+"; " for i in aBranch.children]
        print( "\t" * self.depth + str(aBranch.token.content) + "; Children="+str(children_val));
        ret = func(aBranch)

        self.depth -= 1
        return ret

    def exec(self, aBranch):
        for i in aBranch.children:
            if i.token.content == "=":
                self.call(self.exec_assignment, i)

    #TODO: replace index-numbers with symbolic values
    def exec_assignment(self, aBranch):
        identifier_name = aBranch.children[0].token.content
        value_node      = aBranch.children[1]

        val = self.call(self.exec_expression, value_node)
        self.identifiers[identifier_name] = val;

    def exec_expression(self, aBranch):
        #return value
        if len(aBranch.children) < 1:
            return int(aBranch.token.content)
        #more complex expression
        else:
            op = aBranch.token.content;

            left_num  = aBranch.children[0];
            right_num = aBranch.children[1];

            if isinstance(left_num, AstNode):
                left_num  = int(self.call(self.exec_expression, left_num))
            if isinstance(right_num, AstNode):
                right_num = int(self.call(self.exec_expression, right_num))
            ret = None

            if   op == "+":
                ret = left_num + right_num
            elif op == "-":
                ret = left_num - right_num
            elif op == "*":
                ret = left_num * right_num
            elif op == "/":
                ret = left_num / right_num

            return ret

testProgram = """
start = 0;
end   = 1+2+3+4*5;
for start to end
{
        a = 0;
};
"""

if __name__ == "__main__":
    astTree = Parser(testProgram).ast
    ExecuteAst(astTree)
