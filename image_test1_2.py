import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def exec_gamma_correction(img ):
    gamma = 3.0
    # ガンマ値を使って Look up tableを作成
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    # Look up tableを使って画像の輝度値を変更
    imgA = cv2.LUT(img, lookUpTable)
    return imgA


def exec_norm_rgb(img):
    height, width, channels = img.shape[:3]
    zeros = np.zeros((height, width), img.dtype)
    img_blue_c1, img_green_c1, img_red_c1 = cv2.split(img)
    img_blue_c3 = cv2.merge((img_blue_c1, zeros, zeros))
    img_green_c3 = cv2.merge((zeros, img_green_c1, zeros))
    img_red_c3 = cv2.merge((zeros, zeros, img_red_c1))
    img2_b = normalize(img_blue_c1)
    img2_g = normalize(img_green_c1)
    img2_r = normalize(img_red_c1)
    img2 = cv2.merge((img2_b, img2_g, img2_r))
    return img_blue_c3, img_green_c3, img_red_c3, img2

def normalize(img):
    a = (img - np.mean(img))/np.std(img) * 16 + 128
    return a.astype(dtype='uint8')

def plot_hist_rgb(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist(img,[i],None,[256],[0,256])
        plt.plot(histr, color = col)
        plt.xlim([0,256])

def plot_hist(img):
    plt.hist(img.ravel(),256,[0,256]);


plt.figure(figsize=(10,10))

is_hsv = True
BASE = 'C:\\aaa\\diff\\'
file_name1 = BASE + 'day.png'
file_name2 = BASE + 'night.jpg'

img1 = cv2.imread(file_name1)
img2 = cv2.imread(file_name2)


#上段
plt.subplot(2, 4, 1)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

p_file_name1 = os.path.basename(file_name1)
p_file_name1 = os.path.splitext(p_file_name1)[0]
p_file_name2= ''
conv_img1 = None
if is_hsv:
    p_file_name2 = 'hsv'
    conv_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
else:
    p_file_name2 = 'rgb'
    conv_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img_color_arr1 = cv2.split(conv_img1)

for i in range(0, 3):
    plt.subplot(2, 4, i + 2)
    plt.imshow(cv2.cvtColor(img_color_arr1[i], cv2.COLOR_BGR2RGB))
    cv2.imwrite('{0}{1}_{2}{3}.jpg'.format(BASE, p_file_name1, p_file_name2, str(i) ), img_color_arr1[i])



#下段
plt.subplot(2, 4, 5)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

p_file_name1 = os.path.basename(file_name2)
p_file_name1 = os.path.splitext(p_file_name1)[0]
conv_img2 = None
if is_hsv:
    conv_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
else:
    conv_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_color_arr2 = cv2.split(conv_img2)

for i in range(0, 3):
    plt.subplot(2, 4, i + 6)
    plt.imshow(cv2.cvtColor(img_color_arr2[i], cv2.COLOR_BGR2RGB))
    cv2.imwrite('{0}{1}_{2}{3}.jpg'.format(BASE, p_file_name1, p_file_name2, str(i) ), img_color_arr2[i])

plt.show()
