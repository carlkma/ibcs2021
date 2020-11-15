from keras.datasets import mnist
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FastICA
import numpy as np
from keras import models
from keras import layers
from keras import optimizers
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import time

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape((60000,28*28))
x_test = x_test.reshape((10000,28*28))

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

rms = optimizers.RMSprop(learning_rate=0.0001)
alltime = []

start = time.time()
pca1 = FastICA(n_components=50)
x_train1 = pca1.fit_transform(x_train)
x_test1 = pca1.transform(x_test)
end = time.time()
alltime.append(end-start)


network1 = models.Sequential()
network1.add(layers.Dense(128,activation="relu",input_shape=(50,)))
network1.add(layers.Dense(10,activation="softmax"))
network1.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history1 = network1.fit(x_train1,y_train,epochs=100,batch_size=512,validation_data=(x_test1,y_test))

print(alltime)
plt.plot(history1.history["val_accuracy"])
plt.title("Model Accuracy with ICA")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["n=9"],loc="lower right")
plt.show()

