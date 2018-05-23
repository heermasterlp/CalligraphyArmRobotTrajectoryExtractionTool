import sys
import math
import cv2
import os
import csv
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from mainWindow import Ui_MainWindow
from utils import getContourOfImage, getSkeletonOfImage, createBlankGrayscaleImage


class CalligraphyArmRobotTrajectoryExtractionTool(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(CalligraphyArmRobotTrajectoryExtractionTool, self).__init__()
        self.setupUi(self)

        self.image_path = ""
        self.image_name = ""

        self.scale = 700

        self.image_gray = None
        self.image_contour = None
        self.image_skeleton = None
        self.image_merge = None

        self.image_pix = QPixmap()
        self.temp_image_pix = QPixmap()

        self.main_scene = GraphicsScene()
        self.main_scene.setBackgroundBrush(Qt.gray)
        self.main_gview.setScene(self.main_scene)

        self.lastPoint = None
        self.endPoint = None

        # add listener
        self.open_btn.clicked.connect(self.handle_open_btn)
        self.clear_btn.clicked.connect(self.handle_clear_btn)
        self.exit_btn.clicked.connect(self.handle_exit_btn)
        self.save_btn.clicked.connect(self.handle_save_btn)

    def handle_open_btn(self):
        print("Open button clicked!")
        self.main_scene.clear()
        self.lastPoint = None
        self.endPoint = None

        filename, _ = QFileDialog.getOpenFileName(None, "Open File", QDir.currentPath())
        if filename:
            self.image_path = filename
            self.image_name = os.path.splitext(os.path.basename(filename))[0]

            qimg = QImage(filename)
            if qimg.isNull():
                QMessageBox.information(self, "Image viewer", "Cannot load %s." % filename)
                return

            # grayscale image
            img_ = cv2.imread(filename, 0)
            _, img_ = cv2.threshold(img_, 127, 255, cv2.THRESH_BINARY)
            self.image_gray = img_.copy()

            contour = getContourOfImage(img_)

            skeleton = getSkeletonOfImage(img_)

            img_merge = createBlankGrayscaleImage(img_)

            for y in range(img_.shape[0]):
                for x in range(img_.shape[1]):
                    if contour[y][x] == 0.0:
                        img_merge[y][x] = 0.0
                    if skeleton[y][x] == 0.0:
                        img_merge[y][x] = 0.0

            self.image_contour = contour.copy()
            self.image_skeleton = skeleton.copy()
            self.image_merge = img_merge.copy()

            qimg = QImage(img_merge.data, img_merge.shape[1], img_merge.shape[0], img_merge.shape[1], QImage.Format_Indexed8)
            self.image_pix = QPixmap.fromImage(qimg)
            self.temp_image_pix = self.image_pix.copy()
            self.main_scene.addPixmap(self.image_pix)
            self.main_scene.update()

            self.statusbar.showMessage("Open file successed!")



    def handle_clear_btn(self):
        print("Clear button clicked!")

        self.main_scene.lastPoint = None
        self.main_scene.endPoint = None
        self.main_scene.trajectory_points = []

        self.image_pix = self.temp_image_pix.copy()
        self.main_scene.addPixmap(self.image_pix)
        self.main_scene.update()

        self.statusbar.showMessage("Clear successed!")

    def handle_exit_btn(self):
        print("Exit button clicked!")
        qApp = QApplication.instance()
        sys.exit(qApp.exec_())

    def handle_save_btn(self):
        print("Save button clicked!")

        print(self.main_scene.trajectory_points)

        print(type(self.x0_lineedit.text()))
        print(self.x0_lineedit.text())

        x0 = float(self.x0_lineedit.text())
        y0 = float(self.y0_lineedit.text())
        z0 = float(self.z0_lineedit.text())

        points = []
        for pt in self.main_scene.trajectory_points:
            points.append((pt[0] * 0.1 / self.scale, pt[1] * 0.1 / self.scale, z0))

        if len(points) == 0:
            QMessageBox.information(self, "Points ", "Points are null!")
            return

        # save to selected path
        filename = str(QFileDialog.getExistingDirectory(self, "Selected Directory"))
        print(filename)
        file_path = filename + "/data.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(points)

        self.statusbar.showMessage("Save to CSV file successed!")



class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

        self.lastPoint = None
        self.endPoint = None

        self.trajectory_points = []

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        pen = QPen(Qt.red)
        brush = QBrush(Qt.red)

        x = event.scenePos().x()
        y = event.scenePos().y()

        self.addEllipse(x, y, 2, 2, pen, brush)

        self.trajectory_points.append((x, y))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CalligraphyArmRobotTrajectoryExtractionTool()
    mainWindow.show()
    sys.exit(app.exec_())
