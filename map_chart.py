from class_dash import ReadData
import pandas as pd
from pandas import DataFrame
from typing import Dict


class MapChart(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def show_map(self, w_city: str = 'All', w_kind_of_investment: str = 'All', w_market: str = 'All') -> DataFrame:
        if w_city == 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            geography = self.df.groupby(['city', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            geograp = self.df.groupby(['city', 'kind_of_investment', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[geograp['kind_of_investment'] == w_kind_of_investment]
        elif w_city == 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            geograp = self.df.groupby(['city', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[geograp['market'] == w_market]
        elif w_city == 'All' and w_kind_of_investment != 'All' and w_market != 'All':
            geograp = self.df.groupby(['city', 'kind_of_investment', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[
                (geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['market'] == w_market)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market == 'All':
            geograp = self.df.groupby(['city', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['city'] == w_city)]
        elif w_city != 'All' and w_kind_of_investment == 'All' and w_market != 'All':
            geograp = self.df.groupby(['city', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[(geograp['market'] == w_market) & (geograp['city'] == w_city)]
        elif w_city != 'All' and w_kind_of_investment != 'All' and w_market == 'All':
            geograp = self.df.groupby(['city', 'kind_of_investment', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[
                (geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['city'] == w_city)]
        else:
            geograp = self.df.groupby(['city', 'kind_of_investment', 'market', 'lat', 'long'])[['id']].agg(
                {'id': pd.Series.count}).reset_index()
            geography = geograp.loc[
                (geograp['kind_of_investment'] == w_kind_of_investment) & (geograp['city'] == w_city) & (
                            geograp['market'] == w_market)]
        return geography

    def add_column_lat_long(self, geography_lat_long: Dict) -> None:
        cities = self.df['city'].unique()

        for city in cities:
            if city in geography_lat_long:
                self.df.loc[self.df['city'] == city, 'lat'] = geography_lat_long[city]['lat']
                self.df.loc[self.df['city'] == city, 'long'] = geography_lat_long[city]['long']
