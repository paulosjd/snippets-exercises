import csv
import sys
from math import radians, cos, sin, asin, sqrt


class AirportLocator:

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def haversine(self, lon, lat):
        """
        Calculate using the haversine formula the distance from GPS point supplied and that defined for the instance
        Args:
            lon (float): A float value representing an airports longitude
            lat (float): A float value representing an airports latitude
        Returns:
            A float value representing the distance in kilometres
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon, lat, self.longitude, self.latitude])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def get_nearest(self):
        airport_data = []
        with open('airports.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                airport_data.append({
                    'name': row['NAME'],
                    'icao': row['ICAO'],
                    'distance': self.haversine(float(row['Longitude']), float(row['Latitude']))
                })
        min_distance = (min([a.get('distance') for a in airport_data]))
        nearest = [(d.get('name'), d.get('icao')) for d in airport_data if d.get('distance') == min_distance]
        return 'Nearest airport: {} ({})'.format(*nearest[0])


def get_user_input():
    latitude, longitude = None, None
    while True:
        print('Enter latitude')
        lat_choice = input("> ")
        print('Enter longitude:')
        lon_choice = input("> ")
        try:
            longitude = float(lon_choice)
            latitude = float(lat_choice)
            break
        except ValueError:
            print('Please enter decimal values')
            continue
    return latitude, longitude


if __name__ == '__main__':
    user_input = None, None
    if len(sys.argv) > 1:
        try:
            user_input = float(sys.argv[1]), float(sys.argv[2])
        except (ValueError, IndexError):
            pass
    if not all(user_input):
        user_input = get_user_input()
    airport_locator = AirportLocator(*user_input)
    print(airport_locator.get_nearest())
