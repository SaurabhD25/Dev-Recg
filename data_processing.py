import os
import cv2
import numpy as np
import random

dirname = "C:/Users/Saurabh/Documents/AI/Hindi Character Recog using CNN/Train_set"
categories = ["1","2","3","4","5","6","7","8","9","10","11","12",
               "13","14","15","16","17","18","19","20","21","22","23","24",
               "25","26","27","28","29","30","31","32","33","34","35","36",
               "37","38","39","40","41","42","43","44","45","46","47","48"]

training_data = []

def create_training_data():
    for category in categories:
        path = os.path.join(dirname, category)
        class_num = (categories.index(category)) + 1
        print(class_num)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                training_data.append([img_array, class_num])
                
            except Exception as e:
                pass

create_training_data()
print(len(training_data)) 

random.shuffle(training_data)
for sample in training_data[:10]:
    print(sample[1])
    
x1 = []
y1 = []

for features,label in training_data:
    x1.append(features)
    y1.append(label)
    
x1 = np.array(x1).reshape(-1, 32, 32, 1)

import pickle

pickle_out = open("x1.pickle","wb")
pickle.dump(x1, pickle_out)
pickle_out.close()

pickle_out = open("y1.pickle","wb")
pickle.dump(y1, pickle_out)
pickle_out.close()




    
    

        

