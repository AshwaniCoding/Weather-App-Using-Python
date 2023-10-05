#import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

# Function to get weather information frpm OpenWeatherMap API
def get_weather(city):
    API_key = "a80ba40509d60e525ab8eb451f30c530"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)


    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    # Parse the response JSON to get weather information 
    weather = res.json()
    # print("response,",weather)
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the URl and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and descriptions label
    temperature_label.config(text=f"Temperature : {temperature:.0f}°C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("500x600")

# Label widget -> to show the enter city name label
cityName_label = tk.Label(root, text="Enter City Name: ", bg='#fff', fg='#f00', pady=10, padx=10, font=("Helvetica", 18))
cityName_label.pack(pady=10)

# Entry widget -> to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=3)

# Button widget -> to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget -> to show the city
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label Widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

#Label widget -> to show the temperature
temperature_label = tk.Label(root,font='Helvetica, 20')
temperature_label.pack()

# Label widget -> to show the weather description
description_label = tk.Label(root ,font="Helvetica, 20")
description_label.pack()

root.mainloop()