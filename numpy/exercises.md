
Exercises
---------

Create a vector with values ranging from 10 to 99

    >>> np.arange(10, 100)

Create a 3x3 matrix with even values from 0 to 16

    >>> a = np.arange(0, 17, 2)
    >>> np.reshape(a, (3, 3))

    >>> np.arange(0, 17, 2).reshape(3, 3)

Create a 10x10 array with random values and find the minimum value

    >>> np.random.random((10, 10)).min()

Create a 2d array with 1 on the border and 0 inside

    >>> ary = np.ones((10, 10))
    >>> ary[1:-1, 1:-1] = 0

Declare a 10x10x10 array with random values

    >>> ary = np.random.random((10, 10, 10))

Create a 3x3x3 array of random values and multiply with 3d array of same dimensions containing values incrementing by 1

    >>> a = np.arange(0,27)
    >>> b = np.reshape(a, (3,3,3))
    >>> np.random.random((3,3,3)) * b


Create a 3 x 4 array filled with all zeros, and a 6 x 4 array filled with all 1s.
Concatenate both arrays vertically into a 9 x 4 array, with the ones array on top and print out first_column.

    >>> a = np.zeros((3,4))
    >>> b = np.ones((6,4))
    >>> np.vstack((b,a))[:,0]
    array([ 1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.])

**Script to calculate the nearest location to current geographical coordinates from csv file of locations, location code, latitudes, longitudes**

    import csv
    import sys

    import numpy as np

     def haversine_np(lon1, lat1, lon2=0.2716, lat2=50.8342):
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        return 6367 * c

    vfunc = np.vectorize(haversine_np)

    with open('airports.csv') as csvfile:
        csv_data = list(csv.reader(csvfile))

    airports = [a[:2] for a in csv_data[1:]]
    latitudes = np.array([a[2] for a in csv_data[1:]], dtype=np.float64)
    longitudes = np.array([a[3] for a in csv_data[1:]], dtype=np.float64)

    distances = vfunc(longitudes, latitudes)
    min_index = distances.argmin()

    print(airports[min_index])
