import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import os
import cv2


Pythoncolors = {'orange':'orange','apple':'red','peach':'pink'}
CUR_DIR = 'D:\\data\\'
#FILE_NAME = '2019-02-22-10-53-54.csv'
FILE_NAME = '2019-02-22-11-25-00.csv'

def angle_conv(x, y):
    dot_xy = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos = dot_xy / (norm_x*norm_y)
    rad = np.arccos(cos)
    theta = rad * 180 / np.pi
    return theta

def get_ang_vectors(angles):
    ang_vectors = []
    for i, angle in enumerate(angles):
        angle *= -1
        angles_rad = angle * (math.pi / 180.0);
        ang_x = math.cos(angles_rad);
        ang_y = math.sin(angles_rad);
        ang_vec = np.array([ang_x, ang_y])
        ang_vectors.append(ang_vec)
    return ang_vectors


def show_img(plt, image_paths, size, i, error_num, num):
    plt.subplot(size, 3, i * 3 + num)
    plt.title(error_num + (num - 2),loc='center')
    try:
        path = image_paths[error_num + (num -2)]
        file_name = os.path.basename(path)
        img = cv2.imread(CUR_DIR + file_name)
        plt.imshow(img,clim=[0,255])
    except:
        pass

def plot_img(image_list, image_paths):
    plt.figure(figsize=(20,20))
    for i, error_num in enumerate(image_list):
        size = len(image_list)
        show_img(plt, image_paths, size, i, error_num,  1)
        show_img(plt, image_paths, size, i, error_num,  2)
        show_img(plt, image_paths, size, i, error_num,  3)
    plt.show()


def is_error(diff_angle, diff_distance, error_num):
    #print (error_num)
    offset = error_num * 0.5
    if diff_distance > 3 + offset:
        return True
    elif diff_angle > 60 and diff_distance > 1 + offset:
        return True
    else:
        return False

df = pd.read_csv(CUR_DIR + FILE_NAME,
                          names=('Ang', 'B', 'C', 'X', 'Y', 'F', 'IMG', 'H', 'I'))
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
correct_list = []
error_num = 0
temp = None
for i in range(len(posi_vectors)):
    if len(correct_list) == 0:
        diff_vector = posi_vectors[i+1] - posi_vectors[i]
        diff_angle = angle_conv(diff_vector, ang_vectors[i])
        diff_distance = np.linalg.norm(diff_vector)
        if is_error(diff_angle, diff_distance, 0) == False:
            if temp is None:
                temp = i
            else:
                correct_list.append(temp)
                correct_list.append(i)
    else:
        indix = correct_list[-1]
        diff_vector = posi_vectors[i] - posi_vectors[indix]
        diff_angle = angle_conv(diff_vector, ang_vectors[i])
        #print ('%d:%f' % (i, diff_angle))
        diff_distance = np.linalg.norm(diff_vector)
        if is_error(diff_angle, diff_distance, error_num) == False:
            error_num = 0
            correct_list.append(i)
        else:
            error_num = error_num + 1

print (correct_list)

plt.figure(figsize=(10,10))
plt.subplot(1,1,1)
plt.title(FILE_NAME,loc='center')

for i in range(len(ang_vectors)):
    plt.quiver(posi_vectors[i][0], posi_vectors[i][1], ang_vectors[i][0],ang_vectors[i][1],angles='xy',scale_units='xy',scale=1)

error_images = []
for i,(x,y) in enumerate(zip(posi_vectors[:, 0],posi_vectors[:, 1])):
    plt.annotate(str(i),(x,y))
    if correct_list.__contains__(i) == False:
        plt.scatter(x,y,c='red')
        error_images.append(i)
    else:
        plt.scatter(x,y,c='blue')

plt.plot(posi_vectors[:, 0],posi_vectors[:,1])
plt.show()

#plot_img(error_images, image_paths)