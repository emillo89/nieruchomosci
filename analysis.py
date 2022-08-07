from connect_with_database import DatabaseConnect
import pandas as pd

con = DatabaseConnect('offert.db')
connection = con.connect_data()

df = pd.read_sql_query('SELECT * FROM property', connection)
# print(df.head(10))

pd.DataFrame.to_csv(df, 'offert.csv')