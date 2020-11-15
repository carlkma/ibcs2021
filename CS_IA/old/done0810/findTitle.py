import cv2
import math
import numpy as np
from pythonRLSA import rlsa

def findTitle(image):
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
		if h > avgLetterHeight*2 and h < image.shape[0]:
			cv2.drawContours(mask, contour, -1, 0)

	mask = rlsa.rlsa(mask, True, False, image.shape[0]//15)
	#(vertical, horizontal)
	kernel = np.ones((image.shape[0]//300,image.shape[0]//200), np.uint8) 
	eroded = cv2.erode(mask, kernel, iterations=2)

	'''#---------- DISPLAY ----------# 
	cv2.imshow("~eroded",cv2.resize(~eroded,(image.shape[1]//2,image.shape[0]//2)))
	cv2.waitKey()
	'''#----------/DISPLAY ----------# 

	contours = cv2.findContours(~eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgBlockHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)
	
	possible_title = []
	actual_title = []
	for contour in contours:
	    x,y,w,h = cv2.boundingRect(contour)
	    if x < image.shape[1]/4 and y < image.shape[0]/4 and w > image.shape[1]/4 and h > avgBlockHeight:
	    	possible_title.append([x,y,w,h])

	possible_title.reverse()
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

	x = min(each[0] for each in actual_title)
	y = actual_title[0][1]
	w = max(each[2] for each in actual_title)
	h = actual_title[-1][1] + actual_title[-1][3] - y
	return (x,y,w,h)