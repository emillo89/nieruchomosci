from class_dash import ReadData
import pandas as pd
from pandas import DataFrame


class LineChart(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def show_line_chart(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') -> \
            DataFrame:
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            data = self.df.groupby(['date_addition_add'], as_index=False).agg({'price_per_1m2': pd.Series.mean})
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'kind_of_investment']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city']).agg({'price_per_1m2': pd.Series.mean}).\
                reset_index()
            data = filtered_df[(filtered_df['city'] == w_city)]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[(filtered_df['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'kind_of_investment']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[
                (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
        else:
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            data = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                        filtered_df['market'] == w_market)]
        return data
