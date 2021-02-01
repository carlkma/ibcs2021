import math
import scipy
import numpy as np
from skimage import util
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import to_categorical
import time
import os
import psutil

# -- TRAIN AND TEST DATA PREPARATION -- #
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape((60000,28*28))
x_train = x_train.astype("float32") / 255

x_test = x_test.reshape((10000,28*28))
x_test = x_test.astype("float32") / 255

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# -- DIMENSIONALITY REDUCTION -- #
start = time.time()
import dim_reduction
x_train0, x_test0 = dim_reduction.apply(30, x_train, x_test, "FA")

# -- NEURAL NETWORK -- #
import neural_network
history0 = neural_network.fit(30, 30, x_train0, y_train, x_test0, y_test)
end = time.time()


print(end-start)
process = psutil.Process(os.getpid())
print(process.memory_info().rss) # in bytes

# rss: aka “Resident Set Size”, this is the non-swapped physical memory a process has used.
# https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info