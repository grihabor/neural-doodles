from skimage import io
from skimage import filters
from skimage import img_as_ubyte
import numpy as np
import sys

print('argv: ', sys.argv)
img = io.imread(sys.argv[1])
img = filters.gaussian(img, 0.01, multichannel=True)

for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        for val in range(img.shape[2]):
            if img[y, x, val] > 0. and img[y, x, val] <= .5:
                img[y, x, val] = 0.
            elif img[y, x, val] > .5 and img[y, x, val] < 1.:
                img[y, x, val] = 1.
  
img = img_as_ubyte(img).astype(np.int32)

#print(img[::50, ::50])

#img = np.pad()
image = img[:,:,0]*256*256 + img[:,:,1]*256 + img[:,:,2]

import operator
def most_freq(arr):
    dict = {}
    arr = arr.flatten()
    for val in arr:
        if val in dict:
            dict[val] += 1
        else:
            dict[val] = 1
    
    i = 0
    max_val = None
    max_n = None
    for val in dict:
        if i == 0:
            max_val = val
            max_n = dict[val]
        else:
            if dict[val] > max_n:
                max_val = val
                max_n = dict[val]
        i += 1
    
    return max_val

            
t = np.copy(image)
pad = 2
for y in range(pad, image.shape[0]-pad):
    for x in range(pad, image.shape[1]-pad):
        f = image[y-pad:y+pad+1, x-pad:x+pad+1]
        t[y, x] = most_freq(f)
        
img[:,:,0] = (t//256//256) % 256
img[:,:,1] = (t//256) % 256
img[:,:,2] = t % 256

  
io.imsave(sys.argv[1][:-4] + "em.png", img)