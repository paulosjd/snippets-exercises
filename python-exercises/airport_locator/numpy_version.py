import csv
import sys

import numpy as np


def haversine_np(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6367 * c


with open('airports.csv') as csvfile:
    csv_data = list(csv.reader(csvfile))

airports = [a[:2] for a in csv_data[1:]]
coordinates = np.array([a[2:] for a in csv_data[1:]], dtype=np.float)
vfunc = np.vectorize(haversine_np)


def find_nearest(lon2=0.2716, lat2=50.8342):
    distances = vfunc(coordinates[:,1], coordinates[:,0], lon2, lat2)
    min_index = distances.argmin()
    return airports[min_index]


print(find_nearest())
