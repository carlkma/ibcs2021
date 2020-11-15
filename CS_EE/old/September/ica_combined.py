from keras.datasets import mnist
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FastICA as PCA
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
pca1 = PCA(n_components=10)
x_train1 = pca1.fit_transform(x_train)
x_test1 = pca1.transform(x_test)
end = time.time()
alltime.append(end-start)

start = time.time()
pca2 = PCA(n_components=20)
x_train2 = pca2.fit_transform(x_train)
x_test2 = pca2.transform(x_test)
end = time.time()
alltime.append(end-start)

start = time.time()
pca3 = PCA(n_components=30)
x_train3 = pca3.fit_transform(x_train)
x_test3 = pca3.transform(x_test)
end = time.time()
alltime.append(end-start)

start = time.time()
pca4 = PCA(n_components=40)
x_train4 = pca4.fit_transform(x_train)
x_test4 = pca4.transform(x_test)
end = time.time()
alltime.append(end-start)

start = time.time()
pca5 = PCA(n_components=50)
x_train5 = pca5.fit_transform(x_train)
x_test5 = pca5.transform(x_test)
end = time.time()
alltime.append(end-start)

start = time.time()
pca6 = PCA(n_components=100)
x_train6 = pca6.fit_transform(x_train)
x_test6 = pca6.transform(x_test)
end = time.time()
alltime.append(end-start)

network1 = models.Sequential()
network1.add(layers.Dense(128,activation="relu",input_shape=(10,)))
network1.add(layers.Dense(10,activation="softmax"))
network1.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history1 = network1.fit(x_train1,y_train,epochs=50,batch_size=512,validation_data=(x_test1,y_test))

network2 = models.Sequential()
network2.add(layers.Dense(128,activation="relu",input_shape=(20,)))
network2.add(layers.Dense(10,activation="softmax"))
network2.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history2 = network2.fit(x_train2,y_train,epochs=50,batch_size=512,validation_data=(x_test2,y_test))


network3 = models.Sequential()
network3.add(layers.Dense(128,activation="relu",input_shape=(30,)))
network3.add(layers.Dense(10,activation="softmax"))
network3.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history3 = network3.fit(x_train3,y_train,epochs=50,batch_size=512,validation_data=(x_test3,y_test))

network4 = models.Sequential()
network4.add(layers.Dense(128,activation="relu",input_shape=(40,)))
network4.add(layers.Dense(10,activation="softmax"))
network4.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history4 = network4.fit(x_train4,y_train,epochs=50,batch_size=512,validation_data=(x_test4,y_test))

network5 = models.Sequential()
network5.add(layers.Dense(128,activation="relu",input_shape=(50,)))
network5.add(layers.Dense(10,activation="softmax"))
network5.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history5 = network5.fit(x_train5,y_train,epochs=50,batch_size=512,validation_data=(x_test5,y_test))

network6 = models.Sequential()
network6.add(layers.Dense(128,activation="relu",input_shape=(100,)))
network6.add(layers.Dense(10,activation="softmax"))
network6.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history6 = network6.fit(x_train6,y_train,epochs=50,batch_size=512,validation_data=(x_test6,y_test))

network7 = models.Sequential()
network7.add(layers.Dense(128,activation="relu",input_shape=(28*28,)))
network7.add(layers.Dense(10,activation="softmax"))
network7.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
history7 = network7.fit(x_train,y_train,epochs=50,batch_size=512,validation_data=(x_test,y_test))

print(alltime)

plt.plot(history1.history["val_accuracy"])
plt.plot(history2.history["val_accuracy"])
plt.plot(history3.history["val_accuracy"])
plt.plot(history4.history["val_accuracy"])
plt.plot(history5.history["val_accuracy"])
plt.plot(history6.history["val_accuracy"])
plt.plot(history7.history["val_accuracy"])
plt.title("Model Accuracy with PCA")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["n=10","n=20","n=30","n=40","n=50","n=100","n=784"],loc="lower right")
plt.show()



#,"n=30","n=40","n=50","n=100","n=784"