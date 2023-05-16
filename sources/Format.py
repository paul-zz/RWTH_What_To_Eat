def print_mensa_dish(dish_dict):
    category, name, price = get_dish_data(dish_dict)
    print(f"{category}\n-{name}\n-{price}")

def get_dish_data(dish_dict):
    category = dish_dict['category']
    name = dish_dict['name']
    price = dish_dict['price']
    return category, name, price