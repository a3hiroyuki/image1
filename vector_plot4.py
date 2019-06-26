# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from math import *
import pandas as pd
import pyproj
import matplotlib.image as mpimg


class PlotPoint():

    COLOR = {1:"g", 2:"r"}

    def __init__(self, no, x, y, angle):
        self.no = no
        self.x = x
        self.y = y
        self.angle = angle
        self.vector = self.get_vector()

    def get_vector(self):
        angles_rad = self.angle * (pi / 180.0);
        ang_x = cos(angles_rad);
        ang_y = sin(angles_rad);
        return  [ang_x, ang_y]

    def get_color(self):
        return self.COLOR.get(self.no)

CUR_DIR = 'C:\\aaa\\'

df = pd.read_csv(CUR_DIR + 'ccc.csv', dtype = 'object')

no_arr = df['no'].values.astype('float')
x_arr = df['x'].values.astype('float')
y_arr = df['y'].values.astype('float')
angles = df['ang'].values.astype('float')

img = mpimg.imread(CUR_DIR  + 'yae.png')
h, w, c = img.shape

print (df)

pp_arr = []
for i in range(len(no_arr)):
    pp = PlotPoint(no_arr[i], x_arr[i], y_arr[i], angles[i])
    pp_arr.append(pp)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#範囲設定
ax.set_xlim(-20, 55)
ax.invert_xaxis()
ax.set_ylim(-5, 15)
ax.invert_yaxis()

for pp in pp_arr:
    ax.quiver(pp.x, pp.y, pp.vector[0], pp.vector[1],angles='xy',scale_units='xy',scale=1.0, color=pp.get_color())

xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.imshow(img, extent=[*xlim, *ylim], aspect='auto', alpha=1.0)

plt.show()