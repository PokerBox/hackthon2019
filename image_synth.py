import cv2
import os
import random

image_path = 'D:/Downloads/unlabeled2017'
image_list = os.listdir(image_path) 
butt_path = 'D:/Workspace/hackthon2019/butts'
butt_list = os.listdir(butt_path)

i = 0
image = cv2.imread(image_path +'/'+ image_list[i])
image = cv2.resize(image,(300,300))

j = random.randint(0, len(butt_list))
butt = cv2.imread(butt_path +'/'+ butt_list[j])
x = random.randint(0, len(butt_list))

cv2.imshow('j',image)
cv2.waitKey(0)


