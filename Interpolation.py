import sqlite3
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

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

#Function to calculate moving average
def calculate_moving_average(data, movingvalue):
    return data.rolling(window=movingvalue).mean()

# Create the main window
root = tk.Tk()
root.title("Treasury Rates with Moving Average")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP)

# GUI and plotting code start
fig, ax = plt.subplots()

df['data'] = pd.to_datetime(df['data'])
df.set_index('data', inplace=True)

ax.plot(df.index, df['10_treasury_rate'], label='10-Year Treasury Rate')
ax.plot(df.index, df['12_treasury_rate'], label='12-Year Treasury Rate')
ax.plot(df.index, df['20_treasur_rate'], label='20-Year Treasury Rate')

# x-axis labelling with year
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fig.autofmt_xdate()


ax.legend()

# Adding plot to tkinter main window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack( fill=tk.BOTH)

#user input
textbox = tk.Entry(input_frame)
textbox.pack(side=tk.LEFT, padx=(10, 0))

# Function to update the chart with mvoign values - only positive integer as specified
def update_chart():
    user_input = int(textbox.get())
    if user_input > 0:
        moving_average = calculate_moving_average(df['12_treasury_rate'], user_input)
        ax.plot(df.index, moving_average, label=f'{user_input}-Day Moving Average', linestyle=':')
        ax.legend()
        canvas.draw()
        textbox.delete(0, tk.END) 
    else:
        messagebox.showerror("Input Error", "Only positive integers are accepted.")
        textbox.delete(0, tk.END)

# click button
update_button = tk.Button(input_frame, text="Update Moving Average", command=update_chart)
update_button.pack(side=tk.RIGHT, padx=(0, 10))

root.mainloop()
