DETAILS = ['Powierzchnia','Forma własności','Liczba pokoi', 'Stan wykończenia','Piętro', 'Balkon / ogród / taras',
           'Czynsz','Miejsce parkingowe','Obsługa zdalna','Ogrzewanie','Rynek', 'Typ ogłoszeniodawcy','Dostępne od',
           'Rok budowy','Rodzaj zabudowy','Okna','Winda','Media','Zabezpieczenia','Wyposażenie','Informacje dodatkowe',
           'Materiał budynku']


def check_price(func):
    def wrapper(*args):
        price = func(*args)
        if price == 'Zapytajocenę':
            price = None
        return price
    return wrapper


def check_location(func):
    def wrapper(*args):
        locations = func(*args)
        locations = [locate.getText() for locate in locations]
        try:
            kind_of_investment = locations[0].split(' ')[0]
        except IndexError:
            kind_of_investment=None

        try:
            city = locations[2]
        except IndexError:
            city = None
        try:
            province = locations[1]
        except IndexError:
            province = None
        try:
            district = locations[3]
        except IndexError:
            district = None
        try:
            street = locations[-1]
        except IndexError:
            street = None
        else:
            if not street.startswith('ul.'):
                street = None
        return kind_of_investment,city,province,district,street
    return wrapper


def take_all_details(func):
    def wrapper(*args, **kwargs):
        details = func(*args, **kwargs)
        for key in DETAILS:
            try:
                details[key]
            except KeyError:
                details[key] = None
            except AttributeError:
                details[key] = None
            else:
                if details[key].endswith('m²'):
                    details[key] = details[key].split(' ')[0].replace(',','.')
                if details[key].endswith('zł'):
                    details[key] = details[key].replace(' ','').split('zł')[0]
                if details[key] == 'zapytaj':
                    details[key] = None
                if details['Piętro'].split('/')[0] == 'parter':
                    cut = details['Piętro'].split('/')
                    details['Piętro'] = f'1/{cut[1]}'
                    print("Udało się")
                else:
                    details['Piętro'] == None
                # if details[key].endswith('Film'):
                #     details[key] = None
        return details
    return wrapper

'''Not use'''
def take_details(func):
    def wrapper(*args):
        info = func(*args)
        long = len(info)
        details = {}
        for index in range(0, long, 2):
            details[info[index]] = info[index + 1]
        return details
    return wrapper
