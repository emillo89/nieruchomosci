from connect_with_database import DatabaseConnect
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import Optional, List


class ReadData:

    def __init__(self, databasename: str) -> None:
        self.con = DatabaseConnect(databasename)
        self.df = None

    def query_connection(self, tablename: str) -> None:
        connection = self.con.connect_data()
        self.df = pd.read_sql_query(f'Select * FROM {tablename}', connection)

    def convert_to_csv(self, file_name='flats') -> None:
        pd.DataFrame.to_csv(self.df, f'{file_name}.csv')

    def fillna(self, value: Optional, column: Optional) -> None:
        self.df[column].fillna(value, inplace=True)

    def price_per_m2(self) -> float:
        price = (self.df['price'] // self.df['area']).apply(np.ceil)
        return price

    def insert_column(self, index_place: int, name_new_column: str, new_column: str) -> None:
        self.df.insert(index_place, name_new_column, new_column)

    def convert_date(self, column: Optional, format: Optional, strformat: Optional) -> None:
        self.df[column] = (pd.to_datetime(self.df['date_addition_add'], format=format).dt.strftime(strformat))
