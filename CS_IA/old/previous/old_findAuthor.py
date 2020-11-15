import cv2
import math
import numpy as np
from pythonRLSA import rlsa
import findTitle

def findAuthor(image,title_rect):
	if title_rect != None:
		(x,y,w,h) = title_rect
		image[0:y+h,0:x+w] = 255

	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(image, 127, 255, 0)[1]
	contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgLetterHeight = sum(cv2.boundingRect(contour)[3] for contour in contours[len(contours)//2:]) / len(contours)
	mask = np.ones(image.shape, dtype="uint8") * 255

	for contour in contours:
	    [x,y,w,h] = cv2.boundingRect(contour)
	    if h > avgLetterHeight*2 and h < image.shape[0]:   # ---variable---
	        cv2.drawContours(mask, contour, -1, 0)

	mask = rlsa.rlsa(mask, True, False, image.shape[0]//15)
	kernel = np.ones((image.shape[0]//500,image.shape[0]//200), np.uint8) 
	eroded = cv2.erode(mask, kernel, iterations=2)

	#---------- DISPLAY ----------# 
	cv2.imshow("~eroded Author",cv2.resize(~eroded,(500,500)))
	cv2.waitKey()
	#----------/DISPLAY ----------# 

	contours = cv2.findContours(~eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
	avgBlockHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)

	possible_title = []
	actual_title = []
	for contour in contours:
	    x,y,w,h = cv2.boundingRect(contour)
	    if (True or x < image.shape[1]/4) and y < image.shape[0]/2 and (True or w > image.shape[1]/4) and (True or h > avgBlockHeight):
	    	possible_title.append([x,y,w,h])
	    	#print(possible_title)

	possible_title.reverse()
	flag = False
	for i in range(len(possible_title)):
		x,y,w,h = possible_title[i]
		if i == 0:
			actual_title.append(possible_title[i])
			flag = True
		elif flag:
			x0,y0,w0,h0 = possible_title[i-1]
			#x_condition = abs(x0-x) < 10
			y_condition = abs(y0+h0-y) < avgLetterHeight
			if y_condition:
				actual_title.append(possible_title[i])
			else:
				flag = False
				break
		else:
			flag = False
			break
		#print(possible_title)
	if actual_title == []:
		return None
	x = min(each[0] for each in actual_title)
	#x = 0
	y = actual_title[0][1]
	#w = max(each[2] for each in actual_title)
	w = image.shape[1] - x
	h = actual_title[-1][1] + actual_title[-1][3] - y
	return (x,y,w,h)


'''# --- testing --- #
for i in range(2,8):

image = cv2.imread('asdf.jpg')
title_rect = new_titledone.findTitle(image)
cv2.rectangle(image, title_rect, (0,255,0), 5)
cv2.imshow("title", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))

author_rect = findAuthor(image, title_rect)
cv2.rectangle(image, author_rect, (0,255,0), 5)
cv2.imshow("author", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))
cv2.waitKey()
'''
