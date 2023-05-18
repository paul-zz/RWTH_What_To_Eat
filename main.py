import os, sys, platform, ctypes
import random
import typing
import time

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QSize, QUrl, QT_VERSION_STR, PYQT_VERSION_STR
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QDesktopServices
from PyQt5.QtWidgets import (QApplication, 
                             QAction,
                             QToolBar, 
                             QMainWindow, 
                             QWidget, 
                             QLabel,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QSplashScreen,
                             QMessageBox,
                             QPushButton)

from sources import AssetLoader
from sources import SettingManager
from sources.SettingWindow import SettingWindow
from sources.GetEatOptions import get_mensa_foodplan, get_menu_url
from sources.Format import print_mensa_dish, get_dish_data
from sources.Contents import get_serial_number, get_content_name

developer = "paul-zz"
version = "1.00"
py_ver = sys.version
qt_ver = QT_VERSION_STR
pyqt_ver = PYQT_VERSION_STR
platform_name = platform.system()

if platform_name == "Windows":
    # Enable windows taskbar icon
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    window = None

    def run(self):
        for i in range(50):
            dish = random.choice(self.window.all_option_list)
            category, name, price = get_dish_data(dish)
            self.window.top_label.setText(category)
            self.window.mid_label.setText(name)
            self.window.bottom_label.setText(price)
            time.sleep(0.01)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I'm gonna eat")
        self.setWindowIcon(AssetLoader.load_icon("plate-cutlery.png"))
        # Data
        self.settings_dict, ok = SettingManager.load_settings()
        self.main_list = None
        self.side_list = None
        self.all_option_list = None
        
        # Toolbar
        toolbar = QToolBar("Toolbar", self)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.action_set = QAction(AssetLoader.load_icon("gear.png"), "Settings", self)
        self.action_go = QAction(AssetLoader.load_icon("external.png"), "Visit menu of today", self)
        self.action_git = QAction(AssetLoader.load_icon("git.png"), "Visit Github Repository", self)
        self.action_about = QAction(AssetLoader.load_icon("information-frame.png"), "about", self)
        toolbar.addAction(self.action_set)
        toolbar.addAction(self.action_go)
        toolbar.addAction(self.action_git)
        toolbar.addAction(self.action_about)
        self.action_set.triggered.connect(self.actionSettingsTriggered)
        self.action_go.triggered.connect(self.actionGoTriggered)
        self.action_git.triggered.connect(self.actionGitTriggered)
        self.action_about.triggered.connect(self.actionAboutTriggered)

        # Layout
        vbox_left = QVBoxLayout()

        # the labels
        top_font = self.settings_dict["font_top"]
        mid_font = self.settings_dict["font_mid"]
        bottom_font = self.settings_dict["font_bottom"]
        self.top_label = QLabel("Make")
        self.top_label.setFont(top_font)
        self.mid_label = QLabel("Your Decision")
        self.mid_label.setFont(mid_font)
        self.bottom_label = QLabel("Now")
        self.bottom_label.setFont(bottom_font)

        vbox_left.addWidget(self.top_label)
        vbox_left.addWidget(self.mid_label)
        vbox_left.addWidget(self.bottom_label)
        
        # button below
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

        # apply settings before startup
        self.applySettings()
        
    def onRollButtonClick(self):
        if len(self.all_option_list) > 0:
            # Roll only if there are available dining options
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
        else:
            # No available dining options
            if len(self.main_list) == 0:
                reason = "The selected mensa may be closed today."
            else:
                reason = "The food offered by mensa today may not be suitable for you."
            QMessageBox(QMessageBox.Icon.Information, "Notice", f"No dining options. {reason} You may check its official website. But you can still add your own dining options in the settings.", parent=self).exec()


    def actionSettingsTriggered(self):
        # Go to settings
        msg = SettingWindow(self)
        msg.setValue(self.settings_dict)
        if msg.exec_():
            self.settings_dict = msg.getValue()
            self.applySettings()
        SettingManager.export_settings(self.settings_dict)

    def actionGoTriggered(self):
        # Go to menu of today
        url = get_menu_url(self.settings_dict["mensa_name"], self.settings_dict["menu_lang"])
        QDesktopServices.openUrl(QUrl(url))

    def actionGitTriggered(self):
        QDesktopServices.openUrl(QUrl("https://github.com/paul-zz/RWTH_What_To_Eat"))

    def actionAboutTriggered(self):
        about_dlg = QMessageBox()
        about_dlg.setWindowIcon(AssetLoader.load_icon("information-frame.png"))
        about_dlg.setWindowTitle("About")
        about_dlg.setText("RWTH What-to-eat")
        about_dlg.setDetailedText(f"Python: {py_ver}\nQt: {qt_ver}\nPyQt: {pyqt_ver}\nOS: {platform_name}")
        about_dlg.setInformativeText(f"v{version} by {developer}")
        about_dlg.setIcon(QMessageBox.Information)
        about_dlg.exec()

    def applySettings(self):
        # Apply the settings
        self.top_label.setFont(self.settings_dict["font_top"])
        self.mid_label.setFont(self.settings_dict["font_mid"])
        self.bottom_label.setFont(self.settings_dict["font_bottom"])
        self.main_list, self.side_list = get_mensa_foodplan(self.settings_dict["mensa_name"], self.settings_dict["menu_lang"])
        self.makeOptions()

    def makeOptions(self):
        # Generate all available options
        self.all_option_list = []
        other_list = self.settings_dict["option_list"]
        taboo_list = [get_serial_number(x) for x in self.settings_dict["taboo_list"]]
        for dish in self.main_list:
            contents = dish["contents"]
            taboo_contents = set(contents) & set(taboo_list)
            if not taboo_contents:
                # Have nothing in common
                self.all_option_list.append(dish)
            else:
                taboo_contents_list = [f"{x}: {get_content_name(x)}" for x in list(taboo_contents)]
                QMessageBox(QMessageBox.Icon.Information, "Notice", f"You may not eat {dish['name']} because it contains {','.join(taboo_contents_list)}. It has been removed from the list.", parent=self).exec()
        for option in other_list:
            # TODO: Later parse option from string to a dict
            option_dict = {}
            option_dict["category"] = ""
            option_dict['name'] = option
            option_dict['price'] = ""
            option_dict['contents'] = ""
            self.all_option_list.append(option_dict)
        



if __name__ == "__main__":
    # create the application
    app = QApplication(sys.argv)

    # load a splash screen
    splash_pixmap = QPixmap("./assets/images/wait.png")
    splash = QSplashScreen(splash_pixmap)
    splash.show()

    # load the main window
    main_window = MainWindow()
    main_window.show()
    splash.destroy()

    # execution
    app.exec()