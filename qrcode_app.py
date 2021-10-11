import sys
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

    def read_QR(self):
        qr_path, _ = QFileDialog.getOpenFileName(self,
                                                 'Ler QRCode',
                                                 'c:\\',
                                                 "Image files (*.jpg *.png)")
        pixmap = QPixmap(qr_path)
        self.label_read_QR.setPixmap(pixmap)
        qr = decode(Image.open(qr_path))
        print(qr)
        self.textEdit.setText(qr[0][0].decode('utf-8', 'ignore'))

    def create_QR(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4)
        qr.add_data('Some data')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
