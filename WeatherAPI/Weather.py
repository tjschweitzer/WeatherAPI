import os

import requests
from random import random

# Free account limited to 60 call
# ps per min
CALLS_PER_MINUTE = 60

# Open weather API KEY
API_KEY = "1144e9d02499289598995ccf71c564ef"


class OpenWeatherAPI:
    lonList = None
    latList = None

    header_List = (
        "lat",
        "lon",
        "temp",
        "pressure",
        "humidity",
        "uvi",
        "wind_speed",
        "wind_deg",
        "wind_gust",
    )
    API_URL = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}"

    def __init__(self, lat_range, lon_range, output_dir, table_name, api_key=API_KEY):
        self.lat_range = lat_range
        self.lon_range = lon_range
        self.output_dir = output_dir
        self.api_key = api_key
        self.table_name = table_name
        self.verify_output_dir()

    def build_lat_lon_list(self, n):
        delta_latitude = self.lat_range[1] - self.lat_range[0]
        delta_longitude = self.lon_range[1] - self.lon_range[0]
        self.latList = [random() * delta_latitude + self.lat_range[0] for x in range(n)]
        self.lonList = [
            random() * delta_longitude + self.lon_range[0] for x in range(n)
        ]
        return self

    def verify_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return self

    def make_weathercall(self):
        with open(
            os.path.join(self.output_dir, self.table_name + ".tjs"), "w"
        ) as the_file:

            for lat, lon in zip(self.latList, self.lonList):
                responce = requests.get(
                    self.API_URL.format(str(lat)[:9], str(lon)[:9], self.api_key)
                )
                responceJson = responce.json()
                line = self.string_format(responceJson)

                the_file.write(line + "\n")

    def string_format(self, json):
        return_string = "{:12s} {:12s} {:12s} {:12s} {:12s} {:12s}".format(
            str(json["coord"]["lat"]),
            str(json["coord"]["lon"]),
            str(json["main"]["temp"]),
            str(json["main"]["humidity"]),
            str(json["wind"]["deg"]),
            str(json["wind"]["speed"]),
        )
        return return_string


def main():
    weather = OpenWeatherAPI([40, 44], [32, 36], "TestData", "testOne")
    weather.build_lat_lon_list(100).make_weathercall()


if __name__ == "__main__":
    main()
