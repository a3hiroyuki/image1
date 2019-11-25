from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import math
import tf

def quaternion_to_euler(px,py,pz,pw):
    e = tf.transformations.euler_from_quaternion(px, py, pz, pw)
    return np.array([e[0], e[1], e[2]])

class CreatePlot:
    lim = 5
    def __init__(self, A, O, T):
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
        self.arrow(et1_O, T, "k")
        self.arrow(et2_O, T, "k")
        self.arrow(et3_O, T, "k")

    def arrow(self, v, sp, c):
        # 空間座標基準で矢印をプロットする
        # v:ベクトル、sp:始点、c:色
        l = np.sqrt(v[0]**2+v[1]**2+v[2]**2)
        v_norm = v / np.linalg.norm(v)
        self.ax.quiver(sp[0], sp[1], sp[2],
                  v_norm[0], v_norm[1], v_norm[2],
                  length=l,
                  color=c,
                  linewidth=1)

class Transformation:
    def __init__(self):
        a = open('ccc.json')
        b = json.load(a)
        print (b)
        tx, ty, tz = b["trans"][0], b["trans"][1], b["trans"][2]
        ox, oy, oz = b["center"][0], b["center"][1], b["center"][2]
        rx, ry, rz = b["rot"][0], b["rot"][1], b["rot"][2]
        sx, sy, sz = b["scale"][0], b["scale"][1], b["scale"][2]
        #原点
        self.O = np.array([0, 0, 0])
        # T
        offset = np.array([ox, oy, oz])
        self.T = -1 * np.array([ tx, ty, tz]) + offset
        self.T = np.array([self.T[0], self.T[1], self.T[2]])
        #self.rOB =  self.O - self.B
        # R
        rx = math.radians(rx)
        ry = math.radians(ry)
        rz = math.radians(rz)
        p = np.array([rx, ry, rz])
        R = self.rotM(p)
        self.A = R.T
        # S
        self.scale = np.array([sx, sy, sz])

    def rotM(self, p):
        # 回転行列を計算する
        px = p[0]
        py = p[1]
        pz = p[2]
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(px), np.sin(px)],
                       [0, -np.sin(px), np.cos(px)]])
        Ry = np.array([[np.cos(py), 0, -np.sin(py)],
                       [0, 1, 0],
                       [np.sin(py), 0, np.cos(py)]])
        Rz = np.array([[np.cos(pz), np.sin(pz), 0],
                       [-np.sin(pz), np.cos(pz), 0],
                       [0, 0, 1]])
        R = Rz.dot(Ry).dot(Rx)  # 物体座標系の 1->2->3 軸で回転させる
        #R = Rx.dot(Ry).dot(Rz)  # 物体座標系の 3->2->1 軸で回転させる
        #R = Rz.dot(Ry).dot(Rx)  # 空間座標系の 3->2->1 軸で回転させる
        return R

    def trans1(self, rL):
        return np.dot(self.A , rL)

    def trans2(self, rL):
        #temp1 = self.scale * sBP.T
        return self.T + self.trans1(rL)

class Points:
    def __init__(self):
        columns = ["no","status","x","y","z","qx","qy","qz","qw"]
        df = pd.read_csv('ccc.csv', names=columns)
        df = df[df['status']  == 'tracking']
        print (df)
        self.x_arr = df['x'].values.tolist()
        self.y_arr = df['y'].values.tolist()
        self.z_arr = df['z'].values.tolist()
        self.qx_arr = df['qx'].values.tolist()
        self.qy_arr = df['qy'].values.tolist()
        self.qz_arr = df['qz'].values.tolist()
        self.qw_arr = df['qz'].values.tolist()
        self.num = len(self.z_arr)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.num:
            raise StopIteration()
        posi = np.array([self.x_arr[self.i], self.y_arr[self.i], self.z_arr[self.i]])
        #rot = quaternion_to_euler(self.qx_arr[self.i], self.qy_arr[self.i], self.qz_arr[self.i], self.qw_arr[self.i])
        rot = 0
        self.i += 1
        return posi, rot

if __name__ == '__main__':
    t = Transformation()
    points = Points()
    plot = CreatePlot(t.A, t.O, t.T)

    i = 0
    for rL, rot in points:
        print(str(i) + ":")
        print(rL)
        plot.arrow(t.trans1(rL), t.T, "r")
        rW = t.trans2(rL)
        print (rW)
        plot.arrow(rW, t.O, "b")
        i = i + 1

    plt.show()
    print ("end")