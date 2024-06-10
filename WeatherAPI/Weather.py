import argparse
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
                response = requests.get(
                    self.API_URL.format(str(lat)[:9], str(lon)[:9], self.api_key)
                )
                responceJson = response.json()
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
    parser = argparse.ArgumentParser()

    parser.add_argument("--Demo", "--D", default="N", help="Path to input file")
    parser.add_argument("--LatStart", "--Lat1", help="Path to input file")
    parser.add_argument("--LatEnd", "--Lat2", help="Path to input file config")
    parser.add_argument("--LonStart", "--Lon1", help="OutPut table name")
    parser.add_argument("--TableInfo", "--Lon2", help="OutPut table information")
    parser.add_argument("--OutputDir", "--O", help="OutPut table information")
    parser.add_argument("--FileName", "--F", help="OutPut table information")
    parser.add_argument("--Number", "--N", help="OutPut table information")

    args = parser.parse_args()
    if args.Demo == "Y":
        weather = OpenWeatherAPI(
            [random, args.LatEnd],
            [args.LonStart, args.LonEnd],
            args.OutputDir,
            args.FileName,
        )
        weather.build_lat_lon_list(args.Number).make_weathercall()
    else:
        weather = OpenWeatherAPI(
            [args.LatStart, args.LatEnd],
            [args.LonStart, args.LonEnd],
            args.OutputDir,
            args.FileName,
        )
        weather.build_lat_lon_list(args.Number).make_weathercall()


if __name__ == "__main__":
    main()
