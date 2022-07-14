def check_price(func):
    def wrapper(*args):
        price = func(*args)
        if price == 'Zapytajocenę':
            price = None
        return price
    return wrapper


# def change_zapytaj(text):
#     if text == 'zapytaj':
#         text = None
#     return text
#
#
# def check_price(text):
#     if text == 'Zapytajocenę':
#         return True
#     return False