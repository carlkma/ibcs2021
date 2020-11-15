import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import util


img = Image.open("IMG_0085.JPG")
img = np.array(img)

noise_gs_img = util.random_noise(img,mode="gaussian",var=0.05**2)
noise_salt_img = util.random_noise(img,mode="salt")
noise_pepper_img = util.random_noise(img,mode="pepper")
noise_sp_img = util.random_noise(img,mode="s&p")
noise_speckle_img = util.random_noise(img,mode="speckle")
plt.subplot(2,3,1), plt.title("original")
plt.imshow(img)
plt.subplot(2,3,2),plt.title("gaussian")
plt.imshow(noise_gs_img)
plt.subplot(2,3,3), plt.title("salt")
plt.imshow(noise_salt_img)
plt.subplot(2,3,4), plt.title("pepper")
plt.imshow(noise_pepper_img)
plt.subplot(2,3,5),plt.title("s&p")
plt.imshow(noise_sp_img)
plt.subplot(2,3,6), plt.title("speckle")
plt.imshow(noise_speckle_img)
plt.show()