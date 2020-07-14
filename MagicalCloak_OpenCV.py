#!/usr/bin/env python
# coding: utf-8

# In[8]:


#_Importing Important Libraries
import cv2
import time
import numpy as np


# In[9]:


print(cv2.__version__)


# In[10]:


#IF you would like to save the Video recorded by webcam
fourcc= cv2.VideoWriter_fourcc(*'XVID')
vout = cv2.VideoWriter('video.avi',fourcc,20.0,(640,480)) 


# In[11]:


#Capturing Video (frames)
cap= cv2.VideoCapture(0)
#Waiting for Webcam to work properly
time.sleep(4)


# In[12]:


count=0
backgroundimg=0
#Capturing  Sample Background  Images
for img in range(60):
    _ , backgroundimg = cap.read()
#print(backgroundimg)
backgroundimg=np.flip(backgroundimg, axis=1)


# In[13]:


while( cap.isOpened() ):
    status , testimg = cap.read()
    if not status:
        print("Some error occured")
        break
    count+=1
    img = np.flip(testimg ,axis = 1)
    
    #Converting Colour from RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Now Selecting the mask for Cloth (means selecting lower and upper mask for red colour)
    #Lower 10% Red mask
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    #Upper 10% Red mask
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    #For Getting Mask Value from both. Doing 'Or' Operation Using '+' sign
    mask1 = mask1 + mask2
    
    #Defining Kernal
    kernal = np.ones((3,3),np.uint8)
    
    #Image Opening and Dilating the Image using cv2 inbuilt 
    #functions for both masks
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernal)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, kernal)
    
    #Now this 'bitwise_not' and 'bitwise_and' operations will
    #segment out red colour from the frame
    mask2 = cv2.bitwise_not(mask1)
    
    #Saving the Redpart Only
    result_r = cv2.bitwise_and(img , img, mask=mask2)
    
    #Saving Other Part except Redpart Portion
    result_b = cv2.bitwise_and(backgroundimg, backgroundimg, mask=mask1) 
    
    #'addWeighted' is a built in function of OpenCV used to merge
    #two images with best fit
    
    finalOp= cv2.addWeighted(result_r,1,result_b,1,0)
    #Writing Our Output to video
    vout.write(finalOp)
    cv2.imshow('OP_Magical_Cloak',finalOp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
vout.release()
cv2.destroyAllWindows()
print(str(count), 'Frames Captured')


# In[ ]:




