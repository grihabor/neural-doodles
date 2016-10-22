from skimage import io
import sys
import numpy as np

#n_channles = 4

if len(sys.argv) < 3:
    print("Usage: ")
    print("python3 merge.py file_1 file_2 ... file_n")
    print("Description:")
    print("merges file_1, file_2, ..., file_n into output.jpg")
    print("merges *_sem.png files into output_sem.png")
    sys.exit()

def merge(filenames, output):
    images = []
    sum_width = 0
    max_height = -1
    
    for i in range(1, len(filenames)):
        images.append(io.imread(filenames[i]))
        '''
        if images[-1].shape[2] != n_channles:
            print('Only', n_channles, 'channel images supported')
            print('channels in' + filenames[i] + ':', images[-1].shape[2])
            sys.exit()
        '''
        sum_width += images[-1].shape[1]
        if max_height == -1 or max_height < images[-1].shape[0]:
            max_height = images[-1].shape[0]
        
    n_channles = images[0].shape[2]
    final_image = np.zeros((max_height, sum_width, n_channles), dtype=np.uint8)

    x = 0
    for img in images:    
        final_image[0:img.shape[0], x:x+img.shape[1], :] = img
        x += img.shape[1]

    io.imsave(output, final_image)


merge(sys.argv, "output.jpg")
merge([filename[:-4] + '_sem.png' for filename in sys.argv], "output_sem.png")
