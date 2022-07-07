import numpy as np
import pandas as pd
from connect_with_database import DatabaseConnect

con = DatabaseConnect('flats.db')
connection = con.connect_data()

df = pd.read_sql_query('Select * FROM property', connection)
print(df)

'''1.How many offers per a city'''
flats_per_city = df.groupby(['city'], as_index=False).agg({'id':pd.Series.count}).sort_values('id', ascending=False)

'''2. What is average per 1m2 in xity'''
price_per_1m2 = (df.price // df.area).apply(np.ceil)
df.insert(5,'price_per_1m2', price_per_1m2)

'''3. Average price per 1m2'''
city_average_price_per_1m = (df.groupby(['city']).agg({'price_per_1m2': pd.Series.mean})).round(0).sort_values(by='price_per_1m2', ascending=False)
city_average_price_per_1m.sort_values(by='price_per_1m2', ascending=False)
print(city_average_price_per_1m)
