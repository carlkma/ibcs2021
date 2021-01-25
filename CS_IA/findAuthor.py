import cv2
import math
import numpy as np
from pythonRLSA import rlsa

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
