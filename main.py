import os, sys
import random
import typing
import time

from PyQt5 import QtCore
from sources.GetEatOptions import get_mensa_foodplan
from sources.Format import print_mensa_dish, get_dish_data
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QDesktopServices
from PyQt5.QtWidgets import (QApplication, 
                             QAction,
                             QToolBar, 
                             QMainWindow, 
                             QFileDialog,
                             QWidget, 
                             QLabel,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QMessageBox,
                             QInputDialog,
                             QFontDialog,
                             QColorDialog,
                             QSplashScreen,
                             QPushButton)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    window = None

    def run(self):
        for i in range(50):
            dish = random.choice(window.main_list)
            category, name, price = get_dish_data(dish)
            window.top_label.setText(category)
            window.mid_label.setText(name)
            window.bottom_label.setText(price)
            time.sleep(0.01)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I'm gonna eat")

        # Data
        main_list, side_list = get_mensa_foodplan()
        self.main_list = main_list

        # Layout
        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()

        # Left : the labels
        top_font = QFont("Bahnschrift", 24, QFont.Weight.Normal, italic=False)
        mid_font = QFont("Bahnschrift", 48, QFont.Weight.Bold, italic=False)
        bottom_font = QFont("Bahnschrift", 24, QFont.Weight.Normal, italic=False)
        self.top_label = QLabel("Make")
        self.top_label.setFont(top_font)
        self.mid_label = QLabel("Your Decision")
        self.mid_label.setFont(mid_font)
        self.bottom_label = QLabel("Now")
        self.bottom_label.setFont(bottom_font)

        vbox_left.addWidget(self.top_label)
        vbox_left.addWidget(self.mid_label)
        vbox_left.addWidget(self.bottom_label)
        

        # Right : the buttons and settings
        self.button_roll = QPushButton("Roll!")
        self.button_roll.setFont(bottom_font)
        self.button_roll.clicked.connect(self.onRollButtonClick)
        vbox_left.addWidget(self.button_roll)

        hbox_main = QHBoxLayout()
        hbox_main.addLayout(vbox_left, 75)
        #hbox_main.addLayout(vbox_right, 25)

        container = QWidget()
        container.setLayout(hbox_main)
        self.setCentralWidget(container)
        

    def onRollButtonClick(self):
        self.button_roll.setEnabled(False)
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        self.worker.window = self
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda : self.button_roll.setEnabled(True))
        # Step 6: Start the thread
        self.thread.start()


if __name__ == "__main__":
    # create the application
    app = QApplication(sys.argv)

    # load the main window
    window = MainWindow()
    window.show()

    # execution
    app.exec()