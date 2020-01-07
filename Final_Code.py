# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 15:15:58 2018

@author: Saurabh
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 02:23:33 2018

@author: USER
"""

import tkinter as tk
from PIL import Image, ImageDraw,ImageTk
import numpy as np
import os
import pickle
import cv2
from keras.models import load_model

from playsound import playsound
#This requires internet connection and is quite slow...
s = []
dirname = r"‪D:\Hindi Recg" #path of the directory containing .h5 file
import matplotlib.pyplot as plt

p= '1'
letter_count = {1 : 'क',2:'ख',3:'ग', 4: 'घ',5: 'ङ',6: 'च',7: 'छ', 8:'ज',9:'झ',10:'ञा',11:'ट', 12:'ठ', 13:'ड',14:'ढ',15:'ण',16:'त', 17:'थ', 18:'द', 19:'ध', 20:'न', 21:'प', 22:'फ' ,23:' ब',24:'भ',25:'म', 26:'य',27:'र',28:'ल', 29:'व',30:'श',31:'ष', 32:'स',33:'ह',34:'क्ष',35:'त्र',36:'ज्ञ', 37: 'अ', 38: 'आ', 39: 'इ',40: 'ई',41: 'उ',42: 'ऊ',43: 'ए',44: 'ऐ', 45: 'ओ', 46:'औ',47: 'अं', 48: 'अः' }
def func():
    print("Hello World!")

def recognise(img):
    print(img)
    global p
    img_array = np.array(img)
    
    img_array = cv2.resize(img_array,(32,32))
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img = 255 - img
    cv2.imshow("Processed Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = img.reshape(-1, 32, 32, 1)
    ret, img = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    model = load_model(os.path.join(dirname, "devanagari2.h5")) #append .h5 file name to directory path
    pred_prob = model.predict(img)[0]
    pred_class = list(pred_prob).index(max(pred_prob))
    print(max(pred_prob))
    print(pred_class)
    pred_char = letter_count[pred_class]
    print(pred_char)
    #s.append('a')
    p = pred_char

def next_char():
    s.append(p)
    
def stop():
    global s
    s.append(p)
    s = "".join([x for x in s])  #Copnverts the array into a contigious string
    root.destroy()



class ImageGenerator:
    j = 1
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.parent1 = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.drawing_area=tk.Canvas(self.parent,width=self.sizex,bg = 'black', height=self.sizey)
        self.drawing_area1=tk.Canvas(self.parent1,width=self.sizex,bg = 'white', height=self.sizey)
        
        
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        
        
        self.drawing_area1.place(x=self.posx+200,y=self.posy)
        self.drawing_area1.create_image( 100,100, image = img)
        
        
        
        
        self.button=tk.Button(self.parent,text="Recognise!",width=8,bg='white',command=self.save)
        self.button.place(x=self.sizex/7-20,y=self.sizey+40)
        
        self.button1=tk.Button(self.parent,text="Clear!",width=8,bg='red',command=self.clear)
        self.button1.place(x=(self.sizex/7)+80,y=self.sizey+40)
        
        self.button2=tk.Button(self.parent,text="Next",width=8,bg='green',command=self.clear1)
        self.button2.place(x=(self.sizex/7)+180,y=self.sizey+40)
        
        self.button3=tk.Button(self.parent,text="Done!",width=8,bg='yellow',command=stop)
        self.button3.place(x=(self.sizex/7)+280,y=self.sizey+40)


        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        

    def save(self):
       
        filename = 'Halant/'+str(j)+'.jpg'
        self.image.save(filename)
        print(self.image)
        j += 1
        recognise(self.image)
        r, g, b = (self.image).getpixel((1, 1))
        print(r, g, b)
        
    def clear1(self):
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        next_char()
        
        
    def clear(self):
        
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def b1down(self,event):
        
        self.b1 = "down"
        
    def b1up(self,event):
        
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
       
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=10,fill='white')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,128,0),width=10)

        self.xold = event.x
        self.yold = event.y

if __name__ == "__main__":
    
    root=tk.Toplevel()
    root.wm_geometry("%dx%d+%d+%d" % (400, 300, 10, 10))
    root.title("Devanagari Character Recognition")
    root.config(bg='white')
    i = Image.open( r'C:\Users\Saurabh\Desktop\vit.png')
    img = ImageTk.PhotoImage(i)
    
    
    ImageGenerator(root,10,10)
    
    root.mainloop()
    
    #print("Hello")
    print(s)
    
    temp = input("Do you want to play audio ? Press 1 for yes and 0 for no")
    
    if(temp == '1'):
        filename = r'C:\Users\Saurabh\Desktop\pick_example'
        outfile = open(filename,'wb')
        pickle.dump(s,outfile)
        outfile.close()
        #infile = open(filename,'rb')
        #new_var = pickle.load(infile)
        #infile.close()
        os.system(r"C:\Users\Saurabh\Desktop\audio_output.py")