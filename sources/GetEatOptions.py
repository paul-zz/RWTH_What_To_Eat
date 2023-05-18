import requests
from bs4 import BeautifulSoup

url_dict = {
    "Academica" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/academica-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html"
    },
    "Ahornstraße" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/ahornstrasse-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/ahornstrasse-w.html"
    },
    "Bistro Templergraben" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/templergraben-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/templergraben-w.html"
    },
    "Bayernallee" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/bayernallee-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/bayernallee-w.html"
    },
    "Eupenerstraße" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/eupenerstrasse-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/eupenerstrasse-w.html"
    },
    "KMAC" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/kmac-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/kmac-w.html"
    },
    "Südpark" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/suedpark-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/suedpark-w.html"
    },
    "Vita" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/vita-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/vita-w.html"
    },
    "Jülich" : {
        "English" : "https://www.studierendenwerk-aachen.de/speiseplaene/juelich-w-en.html",
        "Deutsch" : "https://www.studierendenwerk-aachen.de/speiseplaene/juelich-w.html"
    }
}

def get_mensa_foodplan(mensa_name = "Academica", lang = "English"):
    # Get food plan of today from STW
    URL = get_menu_url(mensa_name, lang)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    today_panel = soup.find("div", class_="active-panel")
    print("Found: ")

    dishes_list = []
    sides_list = []

    if today_panel:
        # If there is food plan today, load the data
        # (no food play when it's holiday or canteen is closed)
        dishes = today_panel.find_all("td", class_="menue-wrapper")
        for dish in dishes:
            if dish.find("span", class_="menue-item menue-category") != None:
                # Main dishes
                dish_category = dish.find("span", class_="menue-item menue-category")
                dish_name = dish.find("span", class_="menue-item menue-desc")
                dish_name_sups = dish_name.find_all("sup")
                dish_sup_lst = []
                for sup in dish_name_sups:
                    sup_text_split = sup.text.strip().split(",")
                    dish_sup_lst.extend(sup_text_split)
                    sup.extract()
                dish_price = dish.find("span", class_="menue-item menue-price large-price")
                dish_dict = {}
                dish_dict['category'] = dish_category.text
                dish_dict['name'] = dish_name.text.strip("+")
                dish_dict['price'] = dish_price.text
                dish_dict['contents'] = dish_sup_lst
                dishes_list.append(dish_dict)
                # print("Category: "+dish_category.text)
                # print("Name: " + dish_name.text)
                # print("Price: " + dish_price.text)
                # print()
            elif dish.find("span", class_="menue-item extra menue-category") != None:
                # Sides
                dish_category = dish.find("span", class_="menue-item extra menue-category")
                dish_name = dish.find("span", class_="menue-item extra menue-desc")
                side_dict = {}
                side_dict['category'] = dish_category.text
                side_dict['name'] = dish_name
                sides_list.append(side_dict)
                # print("Category: "+dish_category.text)
                # print("Name: " + dish_name.text)
    return dishes_list, sides_list

def get_menu_url(mensa_name = "Academica", lang = "English"):
    return url_dict[mensa_name][lang]

def get_mensa_names():
    names = list(url_dict.keys())
    return names
