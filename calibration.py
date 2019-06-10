import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np

# チェスボードを撮影した画像を読み込む。
samples = []

PATH = "C:\\aaa\\calib\\"

for path in glob.glob(PATH + '*.jpg'):
    img = cv2.imread(path)
    samples.append(img)

print('number of samples:', len(samples))  # number of samples: 13
print('image shape:', samples[0].shape)  # image shape: (480, 640, 3)

#plt.imshow(samples[0])
#plt.show()


# チェスボードの設定
cols = 9  # 列方向の交点数
rows = 6  # 行方向の交点数
# チェスボードのマーカー検出を行う。
image_points = []
for img in samples:
    # 画像をグレースケールに変換する。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # チェスボードの交点を検出する。
    ret, corners = cv2.findChessboardCorners(img, (cols, rows))

    if ret:  # すべての交点の検出に成功
        image_points.append(corners)
    else:
        print('corners detection failed.')

# 1枚目の交点検出結果を可視化する。
print('corners shape', image_points[0].shape)  # corners shape (54, 1, 2)

img = samples[0].copy()
cv2.drawChessboardCorners(img, (cols, rows), image_points[0], ret)
plt.imshow(img)
plt.show()

img = samples[1].copy()
cv2.drawChessboardCorners(img, (cols, rows), image_points[1], ret)
plt.imshow(img)
plt.show()


# 検出した画像座標上の点に対応する3次元上の点を作成する。
world_points = np.zeros((rows * cols, 3), np.float32)
world_points[:, :2] = np.mgrid[:cols, :rows].T.reshape(-1, 2)
print('world_points shape:', world_points.shape)  # world_points shape: (54, 3)

print (world_points)

for img_pt, world_pt in zip(image_points[0], world_points):
    print('image coordinate: {} <-> world coordinate: {}'.format(img_pt, world_pt))

# 画像の枚数個複製する。
object_points = [world_points] * len(samples)

h, w, c = samples[0].shape
ret, camera_matrix, distortion, rvecs, tvecs = cv2.calibrateCamera(
    object_points, image_points, (w, h), None, None)

print('reprojection error:\n', ret)
print('camera matrix:\n', camera_matrix)
print('distortion:\n', distortion)
print('rvecs:\n', rvecs[0].shape)
print('tvecs:\n', tvecs[0].shape)
