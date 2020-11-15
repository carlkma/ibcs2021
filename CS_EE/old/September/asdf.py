'''
from keras.datasets import mnist
import numpy as np
(x_train, _), (x_test, _) = mnist.load_data(path="")
'''

import scipy.io

asdf = scipy.io.loadmat("mnist-with-awgn.gz")
print(asdf)