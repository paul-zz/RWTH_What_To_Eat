import os
import yaml
from PyQt5.QtGui import QFont


def load_settings():
    # Load the settings from file
    # Returns (settings_dict, ok)
    settings_path = "./data/settings.yml"
    if os.path.exists(settings_path):
        # If file exists, read it
        try:
            # if successfully loaded
            settings_dict = {}
            with open(settings_path, "r") as f:
                dict_read = yaml.safe_load(f)
            settings_dict["mensa_name"] = dict_read["mensa_name"]
            settings_dict["taboo_list"] = dict_read["taboo_list"]
            settings_dict["option_list"] = dict_read["option_list"]
            settings_dict["menu_lang"] = dict_read["menu_lang"]
            settings_dict["font_top"] = QFont(dict_read["font_top"]["family"], dict_read["font_top"]["pointsize"], dict_read["font_top"]["weight"], dict_read["font_top"]["italic"])
            settings_dict["font_mid"] = QFont(dict_read["font_mid"]["family"], dict_read["font_mid"]["pointsize"], dict_read["font_mid"]["weight"], dict_read["font_mid"]["italic"])
            settings_dict["font_bottom"] = QFont(dict_read["font_bottom"]["family"], dict_read["font_bottom"]["pointsize"], dict_read["font_bottom"]["weight"], dict_read["font_bottom"]["italic"])
            settings_dict["font_button"] = QFont(dict_read["font_button"]["family"], dict_read["font_button"]["pointsize"], dict_read["font_button"]["weight"], dict_read["font_button"]["italic"])
            return settings_dict, True
        except Exception as e:
            return create_default_settings(), False
    else:
        # If setting file doesn't exist, create default
        return create_default_settings(), True

def export_settings(settings_dict : dict):
    # Export settings dict to yaml file
    settings_path = "./data/settings.yml"
    settings_new_dict = {}
    for k, v in settings_dict.items():
        key = k
        if type(v) == QFont:
            value = {}
            value["family"] = v.family()
            value["pointsize"] = v.pointSize()
            value["weight"] = v.weight()
            value["italic"] = v.italic()
        else:
            value = v
        settings_new_dict[key] = value
    with open(settings_path, "w") as f:
        yaml.dump(settings_new_dict, f)


def create_default_settings():
    settings_dict = {}
    settings_dict["mensa_name"] = "Academica"
    settings_dict["taboo_list"] = []
    settings_dict["option_list"] = []
    settings_dict["menu_lang"] = "English"
    settings_dict["font_top"] = QFont("Arial", 24, QFont.Weight.Normal, italic=False)
    settings_dict["font_mid"] = QFont("Arial", 48, QFont.Weight.Bold, italic=False)
    settings_dict["font_bottom"] = QFont("Arial", 24, QFont.Weight.Normal, italic=False)
    settings_dict["font_button"] = QFont("Arial", 24, QFont.Weight.Normal, italic=False)
    return settings_dict

