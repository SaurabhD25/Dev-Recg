
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

train_datagen = ImageDataGenerator(featurewise_center=True, rotation_range=25)
i = 0
for x,val in train_datagen.flow_from_directory('Train_set',target_size=(32,32),save_to_dir='Dataset',shuffle=False, class_mode='categorical',save_prefix='N',save_format='jpeg',batch_size=32):
    if(i>9070):
        break
    i+=1
