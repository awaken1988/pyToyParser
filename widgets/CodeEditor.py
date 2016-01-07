import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        
        
    def sizeHint(self, *args, **kwargs):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)
    
    def paintEvent(self, event):
        print("LineNumberArea::paintEvent")
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
       
        
        self.lineNumberArea = LineNumberArea(self)
        print(self.lineNumberArea)
        
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        self.show()
        
    def lineNumberAreaWidth(self):
        digits = 1
        max = self.blockCount()
        
        if max < 1:
            max = 1
        
        while max >= 10:
            max    /= 10
            digits += 1
            
        space = 3 + self.fontMetrics().width("9") * digits
        #space = 10+ 10 * digits
        
        print("lineNumberAreaWidth "+str(space))
        return space

    def updateLineNumberAreaWidth(self, arg):
        #print("updateLineNumberAreaWidth")
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
        
    def updateLineNumberArea(self, rect, dy):
        #print("updateLineNumberArea")
        if dy != 0:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
            
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
        
    def highlightCurrentLine(self, *arg):
        print("CodeEditor::highlightCurrentLine")
    
    def lineNumberAreaPaintEvent(self, event):
        print("CodeEditor::lineNumberAreaPaintEvent "+str(event.rect()))
        painter = QPainter()
        painter.begin(self.lineNumberArea) 
        painter.fillRect(QRect(0, 0, self.lineNumberArea.geometry().width(), self.height()), Qt.gray)
        
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top     = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom  = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom  = top + self.blockBoundingRect(block).height()
            blockNumber += 1
        
        painter.end()
        
    def paintEvent(self, *args, **kwargs):
        print("CodeEditor::paintEvent")
        QPlainTextEdit.paintEvent(self, *args, **kwargs)
        
    def resizeEvent(self, e):
        print("CodeEditor::resizeEvent "+str(e))
        super().resizeEvent(e)
        cr = self.contentsRect()
        print("    "+str(cr))
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))           

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = CodeEditor()
    app.exec_()

