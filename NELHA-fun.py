import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

# Define company colors
Symbrosia_colors = {
    'red': '#db0f40',
    'blue': '#66afb2',
    'yellow': '#ffb200'
}

# Define a function to fetch weather data from the NELHA website
def fetch_weather_data():
    url = "https://midcdmz.nrel.gov/apps/display.pl?site=NELHA;all=1"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', attrs={'border': '', 'cellpadding': '3'})
        if table:
            # Clear the tree, standard practice to clear the tree before inserting new data
            clear_treeview()
            # Initialize status message
            status_msg = ""
            # Iterate through rows of the table and extract data
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) == 3:
                    label = columns[0].text.strip()
                    value = columns[1].text.strip()
                    units = columns[2].text.strip()
                    # Insert data into the treeview
                    tree.insert('', 'end', values=(label, value, units))
                    # Check conditions and concatenate messages
                    if label == "Global UV" and float(value) < 750:
                        status_msg += "The Limu Kohu would love more sun!\n"
                    if label == "Global UV" and float(value) >= 750:
                        status_msg += "The Limu Kohu is loving the sun rays!\n"
                    if label == "Air Temperature" and float(value) > 28:
                        status_msg += "Thank you for air conditioning!\n"
                    if label == "Air Temperature" and float(value) < 20:
                        status_msg += "Are we still in Hawai'i?!\n"
                    if label == "Wind Speed" and float(value) > 18:
                        status_msg += "Don't let your work blow away out there!\n"
                    if label == "Wind Speed" and float(value) < 10:
                        status_msg += "It's a calm day at NELHA!\n"
            # Update status label with concatenated messages
            lbl_status.config(text=status_msg.strip(), fg=Symbrosia_colors['yellow'])
        else:
            lbl_status.config(text="What table are you talking about? Use the inspect element tool in your browser to find the table.")
    else:
        lbl_status.config(text="Noooooooo! The website is down! Try again later.")

def clear_treeview():
    # Clear existing data in the treeview
    for i in tree.get_children():
        tree.delete(i)

root = tk.Tk()
root.title("NELHA Weather Station Data")

# Set background color of the root window
root.configure(background=Symbrosia_colors['blue'])

# Create a style to customize the appearance of the treeview
style = ttk.Style(root)
style.configure("Treeview", background=Symbrosia_colors['blue'], fieldbackground=Symbrosia_colors['red'], foreground='white')
# Set font size for the treeview
style.configure("Treeview.Heading", font=('Helvetica', 14))
style.configure("Treeview", font=('Helvetica', 14))

# Create a treeview with columns for parameter, value, and units
tree = ttk.Treeview(root, columns=('Parameter', 'Value', 'Units'), show='headings')
tree.heading('Parameter', text='Parameter')
tree.heading('Value', text='Value')
tree.heading('Units', text='Units')
tree.pack()

# Add some feedback to the user
lbl_status = tk.Label(root, text="", fg=Symbrosia_colors['red'], font=('Helvetica', 14, 'bold'))
lbl_status.pack()

# Fetch data button
btn_fetch_data = tk.Button(root, text="Fetch Weather Data", command=fetch_weather_data, bg=Symbrosia_colors['yellow'], fg='black', activebackground=Symbrosia_colors['yellow'], activeforeground='black', font=('Helvetica', 14, 'bold'))
btn_fetch_data.pack()

root.mainloop()
