import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import ArtistAnimation

CUR_DIR = "C:\\aaa\\"


height1 = [[10,20], [20, 30], [30, 40], [40,50],[50,60]]  # 点数1

left = np.arange(len(height1[0]))  # numpyで横軸を設定
labels = ['AAA', 'Math']

height = 0.3

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_ylabel('gene')
ax.set_xlabel('gene expression [log(TPM)]')
#x = np.linspace(0, np.pi * 4, 100)

frames = []  # 各フレームを構成する Artist 一覧
for i in range(len(height1)):
    print (i)
    artists = ax.barh(left, height1[i], tick_label=labels)
    frames.append(artists)

print (len(frames))
# アニメーションを作成する。
anim = ArtistAnimation(fig, frames, interval=500)

# gif 画像として保存する。
anim.save(CUR_DIR + 'animation2.gif', writer='imagemagick')

# Figure を表示する。
fig.show()