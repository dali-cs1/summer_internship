import numpy as np
import rasterio
import cv2
import matplotlib.pyplot as plt
from preprocessingDART import downsample_MTF, upsample_perfect


def down_up_sentinel(img, freq_down_up = 32):
    # row = int(img.shape[1] / freq_down_up) * freq_down_up
    # col = int(img.shape[2] / freq_down_up) * freq_down_up
    #
    # img_down_up = np.zeros([10,row, col])
    img_down_up= np.zeros_like(img[:10,:,:])
    for b in range(10):
        band = img[b, :, :]

        dsize = (int(band.shape[0] / freq_down_up) * freq_down_up, int(band.shape[1] / freq_down_up) * freq_down_up)
        band32 = cv2.resize(band, dsize)
        band32_down = downsample_MTF(band32, 0.2, freq_down_up, 171)

        band32_up = upsample_perfect(band32_down, 32)
        band32_up = cv2.resize(band32_up,(band.shape[1], band.shape[0]))
        img_down_up[b,:,:] = band32_up
        # plt.figure()
        # plt.subplot(1, 3, 1)
        # plt.imshow(band32, cmap='gray', vmin=2000, vmax=8000)
        # plt.title("HR sentinel image")
        # plt.subplot(1, 3, 2)
        # plt.imshow(band32_down, cmap='gray', vmin=2000, vmax=8000)
        # plt.title("After downsampling")
        # plt.subplot(1, 3, 3)
        # plt.imshow(band32_up, cmap='gray', vmin=2000, vmax=8000)
        # plt.title("After upsampling")
        # plt.show()
    return img_down_up

# freq_down_up = 32
#
# imagename = "./Dataset/TrainingDART/seq_treesize0.5_1/seq_treesize0.5_1.tif"
#
# src = rasterio.open(imagename)
# img = src.read()
#
# img_down_up = down_up_sentinel(img)
