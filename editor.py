import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTextEdit, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
import threading
import enum

#toy language includes
from Parser import AstNode
from Parser import Parser
from Lexer  import Token
from ExecuteFile import ExecuteAst
from widgets.CodeEditor import CodeEditor
from idlelib.idle_test.test_warning import RunWarnTest


#REFERENCES:
#    - http://zetcode.com/gui/pyqt5/eventssignals/
#
#

#TODO:
#    . Add line numbers
#        - http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
#


class ExecState(enum.Enum):
    not_running = 0 #ExecuteAst is not running at all
    running     = 1 #ExecuteAst is running
    halted      = 2 #ExecuteAst exists but halted (e.g because breakpoint)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__();
        self.setGeometry(200, 200, 800, 640);
        self.initUi();
        
        self.state = ExecState.not_running
        self.lock  = threading.Lock()
        
    def initUi(self):
        self.setWindowTitle("Toy Language")
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        
        self.initCodeEditor()
        self.initVariableTable()
        self.initButtons()
        
        self.setLayout(self.grid)
        self.show()

    def initCodeEditor(self):
        self.codeEditor = CodeEditor(self)
        self.grid.addWidget(self.codeEditor, 2, 1)
        
        defaultCode = """
x = 1;
y = 1;
z = 2;

for i=0 to 2
{
    for j=0 to 2
    {
        x = x + 1;
    };
    
    y = y * 2;
};

if x > 0
{
    z = 100;
};



        """
        
        self.codeEditor.setPlainText(defaultCode)
        
       
    def initVariableTable(self):
        self.variableTable = QTableWidget()
        #self.variableTable.setRowCount(8)
        self.variableTable.setColumnCount(2)
        self.grid.addWidget(self.variableTable, 2, 2)
        
    def initButtons(self):
        self.btnHBox = QHBoxLayout();
        
        self.btnRun     = QPushButton("Run")
        self.btnSave    = QPushButton("Save")
         
        self.btnRun.clicked.connect(self.run)
         
        self.btnHBox.addWidget(self.btnRun)
        self.btnHBox.addWidget(self.btnSave)
        self.grid.addLayout(self.btnHBox, 1, 1)
         
    def run(self):
        content = self.codeEditor.toPlainText()
        
        astTree = None
        
        #parse
        try:
            astTree = Parser(content).ast
            self.execAst = ExecuteAst(astTree)
            self.interpreter_thread = threading.Thread(self.execAst.run()) 
            self.interpreter_thread.start()
        except Exception as e:
            print(e)
            
        self.runWaitReady()
        
    def runWaitReady(self):
        while not self.execAst.isEnd:
            self.lock.acquire()    
            self.lock.release()
        self.updateVariableTable()     
        
    def updateVariableTable(self):
        currentVars = self.execAst.identifiers.dumpMap()
        
        self.variableTable.clear()
        self.variableTable.setRowCount(len(currentVars))
        for iNum, iName in enumerate(currentVars):
            iValue = currentVars[iName]
            print("<<<" + str(iName) + " - " + str(iValue))
            self.variableTable.setItem( iNum, 0,  QTableWidgetItem(str(iName)))
            self.variableTable.setItem( iNum, 1,  QTableWidgetItem(str(iValue)))
            
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    x = MainWindow()
    
    sys.exit(app.exec_())