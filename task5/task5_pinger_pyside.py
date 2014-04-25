import threading
import subprocess
import argparse
import sys
from PySide import QtGui, QtCore

class DataSignal(QtCore.QObject):
    sig = QtCore.Signal(str, int)
    

threads = []
signalizer = DataSignal()

def ping_host(host, num): 
    PIPE = subprocess.PIPE
    p = subprocess.Popen(" ".join(["ping", host]), shell=True, stdin=PIPE, stdout=PIPE,
        stderr=subprocess.STDOUT, close_fds=True)
    answer = p.stdout.readline()
    while answer:
        signalizer.sig.emit(str(answer)[2:-3], num + 2)
        answer = p.stdout.readline()        
        
'''class PopUpWidget(QtGui.QInputDialog):
    def __init__(self):
        super(PopUpWidget, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setInputMode(QtGui.QInputDialog.TextInput)
        ip_addr = QtGui.QInputDialog.getText(self, "QInputDialog.getText()",
                                          "User name:");
        if not len(ip_addr) == 0:
            print(ip_addr[0])
            
        self.show()'''

class PingerWidget(QtGui.QWidget):
    def __init__(self):
        super(PingerWidget, self).__init__()
        self.counter = 0
        self.addPopUp = QtGui.QInputDialog()
        self.grid = QtGui.QGridLayout()   
        self.initUI()
    
    def initUI(self):      
        addNewBut = QtGui.QPushButton("Add new address")
        self.addPopUp.setInputMode(QtGui.QInputDialog.TextInput)
        addNewBut.clicked.connect(self.azaza)
        signalizer.sig.connect(self.addData)
        
        self.grid.addWidget(addNewBut, 0, 1)
        self.grid.addWidget(QtGui.QLabel("#"), 1, 0)
        self.grid.addWidget(QtGui.QLabel("ip address"), 1, 1)
        self.grid.addWidget(QtGui.QLabel("last ping response"), 1, 2)
        self.setLayout(self.grid)
        
    def azaza(self):
        response = QtGui.QInputDialog.getText(self, "Enter IP", "Ip: ")
        if response[1]:
            ip = response[0]
            self.grid.addWidget(QtGui.QLabel(str(self.counter)), self.counter + 2, 0)
            self.grid.addWidget(QtGui.QLabel(ip), self.counter + 2, 1)
            self.grid.addWidget(QtGui.QLabel(""), self.counter + 2, 2)
            t = threading.Thread(target=ping_host, args=(ip, self.counter))
            threads.append(t)
            t.start()
            self.counter += 1
    
    '''slot for a data signal'''
    def addData(self, response, lineNum):
        self.grid.itemAtPosition(lineNum, 2).widget().setText(response)

class PingerMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(PingerMainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):        
        '''openAction = QtGui.QAction('&Open IP list', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open text file with a list of IP addresses')
        #openAction.triggered.connect() 

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)'''
        
        self.setCentralWidget(PingerWidget())
        
        self.setWindowTitle('Pinger 0.1')
        self.show()
        
    def keyPressEvent(self, e):
        print(e.type())
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    wind = PingerMainWindow()
    sys.exit(app.exec_())

    '''parser = argparse.ArgumentParser(description='Pinger v.0.0.9')
    parser.add_argument('hosts', metavar = 'host', type = str, nargs = '+', 
                    help = 'IP addresses, such as 127.0.0.1')
    args = parser.parse_args()
    threads = []
    for i in range(len(args.hosts)):
        t = threading.Thread(target=ping_host, args=(args.hosts[i],i,))
        threads.append(t)
        t.start() '''
        
if __name__ == '__main__':
    main()