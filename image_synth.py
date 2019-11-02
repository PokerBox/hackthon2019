import cv2
import os
import random

background_path = 'background/'
background_list = os.listdir(background_path) 
butt_path = 'butts/'
butt_list = os.listdir(butt_path)
synth_path = 'synth/'

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
	"""
	@brief      Overlays a transparant PNG onto another image using CV2
	
	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
	
	@return     Background image with overlay on top
	"""
	
	bg_img = background_img.copy()
	
	if overlay_size is not None:
		img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

	# Extract the alpha mask of the RGBA image, convert to RGB 
	b,g,r,a = cv2.split(img_to_overlay_t)
	overlay_color = cv2.merge((b,g,r))
	
	# Apply some simple filtering to remove edge noise
	mask = cv2.medianBlur(a,5)

	h, w, _ = overlay_color.shape
	roi = bg_img[y:y+h, x:x+w]

	# Black-out the area behind the logo in our original ROI
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img


for i in range(100):

    bg = cv2.imread(background_path+ background_list[i])

    j = random.randint(0, len(butt_list)-1)
    butt = cv2.imread(butt_path + butt_list[j],-1)

    resize_scale = int(300*random.uniform(0.1, 0.4))
    butt_resize = cv2.resize(butt,(resize_scale,resize_scale))
    x = random.randint(0, 300 - resize_scale)
    y = random.randint(0, 300 - resize_scale)
    print(x,y)
    cv2.imshow('image',overlay_transparent(bg, butt, x, y, (resize_scale,resize_scale)))
    cv2.waitKey(0)






	



