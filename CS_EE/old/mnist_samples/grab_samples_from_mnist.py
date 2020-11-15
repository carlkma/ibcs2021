from keras.datasets import mnist
from PIL import Image

(x_train, y_train), (x_test, y_test) = mnist.load_data()

for i in range(10):

	im = Image.fromarray(x_train[i])
	im.save("mnist" + str(i) + ".jpeg")