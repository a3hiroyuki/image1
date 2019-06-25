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
    pp = PlotPoint(no_arr[i], w * x_arr[i]/15, h * y_arr[i]/10, angles[i])
    pp_arr.append(pp)

plt.figure()
plt.imshow(img)

for pp in pp_arr:
    plt.quiver(pp.x, pp.y, pp.vector[0], pp.vector[1],angles='xy',scale_units='xy',scale=0.05, color=pp.get_color())


# グラフ表示
#plt.xlim([LEFT_BOTTOM[0],RIGHT_TOP[0]])
#plt.ylim([LEFT_BOTTOM[1] ,RIGHT_TOP[1]])

#ax.set_xticks(np.linspace(0, np.pi * 4, 5))
#ax.set_yticks(np.linspace(-1, 1, 3))

plt.draw()
plt.show()