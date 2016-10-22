import numpy as np
import skimage.io as io
import sys
from sklearn.cluster import KMeans
import skimage.transform as tfm


def downscale(img):
    t = img.astype(np.int32)
    return (t[::2, ::2] + t[1::2, ::2] + t[::2, 1::2] + t[1::2, 1::2])/4

def upscale(img):
    t = np.zeros((img.shape[0]*2, img.shape[1]*2), dtype=np.int8)
    t[::2, ::2] = img
    t[1::2, ::2] = img
    t[::2, 1::2] = img
    t[1::2, 1::2] = img
    return t

colors = [[0, 0, 0],
            [0, 0, 255],
            [0, 255, 0],
            [255, 0, 0],
            [255, 255, 0],
            [255, 0, 255],
            [0, 255, 255]]
             

filename = sys.argv[1]
original = io.imread(filename)

if original.shape[0] % 2 != 0 or original.shape[1] % 2 != 0:
    original = tfm.resize(original, [original.shape[0]//2*2, original.shape[1]//2*2, original.shape[2]])
    io.imsave(filename, original)

#downscale = 2
img = original#downscale(original)

arr = np.reshape(img, [-1, 3])
labels = KMeans(n_clusters = 8).fit_predict(arr)
labels = labels.reshape((img.shape[0], -1))

labels *= 32

#labels = upscale(labels)


io.imsave("{}_sem.png".format(filename[:-4]), labels)
