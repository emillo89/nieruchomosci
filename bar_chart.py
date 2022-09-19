from class_dash import ReadData
import pandas as pd


class BarChart(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def show_bar_chart(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All'):
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            offert = self.df.groupby(['date_addition_add'], as_index=False).agg({'id': pd.Series.count}).sort_values(
                'date_addition_add')
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city']).agg({'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['city'] == w_city)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'kind_of_investment']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'market']).agg({'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'kind_of_investment']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'kind_of_investment', 'market']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'market']).agg({'id': pd.Series.count}).\
                reset_index()
            offert = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)]
        else:
            filtered_df = self.df.groupby(['date_addition_add', 'city', 'kind_of_investment', 'market']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                            filtered_df['market'] == w_market)]
        return offert
