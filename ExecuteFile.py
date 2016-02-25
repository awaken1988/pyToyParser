from Parser import AstNode
from Parser import Parser
from Lexer  import Token
import sys

class IdentifierMap:
    def __init__(self):
        self.content = [ {} ]
        
    def _search(self, aIdentifier):
        reverse_content = reversed(self.content)
        reverse_index   = reversed(range(len(self.content)))
        for index, scope in zip(reverse_index,reverse_content):
            if aIdentifier in scope:
                return index;
        return -1;
            
    def contains(self, aIdentifier):
        if self._search(aIdentifier) >= 0:
            return True
        else:
            return False;
    
    def insert(self, aIdentifier, aValue, aTopScope=False):
        idx = self._search(aIdentifier)
        if -1 == idx or aTopScope:
            idx = len(self.content) - 1
        
        self.content[idx][aIdentifier] = aValue 
        

    def pushScope(self):
        self.content.append({})
    
    def popScope(self):
        self.content.pop()
        
    def dumpMap(self):
        ret = {}
        for iScope in self.content:
            for iName, iValue in iScope.items():
                ret[iName] = iValue
        return ret
        
        
    def __setitem__(self, aIdentfier, aValue):
        self.insert(aIdentfier, aValue) 
        
    def __getitem__(self, aIdentifier):
        index = self._search(aIdentifier)
        if index < 0:
            raise Exception("Identifier not found")
        else:
            return self.content[index][aIdentifier]
    
    def __str__(self):
        return str(self.content)
        

class ExecuteAst:
    def __init__(self, aAst, aLock=None):
        self.identifiers = IdentifierMap()
        self.depth = -1
        self.lock = aLock
        self.ast = aAst
        self.isEnd = False
        
    def run(self):
        self.call(self.exec, self.ast)
        self.isEnd = True
        print(self.identifiers)

    #Fixme: throw error if func is not from this class
    def call(self, func, aBranch):
        if self.lock:
            self.lock.acquire()
        self.depth += 1

        #debug
        children_val = [i.token.content+"; " for i in aBranch.children]
        print( "\t" * self.depth + str(aBranch.token.content) + "; Children="+str(children_val));
        ret = func(aBranch)

        self.depth -= 1
        if self.lock:
            self.lock.release()
        return ret

    def exec(self, aBranch):
        for i in aBranch.children:
            if i.token.content == "=":
                self.call(self.exec_assignment, i)
            elif i.token.content == "for":
                self.call(self.exec_for, i)
            elif i.token.content == "if":
                self.call(self.exec_if, i)
            else:
                raise Exception("error: command not included")

    #TODO: is like self.exec without loop; merge these functions
    def exec_inner_loop(self, aBranch):
        if aBranch.token.content == "=":
            self.call(self.exec_assignment, aBranch)
        elif aBranch.token.content == "for":
            self.call(self.exec_for, aBranch)
        elif aBranch.token.content == "if":
            self.call(self.exec_if, aBranch)
        else:
            raise Exception("error: command not included")


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

        #counter variable get own scope
        #variables assigned in the loop get their own scope
        self.identifiers.pushScope()

        self.call(self.exec_assignment, start_node)
        counter_var   = start_node.children[0].token.content
        end_index     = int(self.call(self.exec_expression, end_node))

        for i in range(self.identifiers[counter_var], end_index+1 ):
            for inner_loop_elem in aBranch.children[prev_index:]:
                self.call(self.exec_inner_loop, inner_loop_elem)
                self.identifiers[counter_var] = i
                
        self.identifiers.popScope()
        
    def exec_if(self, aBranch):
        comparison = aBranch.children[0].token.content;
        left   = int(   self.call(self.exec_expression, aBranch.children[1] )   )
        right  = int(   self.call(self.exec_expression, aBranch.children[2] )   )
        
        enterIf = False
        
        if   "==" == comparison:
            enterIf = left == right;
        elif ">=" == comparison:
            enterIf = left >= right;
        elif "<=" == comparison:
            enterIf = left <= right;
        elif ">"  == comparison:
            enterIf = left > right;
        elif "<"  == comparison:
            enterIf == left < right;
        
        #if true execute tree
        
        if enterIf:
            statements_start = 3
            statements_end   = len(aBranch.children) -1;
            
            #if block has no content
            if statements_end < statements_start:
                return; 
            
            for i in range(statements_start, statements_end+1):
                self.call(self.exec_inner_loop, aBranch.children[i])

        return
        
                



testProgram = """
start = 1;
end   = 1+2+3+4*5;
a = 2;
mult = 2;

if a >= mult
{
    mult = 3;
};

for i = 1 to end
{
    a = a * mult * 2;
};
"""

testProgram = """
c1 = 1;
c2 = 10;
x = 0;

if c1 == 1 
{
    x = x + 1;
};

if c2 > 9
{
    x = x + 2;
};

"""



if __name__ == "__main__":
    astTree = Parser(testProgram).ast
    ExecuteAst(astTree)
