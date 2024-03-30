import sqlite3
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


conn = sqlite3.connect('treasury.db')
cur = conn.cursor()

#inserting data into db
df = pd.read_csv('treasury_rate.csv', parse_dates=['data'], dayfirst=True)
df.to_sql('treasury_data', conn, if_exists='append', index=False)

res=cur.execute("PRAGMA table_info(treasury_data)")
for row in res.fetchall():
    print(row)

# Interpolating the 12-year rates with 10 & 20
x = np.array([10, 20])
y = np.stack((df['10_treasury_rate'], df['20_treasur_rate']), axis=-1)

interpolator = interp1d(x, y, axis=1, kind='linear')
df['12_treasury_rate'] = interpolator(12)

print("\n12-Year Treasury Rate:")
print(df['12_treasury_rate'].values)

#checking shcema if 12_treasury_rate exists and then inserting
cur.execute(f"PRAGMA table_info('treasury_data')")
existing_columns = cur.fetchall()
column_exists = any(column[1] == '12_treasury_rate' for column in existing_columns)

if not column_exists:
    cur.execute(f"ALTER TABLE 'treasury_data' ADD COLUMN '12_treasury_rate' 'REAL'")


df.to_sql('treasury_data', conn, if_exists='append', index=False)

res=cur.execute("PRAGMA table_info(treasury_data)")
for row in res.fetchall():
    print(row)
print(res)