import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: " , self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")

        self.setStyleSheet("""
                           
                           QLabel,QPushButton{
                           font-family:calibri;
                           }
                           QLabel#city_label{
                           font-size: 40px;
                           font-style:italic;
                           }
                           QLineEdit#city_input{
                           font-size:40px;
                           }
                           QPushButton#get_weather_button{
                           font-size:30px;
                           font-weight:bold;
                           }
                           QLabel#temp_label{
                           font-size:50px;
                           }
                           QLabel#emoji_label{
                           font-size:100px;
                           font-family:Segoe UI emoji;
                           }
                           QLabel#desc_label{
                           font-size:40px;}
                           """)
        
        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key = "Enter your api key"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['cod'] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check yor input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid Api Key")
                case 403:
                    self.display_error("Forbidden:\Access is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error: \nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")    

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
            pass

        except requests.exceptions.TooManyRedirects:
            self.display_error("To many Redirections:\nCheck the uURL")
            pass
         
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
            pass

    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size:30px;")  
        self.temp_label.setText(message)  
        self.emoji_label.clear()
        self.desc_label.clear()

        
        

    def display_weather(self,data):
       temperature_k = data["main"]["temp"]
       temperature_c = temperature_k - 273.15
       temperature_f = (temperature_k * 9/5) - 459.67

       weather_desc = data["weather"][0]["description"]
       weather_id = data["weather"][0]["id"]

       self.emoji_label.setText(self.get_weather_emoji(weather_id))
       self.temp_label.setText(f"{temperature_c:.0f}°C")
       self.desc_label.setText(f"{weather_desc}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_()) 


    # {'location': {'name': 'Miami', 'region': 'Florida', 'country': 'United States of America', 'lat': 25.7739, 'lon': -80.1939, 'tz_id': 'America/New_York', 'localtime_epoch': 1751529449, 'localtime': '2025-07-03 03:57'}, 'current': {'last_updated_epoch': 1751528700, 'last_updated': '2025-07-03 03:45', 'temp_c': 26.7, 'temp_f': 80.1, 'is_day': 0, 'condition': {'text': 'Partly cloudy', 'icon': '//cdn.weatherapi.com/weather/64x64/night/116.png', 'code': 1003}, 'wind_mph': 8.5, 'wind_kph': 13.7, 'wind_degree': 186, 'wind_dir': 'S', 'pressure_mb': 1016.0, 'pressure_in': 30.0, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 87, 'cloud': 75, 'feelslike_c': 30.7, 'feelslike_f': 87.2, 'windchill_c': 27.5, 'windchill_f': 81.5, 'heatindex_c': 32.3, 'heatindex_f': 90.2, 'dewpoint_c': 25.2, 'dewpoint_f': 77.4, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 0.0, 'gust_mph': 11.5, 'gust_kph': 18.5}}