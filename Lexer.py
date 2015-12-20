#
#FIXME: do we need to parse NEWLINES?
#
#
#



from Scanner import Scanner
from Scanner import SingleChar
import string

class Token:

    KEYWORDS = [    "for", "to", "do",
                    "{",   "}",  ";", "=",
                    "+",   "-",  "*", "/",
                    "if",  ">",  "<", "==",
                    "<=",  ">="
                ]

    IDENTIFIER_STARTCHARS = list(string.ascii_lowercase)
    IDENTIFIER_CHARS      = list(string.ascii_lowercase + string.digits + "_")

    NUMBER_STARTCHARS     = list(string.digits)
    NUMBER_CHARS          = list(string.digits + ".")

    STRING_START_END_CHAR = list("\"")
    WHITESPACE_CHARS      = list(" \t")
    NEWLINE_CHARS =         list("\n")

    STRING             = "String"
    IDENTIFIER         = "Identifier"
    NUMBER             = "Number"
    NEWLINE            = "Newline"
    SYMBOL             = "Symbol"
    EOF                = "EOF"

    def __init__(self, aContent=None, aType=None, aPosInfo=None):
        self.content = aContent
        self.type = aType
        self.pos  = aPosInfo

    def __str__(self):
        contentStr = self.content.replace("\n", "\\n")

        pos = ""
        if self.pos is list:
            pos = str(self.pos[0])

        return "Type='{:12}'; {:16} Content='{}'".format(self.type, pos, contentStr)




class Lexer:
    def __init__(self, aText):
        self.tokens = []
        scan = Scanner(aText)

        while scan.hasChar():
            #print(scan.content[scan.curr_pos])

            #TODO: implement comment parsing
            #TODO: EOF

            if scan.eatNext( Token.WHITESPACE_CHARS ):
                #print("skip whitespace")
                continue

            elif scan.eatNext( Token.KEYWORDS ):
                self.tokens.append( Token(scan.lastEat["String"], Token.SYMBOL, scan.lastEat["SingleChars"]) )

            elif scan.eatNext( Token.NEWLINE_CHARS ):
                #ignore newline
                #self.tokens.append( Token("", Token.NEWLINE, scan.lastEat["SingleChars"]) )
                pass

            elif scan.eatNext( Token.IDENTIFIER_STARTCHARS ):
                startChar = scan.lastEat
                fullString = scan.lastEat["String"]
                while scan.eatNext( Token.IDENTIFIER_CHARS ):
                    fullString += scan.lastEat["String"]
                #TODO: startChar only contains position from the first char
                self.tokens.append( Token(fullString, Token.IDENTIFIER, startChar["SingleChars"]) )

            elif scan.eatNext( Token.NUMBER_STARTCHARS ):
                startChar = scan.lastEat
                fullString = scan.lastEat["String"]
                while scan.eatNext( Token.NUMBER_CHARS ):
                    fullString += scan.lastEat["String"]
                #TODO: startChar only contains position from the first char
                self.tokens.append( Token(fullString, Token.NUMBER, startChar["SingleChars"]) )

            elif scan.eatNext( Token.STRING_START_END_CHAR ):
                beginStr = scan.lastEat
                if not scan.eatNextUntil( Token.STRING_START_END_CHAR ):
                    raise Exception("Cannot parse String")

                fullString      = scan.lastEat["String"]
                fullSingleChars = beginStr["SingleChars"]
                fullSingleChars.extend( scan.lastEat["SingleChars"] )   #TODO: join with the previous line

                self.tokens.append( Token(fullString[0:-1], Token.STRING, fullSingleChars) )
            else:
                raise Exception("Parser Error")
                scan.curr_pos += 1

        self.tokens.append( Token("EOF", Token.EOF, [SingleChar("EOF", 0, 0, 0)]) )

        for i in self.tokens:
            print(i)

#testCode = """test = 1;
#firstnum = 0;
#lastnum = 10;
#for firstnum to lastnum
#{
#    test = test + 1;
#};
#"""

#testCode = """test = 1;
#x = 12 + 13 + 14 + 15 + 16 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1;
#"""

testCode ="""
start = 1;
end = 10;
sum = 0;
for start to end
{
    sum = sum + 1;
};
"""

if __name__ == "__main__":
    Lexer(testCode)
