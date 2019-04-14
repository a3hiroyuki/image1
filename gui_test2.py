import math

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import pandas as pd
import time, threading


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

    def items(self):
        return [ (point.x, point.y) for point in self.points.values()]

    def add_point(self, x, y=0):
        if isinstance(x, MouseEvent):
            x, y = int(x.xdata), int(x.ydata)
        self.points[self.no] = PlotPoint(x, y, 0)
        self.no = self.no + 1

    def remove_point(self, point_no):
        self.points.pop(point_no)

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

class PlotPoint():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

class DraggablePlotExample(object):
    u""" An example of plot with draggable markers """

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

        self._update_plot()
        plt.show()


    def _on_click(self, event):
        # left click
        if event.button == 1 and event.inaxes in [self._axes]:
            point_no = self.plot_points.get_nearest_point(event)
            if point_no:
                self._dragging_point = point_no
                self.plot_points.remove_point(point_no)
            else:
                self.plot_points.add_point(event)
            self._update_plot()
        # right click
        elif event.button == 3 and event.inaxes in [self._axes]:
            point_no = self.plot_points.get_nearest_point(event)
            if point_no:
                self.plot_points.remove_point(point_no)
                self._update_plot()

    def _update_plot(self):
        xy = self.plot_points.items()
        x, y = map(list, zip(*xy))
        if not self._line:
            self._line, = self._axes.plot(x, y, "b", marker="o", markersize=10)
        else:
            self._line.set_data(x, y)
        self._figure.canvas.draw()

#     def _on_release(self, event):
#         u""" callback method for mouse release event
#
#         :type event: MouseEvent
#         """
#         if event.button == 1 and event.inaxes in [self._axes] and self._dragging_point:
#             self._add_point(event)
#             self._dragging_point = None
#             self._update_plot()
#
#     def _on_motion(self, event):
#         u""" callback method for mouse motion event
#
#         :type event: MouseEvent
#         """
#         if not self._dragging_point:
#             return
#         self._remove_point(*self._dragging_point)
#         self._dragging_point = self._add_point(event)
#         self._update_plot()


if __name__ == "__main__":
    plot = DraggablePlotExample()