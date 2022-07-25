from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import datetime

DETAILS = ['Powierzchnia','Forma własności','Liczba pokoi', 'Stan wykończenia','Piętro', 'Balkon / ogród / taras',
           'Czynsz','Miejsce parkingowe','Obsługa zdalna','Ogrzewanie','Rynek', 'Typ ogłoszeniodawcy','Dostępne od',
           'Rok budowy','Rodzaj zabudowy','Okna','Winda','Media','Zabezpieczenia','Wyposażenie','Informacje dodatkowe',
           'Materiał budynku']

UNIT = 60


def check_price(func):
    def wrapper(*args):
        price = func(*args)
        try:
            price = price.getText().replace(' ', '').split('zł')[0]
        except AttributeError:
            price = None
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
                # print(f"{details['Piętro']}")
                try:
                    if details[key].endswith('m²'):
                        details[key] = details[key].split(' ')[0].replace(',','.')
                    if details[key].endswith('zł'):
                        details[key] = details[key].replace(' ','').split('zł')[0]
                    if details[key] == 'zapytaj':
                        details[key] = None
                except AttributeError:
                    details[key] = None
                try:
                    if details['Piętro'].split('/')[0] == 'parter':
                        cut = details['Piętro'].split('/')
                        details['Piętro'] = f'1/{cut[1]}'
                        # print("Udało się")
                    elif details['Piętro'] == 'parter':
                        details['Piętro'] = f'1'
                except IndexError:
                    details['Piętro'] = None
                except AttributeError:
                    details['Piętro'] = None
                # if details[key].endswith('Film'):
                #     details[key] = None
        return details
    return wrapper


def show_offert(func):
    def wrapper(*args):
        nr = func(*args)
        try:
            offert_nr = nr.split(' ')[-1]
        except AttributeError:
            offert_nr = None
        return offert_nr
    return wrapper


def show_data(func):
    def wrapper(*args):
        unit = ['sekunda', 'sekundy', 'sekund', 'minutę', 'minuty', 'minut','minuta','godzina', 'godzin', 'godziny', 'dzień', 'dni', 'miesiąc',
                'miesiące', 'miesięcy', 'rok', 'lata' ]
        now = datetime.date.today()

        try:
            data_info = func(*args).split(' ')
            time_ago = int(data_info[-3])
            time_unit = data_info[-2]
        except TypeError and ValueError:
            return
        else:
            if time_ago == None or time_unit == None:
                return
            if time_unit == 'sekunda' or time_unit == 'sekundę' or time_unit == 'sekund' or time_unit == 'sekundy':
                return now - timedelta(seconds=int(time_ago))
            elif time_unit == 'minut' or time_unit == 'minuty' or time_unit == 'minutę':
                return now - timedelta(minutes=int(time_ago))
            elif time_unit == 'godzinę' or time_unit == 'godzin' or time_unit == 'godziny':
                return now - timedelta(hours=int(time_ago))
            elif time_unit == 'dni' or time_unit == 'dzień':
                return now - timedelta(days=int(time_ago))
            elif time_unit == 'miesiąc' or time_unit == 'miesiące' or time_unit == 'miesięcy':
                return now - relativedelta(months=int(time_ago))
            elif time_unit == 'rok' or time_unit == 'lata' or time_unit == 'lat':
                return now - relativedelta(years=int(time_ago))
            else:
                return
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
