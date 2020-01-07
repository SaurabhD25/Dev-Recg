import os
import cv2
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.utils import np_utils, print_summary
import pandas as pd
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
import keras.backend as K
import pickle
import matplotlib.pyplot as plt

K.set_image_data_format('channels_last')

def keras_model(imagex,imagey):
    num_of_classes = 49
    model = Sequential()
    
    #convolutional layer 1
    model.add(Conv2D(filters=64, kernel_size=(3, 3), input_shape=x.shape[1:], activation='sigmoid'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    
    #convolutional layer 2
    model.add(Conv2D(32, (3, 3), activation='sigmoid'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    
    model.add(Conv2D(32, (3, 3), activation='sigmoid'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    
    #flattening
    model.add(Flatten()) #Flatten just flattens the output
    model.add(Dense(64))
    
    #output layer with softmax probability function
    model.add(Dense(num_of_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    filepath = "C:/Users/Saurabh/Documents/AI/Hindi-Recg/devanagari_model.h5"
    checkpoint1 = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    #checkpoint2 = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    #verbose is basically how do you want to 'see' the training progress for each epoch.
    #We are saving the best only and the criteria for best is max
    callbacks_list = [checkpoint1]

    return model, callbacks_list


x = pickle.load(open("C:/Users/Saurabh/Documents/AI/Hindi-Recg/x1.pickle","rb"))
y = pickle.load(open("C:/Users/Saurabh/Documents/AI/Hindi-Recg/y1.pickle","rb"))

y = np.array(y)
y = y.T
trainy = np_utils.to_categorical(y)

imagex = 32
imagey = 32
    
model, callbacks_list = keras_model(imagex, imagey)
hist = model.fit(x, trainy, epochs=8, batch_size=64, validation_split=0.1, callbacks=callbacks_list)
#scores = model.evaluate(X_test, test_y, verbose=1)
#print("CNN Error: %.2f%%" % (100 - scores[1] * 100))
print_summary(model)

print(hist.history.keys())
# summarize history for accuracy
plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
    
model.save('devanagari_model.h5')

K.clear_session();