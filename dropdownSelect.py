from class_dash import ReadData
import numpy as np
from typing import Optional, List
import pandas as pd


class SelectDropdown(ReadData):

    def __init__(self, databasename: str) -> None:
        super().__init__(databasename)

    def show_city_dropdown(self) -> List[str]:
        city = self.df['city'].unique()
        city = np.append(city, 'All')
        return city

    def show_kind_of_investment_dropdown(self) -> list:
        kind_of_investment = self.df['kind_of_investment'].unique()
        kind_of_investment = np.append(kind_of_investment, 'All')
        return kind_of_investment

    def show_market_dropdown(self) -> List:
        self.fillna('nieznany', 'market')
        market = self.df['market'].unique()
        market = np.append(market, 'All')
        return market

