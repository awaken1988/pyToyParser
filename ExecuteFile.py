from Parser import AstNode
from Parser import Parser
from Lexer  import Token
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
            elif i.token.content == "for":
                self.call(self.exec_for, i)

    #TODO: is like self.exec without loop; merge these functions
    def exec_inner_loop(self, aBranch):
        if aBranch.token.content == "=":
            self.call(self.exec_assignment, aBranch)
        elif aBranch.token.content == "for":
            self.call(self.exec_for, aBranch)


    #TODO: replace index-numbers with symbolic values
    def exec_assignment(self, aBranch):
        identifier_name = aBranch.children[0].token.content
        value_node      = aBranch.children[1]

        val = self.call(self.exec_expression, value_node)
        self.identifiers[identifier_name] = val;

    def exec_expression(self, aBranch):
        #return value
        if len(aBranch.children) < 1:
            if aBranch.token.type == Token.IDENTIFIER:
                return int(self.identifiers[aBranch.token.content])
            else:
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

    def exec_for(self, aBranch):
        start_node = aBranch.children[0]
        end_node   = aBranch.children[1]
        prev_index = 2

        start_index = self.call(self.exec_expression, start_node)
        end_index   = self.call(self.exec_expression, end_node)

        for i in range(0, end_index-start_index+1):
            for inner_loop_elem in aBranch.children[prev_index:]:
                self.call(self.exec_inner_loop, inner_loop_elem)

        #print(str(start_index) + " to " + str(end_index) )




testProgram = """
start = 1;
end   = 1+2+3+4*5;
a = 2;
mult = 2;
for start to end
{
    a = a * mult * 2;
};
"""

if __name__ == "__main__":
    astTree = Parser(testProgram).ast
    ExecuteAst(astTree)
