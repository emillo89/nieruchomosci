import sqlite3


class DatabaseConnect:

    def __init__(self, data: str):
        self.data = data

    def connect_data(self):
        connect = sqlite3.connect(self.data)
        return connect





