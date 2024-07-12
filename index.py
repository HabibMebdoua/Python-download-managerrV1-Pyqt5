
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

from os import path
import sys

import urllib.request #Download files
from pytube import YouTube,Playlist # Download vedio from youtube



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
        self.setFixedSize(736,412)

    def Handel_Buttons(self):
        # Connect the Download btn with the Dowload method
        self.pushButton.clicked.connect(self.Download)
        # connect the browse btn with the browse method
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        #connct the video downloading button
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video)
         #connct the browse video downloading button
        self.pushButton_3.clicked.connect(self.Handel_Youtube_Video_browse)
        #connct the video downloading button
        self.pushButton_4.clicked.connect(self.Download_Youtube_Video)
         #connct the browse playlist downloading button
        self.pushButton_5.clicked.connect(self.Handel_Youtube_Video_browse)
         #connct the playlistdownloading button
        self.pushButton_6.clicked.connect(self.Playlist_Download)

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



    ############################## YOUTUBE VIDEO ############################

    def Get_Youtube_Video(self):

        try:
            video_link = self.lineEdit_4.text()
            video = YouTube(video_link)
        
            # من المفروض هنا تطلع جودات الفيديو
            for st in video.streams:
                if st.type == "video":
                    #print(st.type + ' ' + st.resolution)
                    self.comboBox.addItem(f'{st.type}  {st.resolution}') # add items to the combo box
                elif st.type == "audio":
                    #print(st.type + ' ' + st.abr)
                    self.comboBox.addItem(f'{st.type}  {st.abr}')

        except Exception:
            QMessageBox.warning(self , "Download status" , "Video not found")


    def Handel_Youtube_Video_browse(self):
        #حفظ الملف بدون ادخال الاسم
        save_place = QFileDialog.getExistingDirectory(self , "Save as" , )
        #Getting the saving path
        self.lineEdit_3.setText(save_place)
        self.lineEdit_5.setText(save_place)  # for playlists

    def Download_Youtube_Video(self):
        try:
            video_link = self.lineEdit_4.text()
            video = YouTube(video_link)
            quality = self.comboBox.currentIndex()  #القيمة الحالية الخاصة بالكومبو بوكس
            st = video.streams
            save_place = self.lineEdit_3.text()
            download = st[quality].download(save_place)      
        except Exception:
            QMessageBox.warning(self , "Download status" , "Download faild")
            return
        # في حال انهاء التحميل بنجاح
        QMessageBox.information(self , "Download satus" , "Done")
        self.lineEdit_4.setText('')
        self.lineEdit_3.setText('')

####################################### PLAY LIST ##########################################

    def Playlist_Download(self):
        try:
            playlist_link = self.lineEdit_6.text()
            playlist = Playlist(playlist_link)
        except Exception:
            QMessageBox.warning(self , "Error" , "Playlist Not Found")
            return
        video_count = playlist.length     #Number of videos in the playlist 
        remaining_video_count = 0     
        quality = self.comboBox_2.currentIndex()
        save_place = self.lineEdit_5.text()
        for video in playlist.videos:
            #Create Youtube object
            vid_url = video.watch_url
            yt = YouTube(url=vid_url, on_progress_callback=self.on_progress) 

            res_144p = yt.streams.get_by_resolution('144')
            res_480p = yt.streams.get_by_resolution('480p')
            res_720p = yt.streams.get_by_resolution('720p')
            res_360p = yt.streams.get_by_resolution('360p')
            res_1080p = yt.streams.get_by_resolution('1080')


            #Error in this part
            # if quality == 0 and yt.streams.filter(file_extension='mp4', progressive=True):
            #     #file_size = round((res_144p.filesize / 1000000), 2)
            #     res_144p.download(save_place) 
            if quality == 0 and yt.streams.filter(file_extension='mp4', progressive=True):
                file_size = round((res_360p.filesize / 1000000), 2)
                res_360p.download()
                video_count -=1
                self.label_11.setText(str(video_count))
                QApplication.processEvents()
            elif quality == 1 and yt.streams.filter(file_extension='mp4', progressive=True):
                file_size = round((res_480p.filesize / 1000000), 2)
                res_480p.download()
                video_count -=1
                self.label_11.setText(str(video_count))
                QApplication.processEvents()
            elif quality == 2 and yt.streams.filter(file_extension='mp4', progressive=True):
                file_size = round((res_720p.filesize / 1000000), 2)
                res_720p.download()
                video_count -=1
                self.label_11.setText(str(video_count))
                QApplication.processEvents()
            elif quality == 3 and yt.streams.filter(file_extension='mp4', progressive=True):
                file_size = round((res_1080p.filesize / 1000000), 2)
                res_1080p.download()
                video_count -=1
                self.label_11.setText(str(video_count))
                QApplication.processEvents()
         
    def on_progress(self , stream, chunk, bytes_remaining):
        progress = 100-(bytes_remaining/stream.filesize * 100)
        self.progressBar_2.setValue(int(progress))
        QApplication.processEvents()  # not responding solution

    # def progress_val(self ,progress):
    #     self.progressBar_2.setValue(progress)
    #     QApplication.processEvents()  # not responding solution

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__== '__main__':
    main()