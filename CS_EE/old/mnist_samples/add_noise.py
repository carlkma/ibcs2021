import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import util

img = Image.open("mnist2.jpeg")
img = np.array(img)
print(img.shape)

gaussian_img = util.random_noise(img,mode="gaussian")
salt_img = util.random_noise(img,mode="salt",seed=1)
pepper_img = util.random_noise(img,mode="pepper")
snp_img = util.random_noise(img,mode="s&p")
speckle_img = util.random_noise(img,mode="speckle")

plt.subplot(2,3,1), plt.title("original")
plt.imshow(img, cmap=plt.cm.binary)
plt.subplot(2,3,2),plt.title("gaussian")
plt.imshow(gaussian_img, cmap=plt.cm.binary)
plt.subplot(2,3,3), plt.title("salt")
plt.imshow(salt_img, cmap=plt.cm.binary)
plt.subplot(2,3,4), plt.title("pepper")
plt.imshow(pepper_img, cmap=plt.cm.binary)
plt.subplot(2,3,5),plt.title("salt & pepper")
plt.imshow(snp_img, cmap=plt.cm.binary)
plt.subplot(2,3,6), plt.title("speckle")
plt.imshow(speckle_img, cmap=plt.cm.binary)
plt.show()