import math

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter
from matplotlib.widgets import Slider, Button, RadioButtons

CUR_DIR = 'C:\\aaa\\'

class PlotPoints():
    def __init__(self):
        self.no = 1000
        self.points = {}
        df = pd.read_csv(CUR_DIR + 'bbb.csv', dtype = 'object')
        no_arr = df['no'].values.astype('float')
        x_arr = df['x'].values.astype('float')
        y_arr = df['y'].values.astype('float')
        angles = df['angle'].values.astype('float')
        for i in range(len(no_arr)):
            self.points[int(no_arr[i])] = PlotPoint(x_arr[i], y_arr[i], angles[i])
        self.check_in_circle()

    def add_point(self, x, y=0):
        if isinstance(x, MouseEvent):
            x, y = int(x.xdata), int(x.ydata)
        self.points[self.no] = PlotPoint(x, y, 0)
        self.no = self.no + 1

    def remove_point(self, point_no):
        #self.points.pop(point_no)
        self.points[point_no].is_del = True

    def get_nearest_point(self, event):
        distance_threshold = 3.0
        nearest_point_no = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for no, point in self.points.items():
            distance = math.hypot(event.xdata - point.x, event.ydata - point.y)
            if distance < min_distance:
                min_distance = distance
                nearest_point_no = no
        if min_distance < distance_threshold:
            return nearest_point_no
        return None

    def check_in_circle(self):
        radius = 10
        r2 = radius * radius
        for point1 in self.points.values():
            for point2 in self.points.values():
                if (not point1 == point2) and (not point1.is_del) and (not point2.is_del):
                    point_val = (point2.x - point1.x) * (point2.x - point1.x) + (point2.y - point1.y) * (point2.y - point1.y)
                    if point_val <= r2:
                        point2.is_del = True


class PlotPoint():

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.is_del = False

class DraggablePlot(object):

    def __init__(self):
        self._figure, self._axes, self._line = None, None, None
        self._dragging_point = None
        self.plot_points = PlotPoints()
        self._init_plot()

    def _init_plot(self):
        self._figure = plt.figure("Example plot")
        axes = plt.subplot(1, 1, 1)
        axes.set_xlim(0, 100)
        axes.set_ylim(0, 100)
        axes.grid(which="both")
        self._axes = axes
        self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        #self._figure.canvas.mpl_connect('button_release_event', self._on_release)
        #self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'delete')
        #bnext.on_clicked(on_button_clicked)
        #self._figure.canvas.mpl_connect('button_press_event', on_press)
        self.update_plot()
        plt.show()

    def update_plot(self):
        for point in self.plot_points.points.values():
            if point.is_del:
                self._axes.scatter(point.x,point.y, c='red')
            else:
                self._axes.scatter(point.x,point.y, c='blue')
        self._figure.canvas.draw()



    def _on_click(self, event):
        # left click
        if event.button == 1 and event.inaxes in [self._axes]:
            point_no = self.plot_points.get_nearest_point(event)
            if point_no:
                self._dragging_point = point_no
                self.plot_points.remove_point(point_no)
            else:
                self.plot_points.add_point(event)
            self.update_plot()
        # right click
        elif event.button == 3 and event.inaxes in [self._axes]:
            point_no = self.plot_points.get_nearest_point(event)
            if point_no:
                self.plot_points.remove_point(point_no)
                self.update_plot()

if __name__ == "__main__":
    plot = DraggablePlot()


