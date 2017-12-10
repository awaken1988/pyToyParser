import os

class SingleChar:

    NEWLINE = "\n"
    SPACE = " "
    TAB = "\t"

    def __init__(self, aChar, aLine, aColumn, aPos):
        self.line           = aLine
        self.column         = aColumn
        self.pos            = aPos
        self.char           = aChar

    def __str__(self):
        ch = self.char

        if "\n" == ch:
            ch = "NEWLINE"
        elif " " == ch:
            ch = "SPACE"
        elif "\t" == ch:
            ch = "TAB"

        return "line={:4}; col={:4}; pos={:4}; char={:10}".format(self.line, self.column, self.pos, ch)

#TODO: could also be implemented as yield function
class Scanner:
    def __init__(self, aText):
        self.text       = aText
        self.content    = []

        self.rewind();


        row = 0
        col = 0
        pos = 0

        for i in self.text:
            self.content.append(SingleChar(i, row, col, pos))
            col += 1
            pos += 1

            if i == "\n":
                row += 1;
                col = 0;

    def __str__(self):
        ret = ""
        for i in self.content:
            ret+=str(i)+"\n"
        return ret;

    def __iter__(self):
        self.index = 0
        return self;

    def __next__(self):
        if self.index >= len(self.content):
            raise StopIteration()

        ret = self.content[self.index]
        self.index += 1

        return ret

    def __len__(self):
        return len(self.content)


    #eat methods :)
    def rewind(self):
        self.curr_pos   = 0;    #iterating options
        if hasattr(self, 'lastEat'):
            del self.lastEat

    def hasChar(self):
        if self.curr_pos >= len(self.content):
            return False
        return True

    #TODO: begin search with the longest string
    def nextStr(self, aLen, aOffset=0):
        if self.curr_pos+aLen-1+aOffset   >= len(self.content):
            return None
        if aLen < 1:
            return None

        retStr = ""
        retSingleCharArr = []
        for i in range(0, aLen):
                singleChar = self.content[self.curr_pos+i+aOffset]
                retStr += singleChar.char
                retSingleCharArr.append(singleChar)

        return {"String": retStr, "SingleChars": retSingleCharArr}


    def eatNextUntil(self, aString):
        """ This function reads until one char from aStringList is found """

        retString = ""
        retSingleCharArrar = []

        offset = 0
        for i in range(self.curr_pos, len(self.content)):
            look_ahead = self.nextStr(len(aString), offset)
            if not look_ahead:
                continue

            print( str(look_ahead["String"]) + " : " + aString)
            if look_ahead["String"] == aString:
                retString           += look_ahead["String"]
                retSingleCharArrar.extend( look_ahead["SingleChars"] )
                self.lastEat = {"String": retString, "SingleChars": retSingleCharArrar}
                self.curr_pos += len(retString)
                return True

            retString           += look_ahead["String"][0]
            retSingleCharArrar.append( look_ahead["SingleChars"][0] )
            offset += 1

        return False


    def eatNext(self, aStringList):
        """ This function try to read a string in aStringList
            If nothing is found under the current position return NONE"""

        aStringList = aStringList[:]
        aStringList.sort(key=len, reverse=True)

        for i in aStringList:
            try:
                found = self.nextStr(len(i))
                if i == found["String"]:
                    self.lastEat = found
                    self.curr_pos += len(found["String"])
                    return True
            except TypeError:
                continue

        if hasattr(self, "lastEat"):
            del self.lastEat
        return False

    #deprecated method
    def get_str(self, idx, count):
        ret = ""
        for i in self.content[idx:idx+count]:
            ret += i.char

        return ret




if __name__ == "__main__":
    txt = """test = 1;
    startloop = 0;
    endloop = 1;


    for startloop to endloop do
    {
        test = test +1
    }
"""

    a = Scanner(txt)
    for i in a:
        print(i)
