import cv2
import math
import numpy as np
from pythonRLSA import rlsa

def findTitle(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# ^convert image to grayscale
	thresh = cv2.threshold(image, 127, 255, 0)[1]
	# ^convert image to black and white
	contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	# ^find contour lines in the image
	avgLetterHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)
	# ^define the average letter height as the average height of contour lines
	mask = np.ones(image.shape, dtype="uint8") * 255
	# ^create a blank white image mask for use later


	# TO DELETE: header and/or header line, if present
	for contour in contours:
	    [x,y,w,h] = cv2.boundingRect(contour)
	    to_delete = h < avgLetterHeight and w > 0.75* image.shape[1] and y < 0.5* image.shape[0]
	    # HOW TO FIND THE HEADER LINE?
    	# - height smaller than average letter height
    	# - width larger than 75% of document width
    	# - positioned at top half of document
	    
	    if to_delete:
	    	image[0:y,] = 255
	    	# ^remove (whiten) everything above header line
	    	break

	thresh = cv2.threshold(image, 127, 255, 0)[1]
	contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	# ^again, find contour lines in the modified image
	
	# TO KEEP: large-font characters
	for contour in contours:
		[x,y,w,h] = cv2.boundingRect(contour)
		# HOW TO IDENTIFY LARGE-FONT CHARACTERS?
		# - height greater than two times the average letter height
		# - height less than the document height
		# ^(to ignore the one contour featuring the document dimensions)
		if h > avgLetterHeight*2 and h < image.shape[0]:
			cv2.drawContours(mask, contour, -1, 0)

	# TO DO: connect close but discrete pixels together, horizontally
	mask = rlsa.rlsa(mask, True, False, image.shape[0]//15)
	# ^use of the external library pythonRLSA
	# RLSA, RUN LENGTH SMOOTHING ALGORITHM
	#(vertical, horizontal)

	# TO DO: Inflate the pixels to make the blocks even more distinguishable
	kernel = np.ones((image.shape[0]//300,image.shape[0]//200), np.uint8) 
	eroded = cv2.erode(mask, kernel, iterations=2)
	# ^use of the external library opencv

	'''#---------- DISPLAY ----------# 
	cv2.imshow("~eroded",cv2.resize(~eroded,(image.shape[1]//2,image.shape[0]//2)))
	cv2.waitKey()
	'''#----------/DISPLAY ----------# 

	contours = cv2.findContours(~eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgBlockHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)
	# ^again, find contour lines and average block height in the modified image mask
	
	possible_title = []
	actual_title = []
	for contour in contours:
	    x,y,w,h = cv2.boundingRect(contour)
		# WHICH BLOCK TO SELECT AS POSSIBLE TITLE REGION:
		# - Horizontal position less thatn 25% of document width
		# - Vertical position less than 25% of document width
		# - width larger than 25% of document width
		# - height larger than average block height
	    if x < image.shape[1]/4 and y < image.shape[0]/4 and w > image.shape[1]/4 and h > avgBlockHeight:
	    	possible_title.append([x,y,w,h])

	possible_title.reverse()
	# reverse nesscary since contours are initially found from bottom to top 

	# TO DO: consider titles that span over multiple lines
	# understanding of specifics not required
	flag = False
	for i in range(len(possible_title)):
		x,y,w,h = possible_title[i]
		if i == 0:
			actual_title.append(possible_title[i])
			flag = True
		elif flag:
			x0,y0,w0,h0 = possible_title[i-1]
			x_condition = abs(x0-x) < 10
			y_condition = abs(y0+h0-y) < 15
			if x_condition and y_condition:
				actual_title.append(possible_title[i])
			else:
				flag = False
				break
		else:
			flag = False
			break
			
	if actual_title == []:
		return None

	# return the predicted title region
	x = min(each[0] for each in actual_title)
	y = actual_title[0][1]
	w = max(each[2] for each in actual_title)
	h = actual_title[-1][1] + actual_title[-1][3] - y
	return (x,y,w,h)

def findAuthor(image,title_rect):
	if title_rect != None:
		(x,y,w,h) = title_rect
		image[0:y+h,0:x+w] = 255
		
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(image, 127, 255, 0)[1]
	contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgLetterHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)
	mask = np.ones(image.shape, dtype="uint8") * 255

	for contour in contours:
	    [x,y,w,h] = cv2.boundingRect(contour)
	    to_delete = h < avgLetterHeight and w > 0.75* image.shape[1] and y < 0.5* image.shape[0]

	    if to_delete:
	    	image[0:y,] = 255
	    	break

	thresh = cv2.threshold(image, 127, 255, 0)[1]
	contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

	for contour in contours:
		[x,y,w,h] = cv2.boundingRect(contour)
		if h > avgLetterHeight*1 and h < image.shape[0]:
			cv2.drawContours(mask, contour, -1, 0)

	mask = rlsa.rlsa(mask, True, False, image.shape[0]//15)
	kernel = np.ones((image.shape[0]//500,image.shape[0]//200), np.uint8) 
	eroded = cv2.erode(mask, kernel, iterations=2)

	'''#---------- DISPLAY ----------# 
	cv2.imshow("~eroded",cv2.resize(~eroded,(image.shape[1]//2,image.shape[0]//2)))
	cv2.waitKey()
	'''#----------/DISPLAY ----------# 

	contours = cv2.findContours(~eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgBlockHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)

	possible_author = []
	actual_author = []
	for contour in contours:
	    x,y,w,h = cv2.boundingRect(contour)
	    if (True or x < image.shape[1]/4) and y < image.shape[0]/2 and w > image.shape[1]/4:
	    	possible_author.append([x,y,w,h])

	possible_author.reverse()
	flag = False
	for i in range(len(possible_author)):
		x,y,w,h = possible_author[i]
		if i == 0:
			actual_author.append(possible_author[i])
			flag = True
		elif flag:
			x0,y0,w0,h0 = possible_author[i-1]
			y_condition = abs(y0+h0-y) < 3
			if y_condition:
				actual_author.append(possible_author[i])
			else:
				flag = False
				break
		else:
			flag = False
			break

	if actual_author == []:
		return None

	x = min(each[0] for each in actual_author)
	y = actual_author[0][1]
	w = image.shape[1] - x
	h = actual_author[-1][1] + actual_author[-1][3] - y
	return (x,y,w,h)