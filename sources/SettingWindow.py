import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, 
                             QDialog,
                             QApplication,
                             QTabWidget,
                             QHBoxLayout,
                             QComboBox,
                             QGroupBox,
                             QLabel,
                             QListWidget,
                             QVBoxLayout,
                             QFormLayout,
                             QInputDialog,
                             QFontDialog,
                             QDialogButtonBox,
                             QPushButton)
from . import AssetLoader
from . import Contents
from .GetEatOptions import get_mensa_names

class MyListWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout_main = QHBoxLayout()
        layout_buttons = QVBoxLayout()
        self.button_add = QPushButton()
        self.button_add.setIcon(AssetLoader.load_icon("plus.png"))
        self.button_add.setFixedSize(32, 32)
        self.button_minus = QPushButton()
        self.button_minus.setIcon(AssetLoader.load_icon("minus.png"))
        self.button_minus.setFixedSize(32, 32)
        layout_buttons.addWidget(self.button_add, alignment=Qt.AlignmentFlag.AlignTop)
        layout_buttons.addWidget(self.button_minus, alignment=Qt.AlignmentFlag.AlignTop)
        layout_buttons.addStretch()
        self.list_widget = QListWidget()
        layout_main.addWidget(self.list_widget)
        layout_main.addLayout(layout_buttons)
        self.setLayout(layout_main)


class SettingTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        # Vars
        self.font_top = QFont()
        self.font_mid = QFont()
        self.font_bottom = QFont()
        self.font_button = QFont()

        # UI
        self.tab_dining_options = QWidget()
        self.tab_other_options = QWidget()

        self.addTab(self.tab_dining_options, "Dining")
        self.addTab(self.tab_other_options, "Others")

        # Under "Dining" Tab
        self.tab_dining_options.layout = QVBoxLayout()
        self.group_mensa = QGroupBox("Mensa Settings", self)
        self.group_other = QGroupBox("Other Settings", self)
        # - Under "Mensa Options" group
        group_mensa_layout = QFormLayout(self)
        self.label_mensa = QLabel("Mensa:")
        self.combo_mensa = QComboBox(self)
        self.combo_mensa.addItems(get_mensa_names())

        self.label_taboo = QLabel("Taboo:")
        self.list_taboo = MyListWidget()
        self.list_taboo.button_add.clicked.connect(self.onTabooAddClick)
        self.list_taboo.button_minus.clicked.connect(self.onTabooMinusClick)
        self.label_taboo_note = QLabel("⚠Note: Allergen information is acquired from STW website and here only for information purpose. For people with allergies please refer to the official website.")
        self.label_taboo_note.setWordWrap(True)
        group_mensa_layout.addRow(self.label_mensa, self.combo_mensa)
        group_mensa_layout.addRow(self.label_taboo, self.list_taboo)
        group_mensa_layout.addWidget(self.label_taboo_note)
        self.group_mensa.setLayout(group_mensa_layout)
      
        # - Under "Other Options" group
        group_other_layout = QFormLayout()
        self.group_other.setLayout(group_other_layout)
        self.label_other_options = QLabel("Options:")
        self.list_other_options = MyListWidget()
        self.list_other_options.button_add.clicked.connect(self.onOtherOptionsAddClick)
        self.list_other_options.button_minus.clicked.connect(self.onOtherOptionsMinusClick)

        group_other_layout.addRow(self.label_other_options, self.list_other_options)
        self.tab_dining_options.layout.addWidget(self.group_mensa)
        self.tab_dining_options.layout.addWidget(self.group_other)
        self.tab_dining_options.setLayout(self.tab_dining_options.layout)

        # Under "Others" tab
        self.tab_other_options.layout = QVBoxLayout()
        # - Under "Display" group
        self.group_disp = QGroupBox("Display Settings", self)
        group_disp_layout = QFormLayout()
        self.label_lang = QLabel("Menu Language:")
        self.combo_lang = QComboBox(self)
        self.combo_lang.addItems(["English", "Deutsch"])
        self.label_font_top = QLabel("Font (top):")
        self.button_font_top = QPushButton("FONT_TOP")
        self.button_font_top.clicked.connect(self.onTopFontButtonClick)
        self.label_font_mid = QLabel("Font (middle):")
        self.button_font_mid = QPushButton("FONT_MID")
        self.button_font_mid.clicked.connect(self.onMidFontButtonClick)
        self.label_font_bottom = QLabel("Font (bottom):")
        self.button_font_bottom = QPushButton("FONT_BOTTOM")
        self.button_font_bottom.clicked.connect(self.onBottomFontButtonClick)
        self.label_font_button = QLabel("Font (button):")
        self.button_font_button = QPushButton("FONT_BUTTON")
        self.button_font_button.clicked.connect(self.onButtonFontButtonClick)

        group_disp_layout.addRow(self.label_lang, self.combo_lang)
        group_disp_layout.addRow(self.label_font_top, self.button_font_top)
        group_disp_layout.addRow(self.label_font_mid, self.button_font_mid)
        group_disp_layout.addRow(self.label_font_bottom, self.button_font_bottom)
        group_disp_layout.addRow(self.label_font_button, self.button_font_button)
        self.group_disp.setLayout(group_disp_layout)
        self.tab_other_options.layout.addWidget(self.group_disp)
        self.tab_other_options.setLayout(self.tab_other_options.layout)

    def refreshButtonLooks(self):
        # Refresh font looks
        font = self.button_font_top.font()
        font.setFamily(self.font_top.family())
        font.setWeight(self.font_top.weight())
        font.setItalic(self.font_top.italic())
        font_description = f"{self.font_top.family()}, {self.font_top.pointSize()}"
        self.button_font_top.setFont(font)
        self.button_font_top.setText(font_description)

        font = self.button_font_mid.font()
        font.setFamily(self.font_mid.family())
        font.setWeight(self.font_mid.weight())
        font.setItalic(self.font_mid.italic())
        font_description = f"{self.font_mid.family()}, {self.font_mid.pointSize()}"
        self.button_font_mid.setFont(font)
        self.button_font_mid.setText(font_description)

        font = self.button_font_bottom.font()
        font.setFamily(self.font_bottom.family())
        font.setWeight(self.font_bottom.weight())
        font.setItalic(self.font_bottom.italic())
        self.button_font_bottom.setFont(font)
        font_description = f"{self.font_bottom.family()}, {self.font_bottom.pointSize()}"
        self.button_font_bottom.setFont(font)
        self.button_font_bottom.setText(font_description)

        font = self.button_font_button.font()
        font.setFamily(self.font_button.family())
        font.setWeight(self.font_button.weight())
        font.setItalic(self.font_button.italic())
        self.button_font_button.setFont(font)
        font_description = f"{self.font_button.family()}, {self.font_button.pointSize()}"
        self.button_font_button.setFont(font)
        self.button_font_button.setText(font_description)

    def onTabooAddClick(self):
        # When add button besides Taboo list is clicked
        item, ok = QInputDialog.getItem(self, "Add", "I'd better not eat food containing:😒", Contents.get_all_contents_list(), 0, editable=False)
        if ok:
            # Make sure no duplicate
            if len(self.list_taboo.list_widget.findItems(item, Qt.MatchFlag.MatchContains)) == 0:
                self.list_taboo.list_widget.addItem(item)

    def onTabooMinusClick(self):
        # When minus button besides Taboo list is clicked
        curr_item = self.list_taboo.list_widget.currentItem()
        if curr_item:
            self.list_taboo.list_widget.takeItem(self.list_taboo.list_widget.row(curr_item))

    def onOtherOptionsAddClick(self):
        # Add other dining options
        item, ok = QInputDialog.getText(self, "Add", "I would also like to eat:🥰")
        if ok:
            if len(self.list_other_options.list_widget.findItems(item, Qt.MatchFlag.MatchContains)) == 0:
                self.list_other_options.list_widget.addItem(item)

    def onOtherOptionsMinusClick(self):
        # Delete that option
        curr_item = self.list_other_options.list_widget.currentItem()
        if curr_item:
            self.list_other_options.list_widget.takeItem(self.list_other_options.list_widget.row(curr_item))

    def onTopFontButtonClick(self):
        current_font = self.button_font_top.font()
        font, ok = QFontDialog.getFont(current_font, self, "Select Font")
        if ok:
            # Set text and refresh the review window
            self.font_top = font
            self.refreshButtonLooks()

    def onMidFontButtonClick(self):
        current_font = self.button_font_mid.font()
        font, ok = QFontDialog.getFont(current_font, self, "Select Font")
        if ok:
            # Set text and refresh the review window
            self.font_mid = font
            self.refreshButtonLooks()

    def onBottomFontButtonClick(self):
        current_font = self.button_font_bottom.font()
        font, ok = QFontDialog.getFont(current_font, self, "Select Font")
        if ok:
            # Set text and refresh the review window
            self.font_bottom = font
            self.refreshButtonLooks()

    def onButtonFontButtonClick(self):
        current_font = self.button_font_button.font()
        font, ok = QFontDialog.getFont(current_font, self, "Select Font")
        if ok:
            # Set text and refresh the review window
            self.font_button = font
            self.refreshButtonLooks()


class SettingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        # Vars

        # UI
        self.setWindowTitle("Settings")
        self.setWindowIcon(AssetLoader.load_icon("gear.png"))
        self.setFixedSize(500, 800)
        self.tabs = SettingTabs()
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(self.buttonBox)

        self.setLayout(vbox)

    def getValue(self):
        settings_dict = {}
        settings_dict["mensa_name"] = self.tabs.combo_mensa.currentText()
        settings_dict["taboo_list"] = [str(self.tabs.list_taboo.list_widget.item(i).text()) for i in range(self.tabs.list_taboo.list_widget.count())]
        settings_dict["option_list"] = [str(self.tabs.list_other_options.list_widget.item(i).text()) for i in range(self.tabs.list_other_options.list_widget.count())]
        settings_dict["menu_lang"] = self.tabs.combo_lang.currentText()
        settings_dict["font_top"] = self.tabs.font_top
        settings_dict["font_mid"] = self.tabs.font_mid
        settings_dict["font_bottom"] = self.tabs.font_bottom
        settings_dict["font_button"] = self.tabs.font_button
        return settings_dict
    
    def setValue(self, settings_dict):
        # Set value and refresh the setting window
        if settings_dict != None:
            self.tabs.combo_mensa.setCurrentText(settings_dict["mensa_name"])
            self.tabs.list_taboo.list_widget.addItems(settings_dict["taboo_list"])
            self.tabs.list_other_options.list_widget.addItems(settings_dict["option_list"])
            self.tabs.combo_lang.setCurrentText(settings_dict["menu_lang"])
            self.tabs.font_top = settings_dict["font_top"]
            self.tabs.font_mid = settings_dict["font_mid"]
            self.tabs.font_bottom = settings_dict["font_bottom"]
            self.tabs.font_button  = settings_dict["font_button"]
            self.tabs.refreshButtonLooks()

        
        
