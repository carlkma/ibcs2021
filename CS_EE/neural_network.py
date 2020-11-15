from keras import models, layers, optimizers

def fit(n_components, n_epochs, x_train, y_train, x_test, y_test):
	network = models.Sequential()
	network.add(layers.Dense(128,activation="relu",input_shape=(n_components,)))
	network.add(layers.Dense(10,activation="softmax"))
	rms = optimizers.RMSprop(learning_rate=0.0001)
	network.compile(optimizer=rms,loss='categorical_crossentropy',metrics=['accuracy'])
	history = network.fit(x_train,y_train,epochs=n_epochs,batch_size=512,validation_data=(x_test,y_test))
	return history