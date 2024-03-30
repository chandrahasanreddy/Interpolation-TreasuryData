Interpolation task- Northwestern Mutual

Task:

The attached CSV file has time series of 10-year and 20-year treasury rates.

Please write a script having the following features:

Create an SQLite database

Upload the 10-year and 20-year treasury rates to the SQLite database

Calculate the 12-year treasury rates using linear interpolation and upload them to the same table

Create a simple GUI with a text box, a button, and a line chart.

        (1.) When the GUI is started, the line chart shows the time series of 10-year, 12-year (Calculated in Step 3.) and 20-year treasury rate

        (2.) The text box is designed to accept a positive integer. After a user inputs a positive integer X and clicks the button, the script should calculate the X-day moving average of the interpolated 12-year treasury rate and add it to the chart
1.SQLite Database and Table Creation: An SQLite database was created, and a table named treasury_data was created by directly importing data from a CSV file utilizing the to_sql method in Pandas. This method facilitated handling column names that commence with numerals character which SQLite typically restricts. Instead of the conventional approach of manually defining the table schema and then populating the data (which would necessitate altering the column names or encapsulating them as strings to accommodate the numeric initiation- In the beginnign I used this method and then utilised to_sql), the to_sql method was employed for its efficiency and automation capabilities.

2.Schema Validation: Ensuring the robustness of the implementation, a schema validation step was incorporated. By invoking the PRAGMA table_info(treasury_data) command, the integrity and correctness of the table's schema were verified, particularly focusing on the column names encapsulated as strings, a modification instigated by Python to adhere to SQLite's naming constraints.

3.Interpolation and Dynamic Schema Adaptation: Task 3 necessitated the computation of the 12-year treasury rates, which were to be stored in a newly introduced column, 12_treasury_data. To avoid potential errors associated with repeated script executions—such as the duplication of columns—a preemptive check was implemented. This check ascertains the non-existence of the 12_treasury_data column before its addition to the table. For the interpolation process, the interp1d function from the scipy library was employed. The necessary parameters for this function were meticulously preprocessed to ensure precision in the interpolation results, thereby facilitating the accurate computation and storage of the 12-year treasury rates within the database.

Sample calculation : x = np.array([10, 20]) y = np.array([[6.68, 6.72], [6.42, 6.46], [6.03, 6.2 ], [6.23, 6.31], [6.29, 6.42]])

               Sample calculation:

               (x0, y0) = (10, 6.68)
               (x1, y1) = (20, 6.72)
               m= (6.72−6.68)/(20−10) = 0.04
​y=6.68+0.004×(12−10) y = 6.68 + 0.004 *(12-10) = 6.688

GUI Implementation :

Tkinter Window and Input Frame: A main window is created using tk.Tk(), which serves as the primary interface for the user. An input frame is established using tk.Frame(root) and is at the top of the main window. This frame contains text input and button.

Plotting Treasury Rates:

A Matplotlib figure (fig) and axes (ax) are instantiated for plotting the data. The data column in the DataFrame df is converted to datetime format and set as the index, ensuring time-series data is correctly aligned for plotting.Three time-series lines representing 10-year, 12-year, and 20-year treasury rates are plotted on the axes with labels . The x-axis is configured to display Year with 1 year difference. Embedding the Plot in Tkinter: The Matplotlib figure is embedded within the Tkinter window using FigureCanvasTkAgg, allowing the plot to be displayed as part of the GUI. User Interaction for Moving Average:

A text entry box (textbox) is provided within the input_frame for user input A button (update_button) is created and when clicked, it triggers the update_chart function. The update_chart function reads the input, validates it as a positive integer, calculates the moving average of the 12-year treasury rate over the specified number, and plots this new moving average series on the graph. After updating the chart, the text box content is cleared, and ready to accept the next input.

