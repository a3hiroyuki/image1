import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
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
    zeros = np.zeros((height, width), img1.dtype)
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
    a = (img - np.mean(img))/np.std(img) * 1 + 0
    return a.astype(dtype='uint8')

def plot_hist_rgb(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist(img,[i],None,[256],[0,256])
        plt.plot(histr, color = col)
        plt.xlim([0,256])

def plot_hist(img):
    plt.hist(img.ravel(),256,[0,256]);


FILE_PATH = 'D:\\data2\\'
FILE_PATH1 = FILE_PATH + 'right\\'
FILE_PATH2 = FILE_PATH + 'left\\'
OUTPUT_DIR = FILE_PATH + 'output\\'

files1 = [os.path.abspath(p) for p in glob.glob(FILE_PATH1 + "*")]
files2 = [os.path.abspath(p) for p in glob.glob(FILE_PATH2 + "*")]

print (files1)
print (files2)

fig = plt.figure(figsize=(25,25))
plt.xticks(color="None")
plt.yticks(color="None")

#必要な分だけ回す
for i, file_path1 in enumerate(files1):
    print (file_path1)
    file_path2 = files2[i]
    img1 = cv2.imread(file_path1)
    img2 = cv2.imread(file_path2)

    #一行目
    ax = fig.add_subplot(2, 2, 1)
    ax.set_title("right", loc='center')
    plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

    img1_blue_c3, img1_green_c3, img1_red_c3 , img1_norm = exec_norm_rgb(img1)
    ax = fig.add_subplot(2, 2, 2)
    ax.set_title("right_正規化", loc='center')
    plt.imshow(cv2.cvtColor(img1_norm, cv2.COLOR_BGR2RGB))

    #2行目
    ax = fig.add_subplot(2, 2, 3)
    plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

    img2_blue_c3, img2_green_c3, img2_red_c3 , img2_norm = exec_norm_rgb(img2)
    fig.add_subplot(2, 2, 4)
    plt.imshow(cv2.cvtColor(img2_norm, cv2.COLOR_BGR2RGB))

    plt.savefig(OUTPUT_DIR + str(i) + '.png')

print ("finish!s")


