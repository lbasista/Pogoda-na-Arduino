import requests
import serial
import time

#Tłumaczenie stanów pogody z angielskiego
tlumacz = {
    'Sunny': 'Slonecznie',
    'Clear': 'Bezchmurne niebo',
    'Partly cloudy': 'M. zachmurzenie',
    'Cloudy': 'Zachmurzenie',
    'Overcast': 'Pochmurnie',
    'Mist': 'Mgla',
    'Patchy rain nearby': 'Miejscowe opady',
    'Patchy snow nearby': 'M. opady sniegu',
    'Patchy sleet nearby': 'M. opady sniegu',
    'Patchy freezing drizzle nearby': 'Miejscowa mzawka',
    'Thundery outbreaks in nearby' : 'Gwaltowna burza',
    'Blowing snow' : 'Wiatr i snieg',
    'Blizzard' : 'Sniezyca',
    'Fog' : 'Mgla',
    'Freezing fog' : 'Mrozna mgla',
    'Patchy light drizzle' : 'Lekka mzawka',
    'Light drizzle' : 'Lekka mzawka',
    'Freezing drizzle' : 'Mrozna mzawka',
    'Heavy freezing drizzle' : 'C. mrozna mzawka',
    'Patchy light rain' : 'Miejscowe opady',
    'Light rain' : 'Lekki deszcz',
    'Moderate rain at times' : 'Srednie opady',
    'Moderate rain' : 'Srednie opady',
    'Heavy rain at times' : 'Duze opady',
    'Heavy rain' : 'Duze opady',
    'Light freezing rain' : 'L. mrozny deszcz',
    'Moderate or heavy freezing rain' : 'Mrozny deszcz',
    'Light sleet' : 'Snieg z deszczem',
    'Moderate or heavy sleet' : 'Snieg z deszczem',
    'Patchy light snow' : 'M. lekki snieg',
    'Light snow' : 'Lekki snieg',
    'Patchy moderate snow' : 'M. opady sniegu',
    'Moderate snow' : 'Opady sniegu',
    'Patchy heavy snow' : 'M. mocny snieg',
    'Heavy snow' : 'M. opady sniegu',
    'Ice pellets' : 'Mokry snieg',
    'Light rain shower' : 'Przelotny deszcz',
    'Moderate or heavy rain shower' : 'Przelotna ulewa',
    'Torrential rain shower' : 'P. nawalnica',
    'Light sleet showers' : 'P.deszcz i snieg',
    'Moderate or heavy sleet showers' : 'P.deszcz i snieg',
    'Light snow showers' : 'L. opady sniegu',
    'Moderate or heavy snow showers' : 'S. opady sniegu',
    'Light showers of ice pellets' : 'L. mokry snieg',
    'Patchy light rain in area with thunder' : 'S. mokry snieg',
    'Moderate or heavy rain in area with thunder' : 'Mala burza',
    'Patchy light snow in area with thunder' : 'M. burza i snieg',
    'Moderate or heavy snow in area with thunder' : 'D. burza i snieg'
}

api_key = "" #Wprowadź swoje API
city = "" #Wprowadź ID swojego miasta
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no&alerts=no"

try:
    ser = serial.Serial('COM6', 9600) #Ustaw port COM dla Arduino
    print("Port szeregowy otwarty")
    time.sleep(2)
except Exception as e:
    print(f"Nie można otworzyć portu szeregowego: {e}")

while True:
    try:
        print("Pobieranie danych pogodowych...")
        pogoda = (requests.get(url)).json()
        
        if pogoda.get('current'):

            #Temperatura
            temp = pogoda['current']['temp_c']
            temp_jutro = pogoda['forecast']['forecastday'][0]['day']['avgtemp_c']
            #Miejsca po przecinku
            temp = round(temp, 1)
            temp_jutro = round(temp_jutro, 1)

            #Opis
            opis = pogoda['current']['condition']['text']
            opis_jutro = pogoda['forecast']['forecastday'][0]['day']['condition']['text']
            #Tłumaczenie z ANG na PL
            opis = tlumacz.get(opis, opis)
            opis_jutro = tlumacz.get(opis_jutro, opis_jutro)

            data_to_send = f"{temp} {opis}\n{temp_jutro} {opis_jutro};"
            print(f"Dane do wysłania: {data_to_send}")
            
            #Wyślij dane do Arduino
            ser.write(data_to_send.encode())

        time.sleep(600) #Odświeżanie co 10min
    
    except Exception as e:
        print(f"Błąd: {e}")
        time.sleep(60) #Jeśli błąd odczekaj 1min