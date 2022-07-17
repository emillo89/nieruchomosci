from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DETAILS = ['Powierzchnia','Forma własności','Liczba pokoi', 'Stan wykończenia','Piętro', 'Balkon / ogród / taras',
           'Czynsz','Miejsce parkingowe','Obsługa zdalna','Ogrzewanie','Rynek', 'Typ ogłoszeniodawcy','Dostępne od',
           'Rok budowy','Rodzaj zabudowy','Okna','Winda','Media','Zabezpieczenia','Wyposażenie','Informacje dodatkowe',
           'Materiał budynku']

UNIT = 60


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
                if details['Piętro'] == None:
                    details['Piętro'] = None
                elif details['Piętro'].split('/')[0] == 'parter':
                    cut = details['Piętro'].split('/')
                    details['Piętro'] = f'1/{cut[1]}'
                    print("Udało się")
                else:
                    details['Piętro'] == None
                # if details[key].endswith('Film'):
                #     details[key] = None
        return details
    return wrapper


def show_offert(func):
    def wrapper(*args):
        nr = func(*args)
        offert_nr = nr.split(' ')[-1]
        return offert_nr
    return wrapper


def show_data(func):
    def wrapper(*args):
        unit = ['sekunda', 'sekundy', 'sekund', 'minutę', 'minuty', 'minut', 'dzień', 'dni', 'miesiąc',
                'miesiące', 'miesięcy', 'rok', 'lata' ]
        now = datetime.now()
        try:
            data_info = func(*args).split(' ')
        except UnboundLocalError:
            time_ago = 0
            time_unit = 'sekunda'
        else:
            time_ago = data_info[-3]
            time_unit = data_info[-2]
        if time_ago == '' or time_ago=='aktualizacji' or time_ago=='dodania':
            time_ago = 1
        if time_unit in unit:
            try:
                if time_unit == 'sekundę' or time_unit == 'sekundy' or time_unit == 'sekund':
                    time_delta = now - timedelta(seconds=int(time_ago))
                if time_unit == 'minutę' or time_unit=='minuty' or time_unit =='minut':
                    time_delta = now - timedelta(minutes=int(time_ago))
                if time_unit == 'dzień' or time_unit == 'dni':
                    time_delta = now - timedelta(days=int(time_ago))
                if time_unit == 'miesiąc' or time_unit == 'miesięcy':
                    print(f'{time_unit} - {time_ago}')
                    time_delta = now - relativedelta(months=int(time_ago))
                if time_unit == 'rok' or time_unit == 'lata' or time_unit == 'lat':
                    time_delta = now - relativedelta(years=int(time_ago))
                return time_delta.strftime('%Y-%m-%d')
            except UnboundLocalError:
                return
            except ValueError:
                return

        else:
            return f'{time_ago} - {time_unit}'

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
