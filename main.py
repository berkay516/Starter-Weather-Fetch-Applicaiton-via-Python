import requests
from tkinter import Tk, Label, Entry, Button, mainloop, messagebox
from PIL import Image, ImageTk
import io
from collections import defaultdict

myapi = ""  #individual API should be entered

def but():
    try:
        eget = en.get()
        
        # current weather json info
        a = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={eget}&appid={myapi}&units=metric&lang=tr').json()
        snc.config(text=f'{a["name"]} için sıcaklık şu anda {a["main"]["temp"]} derece. Hava {a["weather"][0]["description"]}. Aşağıda 5 günlük/3 saatlik hava verisi mevcuttur')
        
        # icon fetching to corresponding weather event
        icon_url = f'http://openweathermap.org/img/wn/{a["weather"][0]["icon"]}@2x.png'
        response = requests.get(icon_url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((50, 50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        snc_image.config(image=photo, bg="#00c7ff")
        snc_image.image = photo
        snc_image.grid(row=5, column=0, columnspan=2)

        # another request to fetch 5 days weather info
        b = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={eget}&appid={myapi}&units=metric&lang=tr').json()
        
        # grouping
        daily_data = defaultdict(list)
        for forecast in b["list"]:
            date = forecast["dt_txt"].split(" ")[0]  
            daily_data[date].append(forecast)
        
      
        for widget in t.grid_slaves():
            if int(widget.grid_info()["row"]) > 5:
                widget.destroy()

        
        row = 6
        for date, forecasts in daily_data.items():
            
            day_label = Label(t, text=f"{date}")
            day_label.grid(row=row, column=0, sticky="w")
            row += 1
            
            
            for forecast in forecasts:
                time = forecast["dt_txt"].split(" ")[1]  
                temp = forecast["main"]["temp"]
                desc = forecast["weather"][0]["description"]
                icon = forecast["weather"][0]["icon"]
                
                
                forecast_text = f"{time}: {desc}, {temp}°C"
                forecast_label = Label(t, text=forecast_text)
                forecast_label.grid(row=row, column=0, sticky="w", padx=10)
                
                
                icon_url = f'http://openweathermap.org/img/wn/{icon}@2x.png'
                response = requests.get(icon_url)
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((20, 20), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                icon_label = Label(t)
                icon_label.config(image=photo)
                icon_label.image = photo  
                icon_label.grid(row=row, column=1, sticky="w")
                
                row += 1
        
    except KeyError:
        messagebox.showerror(title="Bulunamadı", message="İstenen veri bulunamadı")
        print(a)
    except requests.exceptions.RequestException:
        messagebox.showerror(title="Hata", message="Resim indirilemedi")
        snc_image.config(image='')
    except Exception as e:
        messagebox.showerror(title="Hata", message=str(e))
        snc_image.config(image='')


t = Tk()
t.title("Basit hava durumu uygulaması (Alfa)")
t.minsize(400, 600)

Label(t, text="il/ülke").grid(row=0, column=0)
en = Entry(t)
en.grid(row=1, column=0)
Button(t, text="bul", command=but, height=1, width=20).grid(row=2, column=0)
Button(t, command=t.destroy, text="bitir").grid(row=3, column=0)
snc = Label(t)
snc.grid(row=4, column=0, columnspan=2)
snc_image = Label(t)
snc_image.grid(row=5, column=0, columnspan=2)

mainloop()
