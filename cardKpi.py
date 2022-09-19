from class_dash import ReadData
import numpy as np
import pandas as pd
from pandas import DataFrame
from typing import Tuple


class CardKpi(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def count_totat_add(self) -> int:
        count_add = self.df.count()['id']
        return count_add

    def fill_in_the_data(self) -> None:
        price_per_1m2 = (self.df['price'] // self.df['area']).apply(np.ceil)
        self.df.insert(6, 'price_per_1m2', price_per_1m2)
        self.df['market'].fillna('nieznany', inplace=True)
        self.df['kind_of_investment'].fillna('nieznany', inplace=True)


class CardKpiTwo(CardKpi):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def filtered_df(self) -> DataFrame:
        groupby_data = self.df.groupby(['city']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
        return groupby_data

    def average_price(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') -> int:
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            average = self.df.agg({'price_per_1m2': pd.Series.mean})['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['city']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[filtered_df['city'] == w_city][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['kind_of_investment']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[filtered_df['kind_of_investment'] == w_kind_of_investment][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[filtered_df['market'] == w_market][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = self.df.groupby(['city', 'kind_of_investment']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            ind = filtered_df.index[
                (filtered_df['city'] == w_city) & (filtered_df['kind_of_investment'] == w_kind_of_investment)][0]
            average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[
                    (filtered_df['market'] == w_market) & (
                                filtered_df['kind_of_investment'] == w_kind_of_investment)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['city', 'market']).agg({'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[
                    (filtered_df['market'] == w_market) & (filtered_df['city'] == w_city)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = self.df.groupby(['city', 'kind_of_investment', 'market']).agg(
                {'price_per_1m2': pd.Series.mean}).reset_index()
            try:
                ind = filtered_df.index[(filtered_df['city'] == w_city) &
                                        (filtered_df['kind_of_investment'] == w_kind_of_investment) &
                                        (filtered_df['market'] == w_market)][0]
            except IndexError:
                average = 0
            else:
                average = filtered_df.iloc[ind]['price_per_1m2']

        return average


class CardKpiTree(CardKpi):
    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def __top_offert(self) -> DataFrame:
        top = self.df.sort_values('price_per_1m2')[
            ['id', 'kind_of_investment', 'city', 'market', 'area', 'price_per_1m2', 'price', 'link']]
        return top

    def top_two_offert(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') -> Tuple:
        top = self.__top_offert()
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            kind = [k for k in top.head(3)['kind_of_investment']]
            area = [k for k in top.head(3)['area']]
            link = [k for k in top.head(3)['link']]
            return kind, area, link

        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            filtered_df = top.loc[top['city'] == w_city]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = top.loc[top['kind_of_investment'] == w_kind_of_investment]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = top.loc[top['market'] == w_market]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            filtered_df = top.loc[(top['city'] == w_city) & (top['kind_of_investment'] == w_kind_of_investment)]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = top.loc[
                (top['market'] == w_market) & (top['kind_of_investment'] == w_kind_of_investment)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            filtered_df = top.loc[(top['city'] == w_city) & (top['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            filtered_df = top.loc[
                (top['city'] == w_city) & (top['kind_of_investment'] == w_kind_of_investment) & (
                            top['market'] == w_market)]

        try:
            kind = [k for k in filtered_df.head(3)['kind_of_investment']]
        except IndexError:
            kind = ['', '']
        try:
            area = [k for k in filtered_df.head(3)['area']]
        except IndexError:
            area = ['', '']
        try:
            link = [k for k in filtered_df.head(3)['link']]
        except IndexError:
            link = ['', '']

        return kind, area, link
