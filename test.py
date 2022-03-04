import pandas as pd
import sqlite3

conn = sqlite3.connect('data/test.db')

conn.execute("""CREATE TABLE IF NOT EXISTS voters (
                adnumber INTEGER NOT NULL,
                name TEXT NOT NULL,
                STD TEXT NOT NULL,
                House TEXT NOT NULL,
                Voted INTEGER NOT NULL
                );""")

df = pd.read_excel('adbawkjhbd', engine='openpyxl')
df['Voted'] = 0
df.to_sql('voters', con=conn, if_exists='append', index=False)
print(df.head())