from class_dash import ReadData
import pandas as pd


class BarChart(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def take_year(self) -> int:
        year = pd.DatetimeIndex(self.df['date_addition_add']).year
        return year

    def take_month(self) -> int:
        month = pd.DatetimeIndex(self.df['date_addition_add']).month
        return month

    def show_bar_chart(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All'):
        offert_year = self.take_year()
        offert_month = self.take_month()
        self.df.insert(22, 'year', offert_year)
        self.df.insert(23, 'month', offert_month)

        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            offert = self.df.groupby(['date_addition_add', 'year', 'month'], as_index=False).\
                agg({'id': pd.Series.count}).sort_values(['year', 'month'])
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'city']).agg({'id': pd.Series.count}).\
                reset_index()
            offert = filtered_df[(filtered_df['city'] == w_city)].sort_values(['year', 'month'])
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'kind_of_investment']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['kind_of_investment'] == w_kind_of_investment)].sort_values(
                ['year', 'month'])
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'market']).\
                agg({'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['market'] == w_market)].sort_values(
                ['year', 'month'])
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'city', 'kind_of_investment']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)].\
                sort_values(['year', 'month'])
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'kind_of_investment', 'market']).agg(
                {'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['kind_of_investment'] == w_kind_of_investment) & (filtered_df['market'] == w_market)].\
                sort_values(['year', 'month'])
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'city', 'market']).\
                agg({'id': pd.Series.count}).reset_index()
            offert = filtered_df[(filtered_df['city'] == w_city) & (filtered_df['market'] == w_market)].sort_values(
                ['year', 'month'])
        else:
            filtered_df = self.df.groupby(['date_addition_add', 'year', 'month', 'city', 'kind_of_investment',
                                           'market']).agg({'id': pd.Series.count}).reset_index()
            offert = filtered_df[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment) & (
                            filtered_df['market'] == w_market)].sort_values(['year', 'month'])
        return offert
