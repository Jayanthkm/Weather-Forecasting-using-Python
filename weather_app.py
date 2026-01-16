import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# ================= CONFIG =================
API_KEY = "YOUR_API_KEY_HERE"   # replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/"
# ==========================================

def get_current_weather():
    city = city_entry.get()
    if city == "":
        messagebox.showerror("Error", "Please enter city name")
        return

    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]

        output_text.delete("1.0", tk.END)
        output_text.insert(
            tk.END,
            f"City: {city}\n"
            f"Temperature: {temp} °C\n"
            f"Humidity: {humidity} %\n"
            f"Wind Speed: {wind} m/s\n"
            f"Condition: {desc}\n"
        )

    except:
        messagebox.showerror("Error", "Unable to fetch weather data")


def get_forecast():
    city = city_entry.get()
    if city == "":
        messagebox.showerror("Error", "Please enter city name")
        return

    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "200":
            messagebox.showerror("Error", "Forecast not available")
            return

        dates = []
        temps = []

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "5-Day Forecast:\n\n")

        # pick one data point per day (every 8th item)
        for i in range(0, 40, 8):
            item = data["list"][i]
            date = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]

            dates.append(date)
            temps.append(temp)

            output_text.insert(
                tk.END,
                f"{date} : {temp} °C , {desc}\n"
            )

        # Plot graph
        plt.figure()
        plt.plot(dates, temps, marker='o')
        plt.title(f"5-Day Temperature Forecast for {city}")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.show()

    except:
        messagebox.showerror("Error", "Unable to fetch forecast data")


# ================= GUI =================
root = tk.Tk()
root.title("Weather Forecasting App")
root.geometry("400x450")
root.resizable(False, False)

title = tk.Label(root, text="Weather Forecasting App", font=("Arial", 16, "bold"))
title.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=5)
city_entry.insert(0, "Enter city name")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

weather_btn = tk.Button(btn_frame, text="Get Weather", command=get_current_weather)
weather_btn.grid(row=0, column=0, padx=10)

forecast_btn = tk.Button(btn_frame, text="Get Forecast", command=get_forecast)
forecast_btn.grid(row=0, column=1, padx=10)

output_text = tk.Text(root, height=12, width=45)
output_text.pack(pady=10)

root.mainloop()
