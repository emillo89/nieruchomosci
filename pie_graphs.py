from class_dash import ReadData
import pandas as pd
from pandas import DataFrame


class PieChart(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def get_data_to_graph(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') \
            -> DataFrame:
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby('kind_of_investment').agg({'id': pd.Series.count}).reset_index()
            data = filtered_df
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['kind_of_investment', 'city']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['city'] == w_city)]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['city', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['kind_of_investment', 'city', 'market']).agg(
                {'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[
                (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
        else:
            filtered_df = self.df.groupby(['city', 'kind_of_investment', 'market'])[['id']].count().reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                        filtered_df['market'] == w_market)]
        return data


class PieChartTwo(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def get_data_to_graph(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') \
            -> DataFrame:
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby('market').agg({'id': pd.Series.count}).reset_index()
            data = filtered_df
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['market', 'city']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['city'] == w_city)]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['market', 'city', 'kind_of_investment']).agg(
                {'id': pd.Series.count}).reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market', 'city']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market', 'kind_of_investment']).agg({'id': pd.Series.count}).reset_index()
            data = filtered_df[
                (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
        else:
            filtered_df = self.df.groupby(['city', 'kind_of_investment', 'market'])[['id']].count().reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                            filtered_df['market'] == w_market)]
        return data
