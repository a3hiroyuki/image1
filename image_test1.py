import cv2
import numpy as np
from matplotlib import pyplot as plt

def exec_gamma_correction(img ):
    gamma = 3.0
    # ガンマ値を使って Look up tableを作成
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    # Look up tableを使って画像の輝度値を変更
    imgA = cv2.LUT(img, lookUpTable)
    return imgA


def exec_norm_rgb(img1):
    zeros = np.zeros((height, width), img1.dtype)

    img_blue_c1, img_green_c1, img_red_c1 = cv2.split(img1)

    img_blue_c3 = cv2.merge((img_blue_c1, zeros, zeros))
    img_green_c3 = cv2.merge((zeros, img_green_c1, zeros))
    img_red_c3 = cv2.merge((zeros, zeros, img_red_c1))
    img2_b = normalize(img_blue_c1)
    img2_g = normalize(img_green_c1)
    img2_r = normalize(img_red_c1)
    img2 = cv2.merge((img2_b, img2_g, img2_r))
    return img_blue_c3, img_green_c3, img_red_c3, img2

def normalize(img):
    a = (img - np.mean(img))/np.std(img)*16+32
    print (a)
    #return np.array(a, dtype='int8')
    b = a.astype(dtype='uint8')
    print (b)
    return b

def plot_hist(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist(img,[i],None,[256],[0,256])
        plt.plot(histr, color = col)
        plt.xlim([0,256])


plt.figure(figsize=(10,10))

img1 = cv2.imread('C:\\aaa\\cat.png')

print (img1.dtype)

if len(img1.shape) == 3:
    height, width, channels = img1.shape[:3]

#一行目
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

img1_blue_c3, img1_green_c3, img1_red_c3 , img1_norm = exec_norm_rgb(img1)
plt.subplot(2, 2, 2)
plt.imshow(img1_norm)

#2行目
img2 = exec_gamma_correction(img1)
plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

img2_blue_c3, img2_green_c3, img2_red_c3 , img2_norm = exec_norm_rgb(img2)

plt.subplot(2, 2, 4)
plt.imshow(img2_norm)

plt.show()

plt.figure(figsize=(10,10))

plt.subplot(2, 2, 1)
plot_hist(img1)

plt.subplot(2, 2, 2)
plot_hist(img2)


#print(img1_norm)
plt.subplot(2, 2, 3)
plot_hist(img1_norm)

plt.subplot(2, 2, 4)
plot_hist(img2_norm)

plt.show()
#3行目
# plt.subplot(4, 6, 13)
# plt.imshow(img2_blue_c3)
#
# plt.subplot(4, 6, 14)
# plt.imshow(img2_green_c3)
#
# plt.subplot(4, 6, 15)
# plt.imshow(img2_red_c3)
#
# plt.subplot(4, 6, 16)


# plt.subplot(4, 3, 5)
# plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
#
# plt.subplot(4, 3, 6)
# plt.imshow(img2)
#
#
#
#
# plt.subplot(4, 3, 7)
# plt.imshow(img3, clim=[0,255])
#
# _, _, _, img4 = exec_norm_rgb(img3)
#
# plt.subplot(4, 3, 8)
# plt.imshow(img4, clim=[0,255])
#
# hist1 = cv2.calcHist(img4, [0],None,[256],[0,256])
#
# plt.subplot(4, 3, 10)
# plt.imshow(cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB))
#
# plt.show()
#
# plt.figure(figsize=(10,10))
# plt.show()
# plt.subplot(1, 2, 1)
# plt.imshow(img1, clim=[0,255])
#
#
# print (np.mean(img1),np.std(img1))
# img2 = (img1 - np.mean(img1))/np.std(img1)
# plt.subplot(1, 2, 2)
# plt.imshow(img2, clim=[0,255])

