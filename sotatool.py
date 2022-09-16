#!/usr/bin/env python
import argparse
from operator import ge
from sqlite3 import paramstyle
import geojson
import csv

class sotaSummit:
    def __init__(self):
        pass

    def parse_list_from_csv(self, data):
        self.code = data[0]
        self.associatoin_name = data[1]
        self.region_name = data[2]
        self.name = data[3]
        self.altitude_in_meters = int(data[4])
        self.altitude_in_feet = int(data[5])
        self.longitude = float(data[8])
        self.latitude = float(data[9])
        self.points = int(data[10])
        self.valid_from = data[12] # TODO: make datetype
        self.valid_to = data[13] # TODO: make datetype
        self.activation_count = int(data[14])
        self.geojson_point = geojson.Point((self.longitude, self.latitude))
        self.sotlas_url = self.build_sotlas_url()

    def build_sotlas_url(self):
         split_data = self.code.split('/')
         url = f'https://sotl.as/summits/{split_data[0]}/{split_data[1]}'
         return url

    def togeojson(self):
        notes_data = f'{self.sotlas_url}\npoints {self.points}\nactivation count: {self.activation_count}'
        summit = geojson.Feature(geometry=self.geojson_point,
                                 id=self.code,
                                 properties={'AltM': self.altitude_in_meters,
                                             'AltFt': self.altitude_in_feet,
                                             'elevation': self.altitude_in_meters,
                                             'summit_code': self.code,
                                             'points': self.points,
                                             'name': f'{self.name} {self.code}',
                                             'notes': notes_data
                                            })
        return(summit)

def parse_sota_csv(infile):
    summits = []
    with open(infile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            summit = sotaSummit()
            summit.parse_list_from_csv(row)
            summits.append(summit.togeojson())
    features = geojson.FeatureCollection(summits)
    print(geojson.dumps(features))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help='csvfile from summits on the air')
    args = parser.parse_args()
    parse_sota_csv(args.csvfile)