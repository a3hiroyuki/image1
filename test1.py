from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import math

class CreatePlot:
    lim = 10
    def __init__(self, A, O, B):
        fig = plt.figure()
        self.ax = fig.gca(projection='3d')
        self.ax.set_xlim(-self.lim, self.lim)
        self.ax.set_ylim(-self.lim, self.lim)
        self.ax.set_zlim(-self.lim, self.lim)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        e1_O = np.array([1, 0, 0])
        e2_O = np.array([0, 1, 0])
        e3_O = np.array([0, 0, 1])
        et1_O = np.dot(A, e1_O)
        et2_O = np.dot(A, e2_O)
        et3_O = np.dot(A, e3_O)
        #原点の描画
        self.arrow(e1_O, O, "k")
        self.arrow(e2_O, O, "k")
        self.arrow(e3_O, O, "k")
        #座標の描画
        self.arrow(et1_O, B, "k")
        self.arrow(et2_O, B, "k")
        self.arrow(et3_O, B, "k")

    def arrow(self, v, sp, c):
        # 空間座標基準で矢印をプロットする
        # v:ベクトル、sp:始点、c:色
        l = np.sqrt(v[0]**2+v[1]**2+v[2]**2)
        v_norm = v / np.linalg.norm(v)
        # ax.quiver(v[0]+sp[0], v[1]+sp[1], v[2]+sp[2],
        #           v[0], v[1], v[2],
        #           pivot='middle',
        #           #length=np.linalg.norm(v),
        #           length = l,
        #           color=c, linewidth=1)
        # Make the direction data for the arrows
        self.ax.quiver(sp[0], sp[1], sp[2],
                  v_norm[0], v_norm[1], v_norm[2],
                  #pivot='middle',
                  # length=np.linalg.norm(v),
                  length=l,
                  color=c,
                  linewidth=1)

class Transformation:

    def __init__(self):
        a = open('aaa.json')
        b = json.load(a)
        print (b)
        bx, by, bz = b["trans"][0], b["trans"][1], b["trans"][2]
        cx, cy, cz = 0, 0, 0
        rx, ry, rz = b["rot"][0], b["rot"][1], b["rot"][2]
        sx, sy, sz = b["scale"][0], b["scale"][1], b["scale"][2]
        self.scale = np.array([sx, sy, sz])
        # T
        self.B = np.array([bx, by, bz])
        self.O = np.array([cx, cy, cz])
        self.rOB = self.B - self.O
        # R
        # rx = np.pi
        #         # ry = np.pi / 2
        #         # rz = np.pi / 3
        rx = math.radians(rx)
        ry = math.radians(ry)
        rz = math.radians(rz)
        p = np.array([rx, ry, rz])
        R = self.rotM(p)
        self.A = R.T

    def rotM(self, p):
        # 回転行列を計算する
        px = p[0]
        py = p[1]
        pz = p[2]

        # 物体座標系の 1->2->3 軸で回転させる
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(px), np.sin(px)],
                       [0, -np.sin(px), np.cos(px)]])
        Ry = np.array([[np.cos(py), 0, -np.sin(py)],
                       [0, 1, 0],
                       [np.sin(py), 0, np.cos(py)]])
        Rz = np.array([[np.cos(pz), np.sin(pz), 0],
                       [-np.sin(pz), np.cos(pz), 0],
                       [0, 0, 1]])
        R = Rz.dot(Ry).dot(Rx)

        # 物体座標系の 3->2->1 軸で回転させる
        # Rx = np.array([[1, 0, 0],
        #                [0, np.cos(px), np.sin(px)],
        #                [0, -np.sin(px), np.cos(px)]])
        # Ry = np.array([[np.cos(py), 0, -np.sin(py)],
        #                [0, 1, 0],
        #                [np.sin(py), 0, np.cos(py)]])
        # Rz = np.array([[np.cos(pz), np.sin(pz), 0],
        #                [-np.sin(pz), np.cos(pz), 0],
        #                [0, 0, 1]])
        # R = Rx.dot(Ry).dot(Rz)

        # 空間座標系の 1->2->3 軸で回転させる
        # Rx = np.array([[1, 0, 0],
        #                [0, np.cos(px), -np.sin(px)],
        #                [0, np.sin(px), np.cos(px)]])
        # Ry = np.array([[np.cos(py), 0, -np.sin(py)],
        #                [0, 1, 0],
        #                [np.sin(py), 0, np.cos(py)]])
        # Rz = np.array([[np.cos(pz), np.sin(pz), 0],
        #                [-np.sin(pz), np.cos(pz), 0],
        #                [0, 0, 1]])
        # R = Rx.dot(Ry).dot(Rz)

        # 空間座標系の 3->2->1 軸で回転させる
        # Rx = np.array([[1, 0, 0],
        #                [0, np.cos(px), -np.sin(px)],
        #                [0, np.sin(px), np.cos(px)]])
        # Ry = np.array([[np.cos(py), 0, -np.sin(py)],
        #                [0, 1, 0],
        #                [np.sin(py), 0, np.cos(py)]])
        # Rz = np.array([[np.cos(pz), np.sin(pz), 0],
        #                [-np.sin(pz), np.cos(pz), 0],
        #                [0, 0, 1]])
        # R = Rz.dot(Ry).dot(Rx)
        return R

    def conv1(self, sBP, rot):
        print (sBP)
        temp1 = self.scale * sBP.T
        temp2 = np.dot(self.A , temp1)
        print (temp2)
        return self.rOB + np.dot(self.A , temp2)

    def conv2(self, sBP):
        return np.dot(self.A , sBP)

class Points:

    def __init__(self):
        df = pd.read_csv('bbb.csv')
        df = df[df['type']  == 'tracking']
        print (df)
        self.x_arr = df['x'].values.tolist()
        self.y_arr = df['y'].values.tolist()
        self.z_arr = df['z'].values.tolist()
        self.pitch = df['pitch'].values.tolist()
        self.yaw = df['yaw'].values.tolist()
        self.roll = df['roll'].values.tolist()
        self.num = len(self.z_arr)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.num:
            raise StopIteration()
        value1 = np.array([self.x_arr[self.i], self.y_arr[self.i], self.z_arr[self.i]])
        value2 = np.array([self.pitch[self.i], self.yaw[self.i], self.roll[self.i]])
        self.i += 1
        return value1, value2

t = Transformation()
points = Points()
plot = CreatePlot(t.A, t.O, t.B)

for sBP, rot in points:
    rBP = t.conv2(sBP. rot)
    plot.arrow(rBP, t.B, "r")
    rOP = t.conv1(sBP)
    #print (rOP)
    plot.arrow(rOP, t.O, "b")

plt.show()
print ("aaa")