import pyproj
import numpy as np
from bokeh.core.enums import LatLon

#平面直角座標系への変換
def latlon2Coord(lat, lon):
    EPSG4612 = pyproj.Proj("+init=EPSG:4612")
    EPSG2451 = pyproj.Proj("+init=EPSG:2451")
    y, x = pyproj.transform(EPSG4612, EPSG2451, lon, lat)
    return (x, y)

def create_conv_matrix():

    lat_lon_arr= [
              (35.679588, 139.771114),
              (35.679750, 139.770723),
              (35.679456, 139.771048)
              ]

    x_y_arr = np.array([[0, 0, 1], [39.14, 0, 1], [0, 13.61, 1]])
    #x_y_arr = np.array([[0, 0, 1], [0, 39.14, 1], [13.61,0, 1]])

    lat_lon_conv_arr = np.empty((0,3), int)
    for (lat,lon) in lat_lon_arr:
        x, y= latlon2Coord(lat, lon)
        a =  np.array([[x, y, 1]])
        lat_lon_conv_arr = np.append(lat_lon_conv_arr, a, axis = 0)

    conv_matrix = np.dot(x_y_arr.T, np.linalg.inv(lat_lon_conv_arr.T))
    return conv_matrix

def get_coord(lat, lon):
    conv_matrix = create_conv_matrix()
    x, y= latlon2Coord(lat, lon)
    a =  np.array([[x, y, 1]])
    b = np.dot(conv_matrix, a.T)
    return b[0][0], b[1][0]

print("aa")
x, y = get_coord(35.679869, 139.770574)
print (x)
print (y)
x, y = get_coord(35.679670, 139.770456)
print (x)
print (y)
x, y = get_coord(35.679560, 139.771341)
print (x)
print (y)
x, y = get_coord(35.679376, 139.771250)
print (x)
print (y)