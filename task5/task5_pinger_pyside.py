import threading
import subprocess
import sys
import os
import signal
from PySide import QtGui, QtCore

class DataSignal(QtCore.QObject):
    sig = QtCore.Signal(str, int)

threads = []
pingers = []
addHostSignalizer = DataSignal()

class HostPinger(): 
    def __init__(self, host, num):
        PIPE = subprocess.PIPE
        self.p = subprocess.Popen(["ping", host], stdin=PIPE, stdout=PIPE,
                              stderr=subprocess.STDOUT, close_fds=True)
        answer = self.p.stdout.readline()
    
        while answer:
            addHostSignalizer.sig.emit(str(answer)[2:-3], num + 2)
            answer = self.p.stdout.readline()   
            
def createPinger(host, num):   
    pingers.append(HostPinger(host, num))

class PingerWidget(QtGui.QWidget):
    def __init__(self):
        super(PingerWidget, self).__init__()
        self.counter = 0
        self.addPopUp = QtGui.QInputDialog()
        self.grid = QtGui.QGridLayout()   
        self.initUI()
    
    def initUI(self):      
        addNewBut = QtGui.QPushButton("Add new host")        
        addNewBut.clicked.connect(self.addHostSlot)
        
        loadListBut = QtGui.QPushButton("Load list from file")
        loadListBut.clicked.connect(self.openActionSlot)
        
        addHostSignalizer.sig.connect(self.addData)
        self.addPopUp.setInputMode(QtGui.QInputDialog.TextInput)
        
        self.grid.addWidget(addNewBut, 0, 1)
        self.grid.addWidget(loadListBut, 0, 2)
        self.grid.addWidget(QtGui.QLabel("#"), 1, 0)
        self.grid.addWidget(QtGui.QLabel("Host"), 1, 1)
        self.grid.addWidget(QtGui.QLabel("Last ping response"), 1, 2)
        self.setLayout(self.grid)
        
    def addLine(self, host):
        self.grid.addWidget(QtGui.QLabel(str(self.counter)), self.counter + 2, 0)
        self.grid.addWidget(QtGui.QLabel(host), self.counter + 2, 1)
        self.grid.addWidget(QtGui.QLabel(""), self.counter + 2, 2)
        t = threading.Thread(target=createPinger, args=(host, self.counter))
        threads.append(t)
        t.start()
        self.counter += 1
    
    def addHostSlot(self):
        response = QtGui.QInputDialog.getText(self, "Enter host", "Enter ip or web-address")
        if response[1]:
            host = response[0]
            self.addLine(host)
            
    def openActionSlot(self):
        textFile = QtGui.QFileDialog.getOpenFileName(self, "Open text file",  os.getcwd())
        f = open(textFile[0], 'r')
        self.pingHostsList(f.read().split())
        
    def pingHostsList(self, l):
        for host in l:
            self.addLine(host)
    
    def addData(self, response, lineNum):
        self.grid.itemAtPosition(lineNum, 2).widget().setText(response)

class PingerMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(PingerMainWindow, self).__init__()
        self.initUI()
    
    def initUI(self): 
        self.setCentralWidget(PingerWidget())
               
        openAction = QtGui.QAction('&Load hosts list from file', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open text file with a list of hosts to ping')
        openAction.triggered.connect(self.centralWidget().openActionSlot) 

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        
        self.setWindowTitle('Pinger 0.1')
        self.show()
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            QtCore.Qt.Key_
            self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    wind = PingerMainWindow()
    exitcode = app.exec_()
    for pinger in pingers:
        #os.killpg(pinger.p.pid, signal.SIGTERM)
        pinger.p.kill()
    
    for thread in threads:
        thread.join()
        
    sys.exit(exitcode)
        
if __name__ == '__main__':
    main()