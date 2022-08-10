from connect_with_database import DatabaseConnect
import pandas as pd


class ReadData:
    def __init__(self, databasename):
        self.con = DatabaseConnect(databasename)
        self.df = None

    def query_connection(self):
        connection = self.con.connect_data()
        self.df = pd.read_sql_query('Select * FROM property', connection)
        return self.df

    def convert_to_csv(self):
        csv_database = pd.DataFrame.to_csv(self.df, 'flats.csv')
        return csv_database

    def count_totat_add(self):
        count_add = self.df.count()['id']
        return count_add

    def show_how_many_offert_per_kin_of_investments(self):
        offert_per_kind_of_investment = self.df.groupby(['kind_of_investment']).agg({'id': pd.Series.count})
        return offert_per_kind_of_investment

    def count_houses(self):
        houses = self.df.loc[self.df['kind_of_investment'] == 'Dom'].count()['id']
        return houses

    def count_flats(self):
        flats = self.df.loc[self.df['kind_of_investment'] == 'Mieszkanie'].count()['id']
        return flats