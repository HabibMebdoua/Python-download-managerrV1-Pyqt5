
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

from os import path
import sys

import urllib.request


FORM_CLASS, _= loadUiType(path.join(path.dirname(__file__),"main.ui"))

######################################################################################
class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Calling the method when the constractor is runnig
        self.Handel_UI()
        # callig the buttons handeling
        self.Handel_Buttons()

    def Handel_UI(self):
        # Changing the window title
        self.setWindowTitle("MEBdownloader")
        # Setting a fixed size for the window
        self.setFixedSize(694,362)

    def Handel_Buttons(self):
        # Connect the Download btn with the Dowload method
        self.pushButton.clicked.connect(self.Download)
        # connect the browse btn with the browse method
        self.pushButton_2.clicked.connect(self.Handel_Browse)

    def Handel_Browse(self):
        '''
            self : لانها تظهر فوق الويدجت
            caption : is the title
            directory : المكان لي تتفتح فيه
            filter : الامتدادات المسموحة (اي اسم,اي امتداد)        
        '''
        save_place = QFileDialog.getSaveFileName(self , caption='Save as' , directory='.' , filter="*.*")
        #Getting the saving path
        text = str(save_place)
        path = (text[2:].split(',')[0].replace("'",''))

        self.lineEdit_2.setText(path)

    def Handel_Progress_Bar(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()  # not responding solution


    def Download(self):
        # geeting the text from the line edit (Url is the path of downloaded File)
        url = self.lineEdit.text()
        # Getting the Saving path
        save_path = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url , save_path , self.Handel_Progress_Bar)
        except Exception:
            # Show a meesage 
            QMessageBox.warning(self , "Download Error" , "Download Faild") 
            return
        
        QMessageBox.information(self , "Download status" , "Downloading done") 
        # Reset the values
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)









def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__== '__main__':
    main()