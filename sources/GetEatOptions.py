import requests
from bs4 import BeautifulSoup



def get_mensa_foodplan(mensa_name = "academica"):
    # Get food plan of today from STW
    URL = "https://www.studierendenwerk-aachen.de/speiseplaene/academica-w-en.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    today_panel = soup.find("div", class_="active-panel")
    print("Found: ")

    dishes_list = []
    sides_list = []

    dishes = today_panel.find_all("td", class_="menue-wrapper")
    for dish in dishes:
        if dish.find("span", class_="menue-item menue-category") != None:
            # Main dishes
            dish_category = dish.find("span", class_="menue-item menue-category")
            dish_name = dish.find("span", class_="menue-item menue-desc")
            dish_name_sups = dish_name.find_all("sup")
            for sup in dish_name_sups:
                sup.extract()
            dish_price = dish.find("span", class_="menue-item menue-price large-price")
            dish_dict = {}
            dish_dict['category'] = dish_category.text
            dish_dict['name'] = dish_name.text.strip("+")
            dish_dict['price'] = dish_price.text
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