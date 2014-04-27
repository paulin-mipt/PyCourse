import sys
import os
from PySide import QtGui, QtCore

class PyMageMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(PyMageMainWindow, self).__init__()
        self.view = QtGui.QGraphicsView()
        self.pixmap = QtGui.QPixmap()
        self.currentMult = 1.0
        self.initUI()
        
    multIn = 1.25
    multOut = 0.8
    
    def zoomInPixmap(self):
        self.currentMult *= self.multIn
        scene = QtGui.QGraphicsScene(self)
        scene.addPixmap(self.pixmap.scaled(self.pixmap.size() * self.currentMult))  
        self.view = QtGui.QGraphicsView(scene)
        self.setCentralWidget(self.view)
        
        
    def zoomOutPixmap(self):
        self.currentMult *= self.multOut
        scene = QtGui.QGraphicsScene(self)
        scene.addPixmap(self.pixmap.scaled(self.pixmap.size() * self.currentMult))  
        self.view = QtGui.QGraphicsView(scene)
        self.setCentralWidget(self.view)
    
    def openImage(self, imagePath):
        self.pixmap = QtGui.QPixmap(imagePath)  
        scene = QtGui.QGraphicsScene(self)
        scene.addPixmap(self.pixmap)  
        self.view = QtGui.QGraphicsView(scene)
        self.view.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.setCentralWidget(self.view)
                
    def loadFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self.view, "Open image",  os.getcwd(), 
                                                     "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tif)")
        if len(fileName[0]) > 0:
            self.openImage(fileName[0])
            self.setWindowTitle("PyMage: " + fileName[0])
        
    def initUI(self):
        openAction = QtGui.QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open image file')
        openAction.triggered.connect(self.loadFile)
        
        exitAction = QtGui.QAction('E&xit', self)
        exitAction.setShortcut('Escape')
        exitAction.setStatusTip('Exit app')
        exitAction.triggered.connect(self.close) 
        
        plusAction = QtGui.QAction('Zoom &In', self)
        plusAction.setShortcut('Ctrl++')
        plusAction.triggered.connect(self.zoomInPixmap)
        
        minusAction = QtGui.QAction('Zoom &Out', self)
        minusAction.setShortcut('Ctrl+-')
        minusAction.triggered.connect(self.zoomOutPixmap)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(plusAction)
        viewMenu.addAction(minusAction)
        
        self.toolbar = self.addToolBar('Zoom')
        QtGui.QToolBar.addSeparator(self.toolbar)
        self.toolbar.addAction(plusAction)
        self.toolbar.addAction(minusAction)
        QtGui.QToolBar.addSeparator(self.toolbar)
        
        self.setWindowTitle('PyMage')
        self.showMaximized()
        

def main():
    app = QtGui.QApplication(sys.argv)
    window = PyMageMainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
