import cv2
import os
from PIL import Image

butt_path = 'D:/Workspace/hackthon2019/butts/'
butt_list = os.listdir(butt_path)

i = 0
for i in range(len(butt_list)):
    image = Image.open(butt_path + butt_list[i])

    fill_color=(255, 255, 255, 0)
    print(image)
    height, width = image.size
    print(height, width)
    size = max(height, width)
    new_image = Image.new('RGBA', (size, size), fill_color)
    new_image.paste(image, (int((size - height) / 2), int((size - width) / 2)))
    new_image = new_image.resize((300,300),Image.LANCZOS)
    new_image.save(butt_path + str(i+1) + '.png')
