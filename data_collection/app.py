import time
import requests
from pymongo import MongoClient

api_key = '079025fd2d352a88e95dc71b9a51efcc'
url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.64&lon=22.93&appid={api_key}"


def fetch_weather_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def main():
    client = MongoClient("mongodb://mongo:27017/")
    db = client["weather_database"]
    collection = db["weather_data"]

    while True:
        weather_data = fetch_weather_data(url)
        if weather_data:
            collection.insert_one(weather_data)
            print("Weather data inserted into MongoDB.")
        time.sleep(10)


if __name__ == "__main__":
    main()
