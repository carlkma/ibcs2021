#!/usr/bin/env python
# coding: utf-8

# In[22]:


'''
VARIABLE: METHOD OF DR


'''


# In[23]:


# -- IMPORTS -- #
import math
import scipy
import numpy as np
from skimage import util
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import to_categorical


# In[24]:


# -- TRAIN AND TEST DATA PREPARATION -- #
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test_noisy = np.empty((len(x_test),28,28),dtype="float64")

std = 0.1
for i in range(len(x_test)):
    x_test_noisy[i] = util.random_noise(x_test[i],mode="gaussian",var=std**2)


# In[25]:


# -- OUTPUT SNR AND SAMPLE NOISY IMAGE -- #
p_signal = np.mean(x_test[30])
p_noise = std
snr = 10 * math.log(p_signal/p_noise,10)
print(snr)

plt.imshow(x_test_noisy[30],cmap=plt.cm.binary)
plt.show()


# In[18]:


# -- CONVERTING DATA FOR INPUT INTO NEURAL NETWORK -- #
x_train = x_train.reshape((60000,28*28))
x_train = x_train.astype("float32") / 255

x_test = x_test.reshape((10000,28*28))
x_test_noisy = x_test_noisy.reshape((10000,28*28))

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)


# In[19]:


# -- DIMENSIONALITY REDUCTION -- #
import dim_reduction
x_train0, x_test_noisy0 = x_train.copy(), x_test_noisy.copy()
x_train1, x_test_noisy1 = dim_reduction.apply(30, x_train, x_test_noisy, "PCA")
x_train2, x_test_noisy2 = dim_reduction.apply(30, x_train, x_test_noisy, "FA")


# In[20]:


# -- NEURAL NETWORK -- #
import neural_network
history0 = neural_network.fit(784, 30, x_train0, y_train, x_test_noisy0, y_test)
history1 = neural_network.fit(30, 30, x_train1, y_train, x_test_noisy1, y_test)
history2 = neural_network.fit(30, 30, x_train2, y_train, x_test_noisy2, y_test)


# In[21]:


# -- OUTPUT PLOTS -- #
plt.plot(history0.history["val_accuracy"])
plt.plot(history1.history["val_accuracy"])
plt.plot(history2.history["val_accuracy"])
plt.plot(history3.history["val_accuracy"])
plt.title("Model Accuracy (Gaussain)")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["None", "PCA", "FA"],loc="lower right")
plt.show()

