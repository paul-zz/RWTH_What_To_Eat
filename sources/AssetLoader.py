import os
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QDesktopServices


def load_icon(name : str):
    base_dir = "./assets/icons/"
    return QIcon(os.path.join(base_dir, name))
