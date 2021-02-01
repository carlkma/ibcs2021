import cv2
import math
import numpy as np
from PIL import Image
from skimage import util
#import matplotlib.pyplot as plt
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
img1 = x_test[30]
#plt.imshow(img1, cmap=plt.cm.binary)
#plt.show()
std = 0.01
amount = 0.01
noise = "s&p"
#img2 = util.random_noise(x_test[30],mode=noise,var=std**2)
img2 = util.random_noise(x_test[30],mode=noise,amount=amount)
img2 = img2 * 255
img2 = img2.astype("uint8")

im1 = Image.fromarray(img1)
im2 = Image.fromarray(img2)
im1.save("1.png")
im2.save("2.png")
img1 = cv2.imread('1.png')
img2 = cv2.imread('2.png')

p_signal = 255
p_noise = std
theoretical_psnr = 10 * math.log(p_signal/p_noise,10)
print("Theoretical: " + str(theoretical_psnr))

experimental_psnr = cv2.PSNR(img1, img2)
print("Experimental: " + str(experimental_psnr))