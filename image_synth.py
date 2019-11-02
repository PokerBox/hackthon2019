import cv2
import os
import random

background_path = 'background/'
background_list = os.listdir(background_path) 
butt_path = 'butts/'
butt_list = os.listdir(butt_path)
synth_path = 'synth/'


for i in range(10)
    image = cv2.imread(background_path+ image_list[i])
    image = cv2.resize(image,(300,300))

    j = random.randint(0, len(butt_list))
    butt = cv2.imread(butt_path + butt_list[j])
    x = random.randint(0, len(butt_list))

    cv2.imshow('j',image)
    cv2.waitKey(0)


