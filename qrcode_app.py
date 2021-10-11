import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
# TODO: Converter imagens (possivelmente precisa de servidor)
qtCreatorFile = "mainwindow.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.toolButton_read_QR.clicked.connect(self.read_QR)
        self.pushButton_convert_text.clicked.connect(self.create_QR)
        self.pushButton_save.clicked.connect(self.save_QR)

    def read_QR(self):
        qr_path, _ = QFileDialog.getOpenFileName(self,
                                                 'Ler QRCode',
                                                 f"{os.environ['USERPROFILE']}"
                                                 r"\Images",
                                                 "Image files (*.jpg *.png)")
        if qr_path:
            pixmap = QPixmap(qr_path)
            self.label_read_QR.setPixmap(pixmap)
            code = decode(Image.open(qr_path))
            text = code[0][0].decode('utf-8', 'ignore')
            self.textEdit.setText(text)

    def create_QR(self):
        text = self.lineEdit.text()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4)
        qr.add_data(text)
        qr.make(fit=True)
        self.code = qr.make_image(fill_color="black", back_color="white")
        temp = 'temp.png'
        self.code.save(temp)
        pixmap = QPixmap(temp)
        self.label_text_QR.setPixmap(pixmap)
        os.remove(temp)

    def save_QR(self):
        save, _ = QFileDialog.getSaveFileName(self,
                                              'Salvar QR code',
                                              f"{os.environ['USERPROFILE']}\\"
                                              r"Images\\",
                                              "Image file (*.png)")
        if save:
            self.code.save(save)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
