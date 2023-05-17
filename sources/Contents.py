content_dict = {
                '1': 'food colouring',
                '2': 'preservatives',
                '3': 'antioxidants',
                '4': 'flavour enhancer',
                '5': 'sulphurized',
                '6': 'blackened',
                '7': 'waxed',
                '8': 'phosphate',
                '9': 'sweetener',
                '10': 'contains a source of phenylalanine',
                'A': 'gluten',
                'A1': 'wheat',
                'A2': 'rye',
                'A3': 'barley',
                'A4': 'oat',
                'A5': 'spellet',
                'B': 'celery',
                'C': 'crustaceans',
                'D': 'eggs',
                'E': 'fish',
                'F': 'peanuts',
                'G': 'soybeans',
                'H': 'milk',
                'I': 'nuts',
                'I1': 'almonds',
                'I2': 'hazelnuts',
                'I3': 'walnuts',
                'I4': 'cashews',
                'I5': 'pecans',
                'I6': 'Brazil nuts',
                'I7': 'pistachios',
                'I8': 'macadamia nuts',
                'J': 'mustard',
                'K': 'sesame seeds',
                'L': 'sulphur dioxide or sulphites',
                'M': 'lupins',
                'N': 'molluscs',
                }

def get_content_name(serial_number : str):
    # get content name using its serial number
    return content_dict[serial_number]

def get_all_serial_numbers():
    return content_dict.keys()

def get_all_contents_list():
    # get all contents in a list containing strings
    contents_list = [f"{k}: {v}" for k, v in content_dict.items()]
    return contents_list

def get_serial_number(content_string : str):
    splitted_string = content_string.split(":")
    get_serial_number = splitted_string[0]
    return get_serial_number