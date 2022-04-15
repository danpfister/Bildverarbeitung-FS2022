import sys,os,cv2
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QGridLayout, QFileDialog
from libs.gui import Ui_MainWindow
import numpy as np

from libs.utils import convert_cv2img_to_QPixmap
from libs.morphology import segment_util, close_hole_util, count_coins_util, text_recog_util


LABEL_WIDTH = 500
LABEL_HEIGHT = 500


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # global variable
        self.img_path = None

        # register event
        self.actionOpen.triggered.connect(self.show_img)
        self.actionRestore.triggered.connect(self.restore_img)
        self.actionSegmentation.triggered.connect(self.segment_coin)
        self.actionClosehole.triggered.connect(self.close_hole)
        self.actionCount.triggered.connect(self.count_coins)
        self.actionText_recog.triggered.connect(self.text_recog)

    
    def print_edited_img(self,img):
        pixmap = convert_cv2img_to_QPixmap(img[:,:,None].astype(np.uint8))
        pixmap = pixmap.scaled(LABEL_WIDTH, LABEL_HEIGHT, QtCore.Qt.KeepAspectRatio)
        self.edit_img.setPixmap(pixmap)


    def show_img(self):
        """
        Open one img
        """
        img = QFileDialog.getOpenFileName(None,'OpenFile','',"img file(*.png *.jpg *.jpeg)")
        imgPath = img[0]
        self.img_path = imgPath
        pixmap = QPixmap(imgPath)
        pixmap = pixmap.scaled(LABEL_WIDTH, LABEL_HEIGHT, QtCore.Qt.KeepAspectRatio)
        self.raw_img.setPixmap(pixmap)
        self.edit_img.setPixmap(pixmap)
    
    def restore_img(self):
        """
        Restore the original image
        """
        pixmap = QPixmap(self.img_path)
        pixmap = pixmap.scaled(LABEL_WIDTH, LABEL_HEIGHT, QtCore.Qt.KeepAspectRatio)
        self.edit_img.setPixmap(pixmap)

    # --------------------------------- Q 2.1 ---------------------------------------   
    # --------------------------------- Q 2.1.1 -------------------------------------
    def segment_coin(self):
        """
        Load the coin.png --> segment and save it, and show it in the right figure
        """
        img = cv2.imread(self.img_path)
        coin_img_seg = segment_util(img) * 255
        cv2.imwrite('results/coins_seg.png', coin_img_seg)
        self.print_edited_img(coin_img_seg)


    # --------------------------------- Q 2.1.2 -------------------------------------
    def close_hole(self):
        img = cv2.imread(self.img_path)[:, :, 0] / 255.
        img_close = close_hole_util(img) * 255
        cv2.imwrite('results/coins_close.png', img_close)
        self.print_edited_img(img_close)


    # --------------------------------- Q 2.1.3 -------------------------------------
    def count_coins(self):
        img = cv2.imread(self.img_path)[:, :, 0] / 255.
        img_disconnected, n_comp = count_coins_util(img)
        img_disconnected = img_disconnected * 255
        cv2.imwrite('results/coins_disconnected.png', img_disconnected)
        print('Number of counted components: ' + str(n_comp))
        self.print_edited_img(img_disconnected)

    # --------------------------------- Q 2.2 ---------------------------------------
    def text_recog(self):
        text = cv2.imread(self.img_path)[:, :, 0] / 255.
        letter_not = cv2.imread('inputs/text_m_inv.png')[:, :, 0] / 255.   
        text_recog_results = text_recog_util(text, letter_not) * 255
        cv2.imwrite('results/text_recog_results.png', text_recog_results)
        self.print_edited_img(text_recog_results)



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()