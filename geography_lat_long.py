lat_and_long = {'Wrocław': {'lat': '51.107883', 'long': '17.038538'},
                'Warszawa': {'lat': '52.229675', 'long': '21.012230'},
                'Szczecin': {'lat': '53.428543', 'long': '14.552812'},
                'Gdańsk': {'lat': '54.352024', 'long': '18.646639'},
                'Lublin': {'lat': '51.246910', 'long': '22.573620'},
                'Poznań': {'lat': '52.406376', 'long': '16.925167'},
                'Kraków': {'lat': '50.064651', 'long': '19.944981'},
                'Łódź': {'lat': '51.759048', 'long': '19.458599'},
                'Białystok': {'lat': '53.132488', 'long': '23.168840'},
                'Bydgoszcz': {'lat': '53.121132', 'long': '17.992970'}}

city = 'Lublin'

if city in lat_and_long:
    lat = lat_and_long['Lublin']['lat']
    long = lat_and_long['Lublin']['long']
    print(lat)
    print(long)