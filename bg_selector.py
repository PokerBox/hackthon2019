import cv2
import os
import random

image_path = 'D:/Downloads/unlabeled2017/'
image_list = os.listdir(image_path)
dest_path = 'background/'


amount = 3000

for i in range(amount-1):
    image = cv2.imread(image_path + image_list[i])
    image = cv2.resize(image,(300,300))
    # compression_params = [cv2.IMWRITE_PNG_COMPRESSION, 9] 
    cv2.imwrite(dest_path+str(i)+'.png', image)