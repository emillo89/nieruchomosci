from connect_with_database import DatabaseConnect
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import Optional, List

class ReadData:
    def __init__(self, databasename: str) -> None:
        self.con = DatabaseConnect(databasename)
        self.df = None
    def query_connection(self) -> DataFrame:
        connection = self.con.connect_data()
        self.df = pd.read_sql_query('Select * FROM property', connection)
        return self.df

    def convert_to_csv(self, file_name='flats') -> None:
        pd.DataFrame.to_csv(self.df, f'{file_name}.csv')

    def count_totat_add(self) -> int:
        count_add = self.df.count()['id']
        return count_add

    def show_how_many_offert_per_kin_of_investments(self) -> DataFrame:
        offert_per_kind_of_investment = self.df.groupby(['kind_of_investment']).agg({'id': pd.Series.count})
        return offert_per_kind_of_investment

    def count_by_filtered_column(self, column: str, value: Optional) -> int:
        houses = self.df.loc[self.df[column] == value].count()['id']
        return houses

    def count_houses(self):
        houses = self.df.loc[self.df['kind_of_investment'] == 'Dom'].count()['id']
        return houses

    def count_flats(self):
        flats = self.df.loc[self.df['kind_of_investment'] == 'Mieszkanie'].count()['id']
        return flats

    def show_city_dropdown(self) -> List[str]:
        city = self.df['city'].unique()
        return city

    def show_kind_of_investment_dropdown(self) -> list:
        kind_of_investment = self.df['kind_of_investment'].unique()
        return kind_of_investment

    def show_market_dropdown(self):
        self.fillna('nieznany', 'market')
        market = self.df['market'].unique()
        return market

    def fillna(self, value, column):
        self.df[column].fillna(value, inplace=True)

    def price_per_m2(self) -> float:
        price = (self.df['price'] // self.df['area']).apply(np.ceil)
        return price

    def insert_column(self, index_place, name_new_column, new_column):
        self.df.insert(index_place, name_new_column, new_column)

    def kind_advertiser_add(self):
        kind_advertisement = self.df.groupby(['advertiser_add'], as_index=False).agg({'price_per_1m2':pd.Series.sum})['advertiser_add']
        return kind_advertisement

    def average_price_for_kind_advertisement(self):
        price = self.df.groupby(['advertiser_add'], as_index=False).agg({'price_per_1m2': pd.Series.sum})['price_per_1m2']
        count_add = self.df.groupby(['advertiser_add'], as_index=False).agg({'price_per_1m2':pd.Series.count})['price_per_1m2']
        average_price = round(price //count_add)
        return average_price


