import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import os
import cv2
from datetime import datetime

CUR_DIR = 'D:\\data\\'


class PointsChecker():

    ANGLE_LIMIT = 50
    DIST_LIMIT = 2

    def __init__(self, posi_vectors, ang_vectors):
        self.posi_vectors = posi_vectors
        self.ang_vectors = ang_vectors
        self.correct_list = []
        self.temp_success_list =[]
        self.check_points()

    def check_points(self):
        temp = -1
        in_error = False
        for i in range(len(self.posi_vectors)):
            if len(self.correct_list) == 0:
                diff_distance, diff_angle = self.get_diff(i, i+1)
                if self.is_error(diff_distance, diff_angle, 0, False) == False:
                    if temp == -1:
                        temp = i
                    else:
                        self.correct_list.append(temp)
                        self.correct_list.append(i)
            else:
                index = self.correct_list[-1]
                diff_distance, diff_angle = self.get_diff(int(index), i)
                if self.is_error( diff_distance, diff_angle, i, in_error) == True:
                    in_error = True
                else:
                    in_error = False
                    self.correct_list.append(i)
                    if len(self.temp_success_list) > 0:
                        self.correct_list.extend(self.temp_success_list)
                        self.temp_success_list.clear()


    def is_error(self, diff_distance, diff_angle, index1, in_error):
        if in_error == False: #初めてのエラー
            if (diff_distance > PointsChecker.DIST_LIMIT) or (diff_distance > PointsChecker.DIST_LIMIT/2 and diff_angle > PointsChecker.ANGLE_LIMIT):
                return True
            else:
                return False
        else:                      #2回目以降のエラー
            if (diff_distance > 10) or (diff_distance > 5 and diff_angle > PointsChecker.ANGLE_LIMIT):  #明らかな異常値の場合はエラーとする
                self.temp_success_list.clear()
                return True
            else:                  #エラーからの復帰チェック
                self.temp_success_list.append(index1)
                if (len(self.temp_success_list)) >= 2:
                    index2 = self.temp_success_list[-2]
                    diff_distance, diff_angle = self.get_diff(index2, index1)
                    print ('%d:%f' % (index2, diff_angle))
                    if ( diff_distance < PointsChecker.DIST_LIMIT and diff_angle < PointsChecker.ANGLE_LIMIT):
                        return False
                    else:
                        self.temp_success_list.pop(-2)
                return True

    def get_diff(self, start_id, end_id):
        diff_vector = self.posi_vectors[end_id] - self.posi_vectors[start_id]
        diff_angle = self.angle_conv(diff_vector, self.ang_vectors[start_id])
        diff_distance = np.linalg.norm(diff_vector)
        return math.fabs(diff_distance), math.fabs(diff_angle)

    def angle_conv(self, x, y):
        dot_xy = np.dot(x, y)
        norm_x = np.linalg.norm(x)
        norm_y = np.linalg.norm(y)
        cos = dot_xy / (norm_x*norm_y)
        rad = np.arccos(cos)
        theta = rad * 180 / np.pi
        return theta


class ImagePlot():

    ROW_SIZE = 5
    COL_SIZE = 3

    def __init__(self, dir_path, data_name, error_id_list, image_paths):
        self.dir_path = dir_path
        self.data_name = data_name
        self.error_id_list = error_id_list
        self.image_paths = image_paths
        self.image_file_num = math.ceil(len(error_id_list) / ImagePlot.ROW_SIZE)

    def plot_img(self):
        for file_id in range(self.image_file_num):
            plt.figure(figsize=(10,10))
            plt.title('aaaaa', loc='center')
            for row in range(ImagePlot.ROW_SIZE):
                index = ImagePlot.ROW_SIZE * file_id + row
                self.show_img(index, row,  1)
                self.show_img(index, row,  2)
                self.show_img(index, row,  3)
            plt.savefig(self.dir_path + self.data_name + '_' + str(file_id) + '..png')

    def show_img(self, index, row, col):
        plt.subplot(ImagePlot.ROW_SIZE, ImagePlot.COL_SIZE, row * 3 + col)
        try:
            image_id = self.error_id_list[index]
            plt.title(image_id + (col - 2), loc='center')
            path = self.image_paths[image_id + (col - 2)]
            file_name = os.path.basename(path)
            plt.xticks(color="None")
            plt.yticks(color="None")
            img = cv2.imread(CUR_DIR + file_name)
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        except:
            pass



def make_dir(plt, date_now, data_name):
    base_dir = 'D:\\map_data\\'
    dir_path1 =  base_dir + date_now
    if os.path.exists(dir_path1) == False:
        os.mkdir(dir_path1)
    dir_path2 = dir_path1 + '\\' + data_name
    os.mkdir(dir_path2)
    return dir_path2 + '\\'


def get_ang_vectors(angles):
    ang_vectors = []
    for angle in angles:
        angle *= -1
        angles_rad = angle * (math.pi / 180.0);
        ang_x = math.cos(angles_rad);
        ang_y = math.sin(angles_rad);
        length = (ang_x*ang_x + ang_y*ang_y) ** 0.5
        print (length)
        ang_vec = np.array([ang_x/length, ang_y/length])
        ang_vectors.append(ang_vec)
    return ang_vectors

def main(date_now, file_name):
    df = pd.read_csv(CUR_DIR + file_name, names=('Ang', 'B', 'C', 'X', 'Y', 'F', 'IMG', 'H', 'I'))
    angles = df['Ang'].values.astype('float')
    angles = np.array(angles)
    x_arr = df['X'].values.astype('float')
    x_arr = np.array(x_arr)
    y_arr = df['Y'].values.astype('float')
    y_arr = np.array(y_arr)
    image_paths = df['IMG']
    a = np.reshape(x_arr, (-1,1))
    b = np.reshape(y_arr, (-1,1))
    posi_vectors = np.concatenate([a, b],axis=1)

    ang_vectors = get_ang_vectors(angles)

    #外れ値のチェック
    correct_list = PointsChecker(posi_vectors, ang_vectors).correct_list

    plt.figure(figsize=(30,10))
    plt.title(file_name,loc='center')

    for i in range(len(ang_vectors)):
        plt.quiver(posi_vectors[i][0], posi_vectors[i][1], ang_vectors[i][0],ang_vectors[i][1], angles='xy', scale_units='xy', scale=1, color='orange')

    error_id_list = []
    for i,(x,y) in enumerate(zip(posi_vectors[:, 0],posi_vectors[:, 1])):
        plt.annotate(str(i),(x,y),color='black')
        if correct_list.__contains__(i) == False:
            plt.scatter(x,y,c='red')
            error_id_list.append(i)
        else:
            plt.scatter(x,y,c='blue')

    plt.plot(posi_vectors[:, 0],posi_vectors[:,1],color='green')
    plt.show()

#     file_name, _ = os.path.splitext(file_name)
#     dir_path = make_dir(plt, date_now, file_name)
#     plt.savefig(dir_path + '\\figure.png')
#     ImagePlot(dir_path, file_name, error_id_list, image_paths).plot_img()



if __name__ == '__main__':
    date_now = datetime.now().strftime("%Y%m%d%H%M%S")
    main(date_now, FILE_NAME1)
#     main(date_now, FILE_NAME2)
#     main(date_now, FILE_NAME3)
#     main(date_now, FILE_NAME4)
    print ('finish!!!')



