import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTextEdit, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem

#toy language includes
from Parser import AstNode
from Parser import Parser
from Lexer  import Token
from ExecuteFile import ExecuteAst


#REFERENCES:
#    - http://zetcode.com/gui/pyqt5/eventssignals/
#
#

#TODO:
#    . Add line numbers
#        - http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
#





class MainWindow(QWidget):
    def __init__(self):
        super().__init__();
        self.setGeometry(200, 200, 800, 640);
        self.initUi();
        
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
        self.codeEditor = QTextEdit()
        self.grid.addWidget(self.codeEditor, 2, 1)
        
        defaultCode = """
x = 1;
y = 1;
z = 2;

for i=0 to 100 
{
    for j=0 to 100
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
        
        self.codeEditor.setText(defaultCode)
        
       
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
        
        
        try:
            astTree = Parser(content).ast
            self.execAst = ExecuteAst(astTree)
            self.updateVariableTable()
        except Exception as e:
            print(e)
            
        
            
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