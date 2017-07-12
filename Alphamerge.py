from PySide import QtGui, QtCore
import os
import sys
from PIL import Image, ImageDraw
import threading

################################
path = r"D:\MyPython\alphamerge"
if path not in sys.path:
    sys.path.append(path)
import myUI
################################

app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
UI = myUI.Ui_alphamerge()
UI.setupUi(window)


class Merge():
    def __init__(self):
        self.lineEdit_Image_Source = ''
        self.lineEdit_Image_Alpha = ''
        self.isSameImage_Source = ''
        self.isSameImage_Alpha  = ''

        self.progressBar = 0
        self.refresh = QtCore.QTimer()
        self.refresh.timeout.connect(lambda: Merge.variables(self))
        self.refresh.start(1000)



    def variables(self):
        self.lineEdit_Save_Path = UI.lineEdit_Save_Path.text()
        UI.progressBar.setProperty("value", self.progressBar)



        self.lineEdit_Image_Source = UI.lineEdit_Image_Source.text()
        self.lineEdit_Image_Alpha = UI.lineEdit_Image_Alpha.text()


        if self.lineEdit_Image_Alpha != self.isSameImage_Alpha or self.lineEdit_Image_Source!=self.isSameImage_Source:
            UI.label_Image_Source_image.setPixmap(QtGui.QPixmap(r'{}'.format(self.lineEdit_Image_Source)))
            UI.label_Image_Alpha_image.setPixmap(QtGui.QPixmap(r'{}'.format(self.lineEdit_Image_Alpha)))

        self.isSameImage_Source = self.lineEdit_Image_Source
        self.isSameImage_Alpha = self.lineEdit_Image_Alpha


    def pushButton_Merge_Alpha(self):

        image = Image.open(self.lineEdit_Image_Source).convert('RGBA')
        alpha = Image.open(self.lineEdit_Image_Alpha).convert('RGBA')

        alpha_data = alpha.load()
        image_data = image.load()

        for y in range(alpha.size[1]):
            for x in range(alpha.size[0]):
                if self.__running:
                    self.progressBar = (y / alpha.size[1])*100
                    if sum(alpha_data[x, y][0:3])/3 == alpha_data[x, y][0]:
                        image_data[x, y] = (image_data[x, y][0], image_data[x, y][1], image_data[x, y][2], alpha_data[x, y][1])

        if self.__running:
            image.save(self.lineEdit_Save_Path, format="PNG")
            UI.progressBar.setProperty("value", 100)

    def Threading(self):
        self.__running = True
        self.Thread = threading.Thread(target=lambda: self.pushButton_Merge_Alpha())
        self.Thread.start()
    def Cancel(self):
        self.__running = False

    def image_source(self):
        fileName = QtGui.QFileDialog.getOpenFileName(filter="Images (*.png *.bmp *.jpg)")[0]
        UI.lineEdit_Image_Source.setText(fileName)

    def image_alpha(self):
        fileName = QtGui.QFileDialog.getOpenFileName(filter="Images (*.png *.bmp *.jpg)")[0]
        UI.lineEdit_Image_Alpha.setText(fileName)

    def save_path(self):
        fileName = QtGui.QFileDialog.getSaveFileName(filter="Images (*.png *.bmp *.jpg)")[0]
        UI.lineEdit_Save_Path.setText(fileName)


Root = Merge()

UI.pushButton_Merge_Alpha.clicked.connect(lambda: Root.Threading())

UI.toolButton_Image_Source_get_path.clicked.connect(lambda: Root.image_source())
UI.toolButton_Image_Alpha_get_path.clicked.connect(lambda: Root.image_alpha())
UI.toolButton_Save_Path_get_path.clicked.connect(lambda: Root.save_path())
UI.pushButton_Cancel.clicked.connect(lambda: Root.Cancel())
if __name__ == "__main__":
    window.show()
    sys.exit(app.exec_())
