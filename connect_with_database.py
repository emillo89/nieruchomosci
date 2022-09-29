import sqlite3
from typing import Optional


class DatabaseConnect:

    def __init__(self, data: str) -> None:
        self.data = data

    def connect_data(self) -> Optional:
        connect = sqlite3.connect(self.data)
        return connect
