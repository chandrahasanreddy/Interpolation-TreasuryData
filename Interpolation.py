import sqlite3
import pandas as pd


conn = sqlite3.connect('treasury.db')
cur = conn.cursor()

#inserting data into db
df = pd.read_csv('treasury_rate.csv', parse_dates=['data'], dayfirst=True)
df.to_sql('treasury_data', conn, if_exists='append', index=False)

res=cur.execute("PRAGMA table_info(treasury_data)")
for row in res.fetchall():
    print(row)