import cv2
import math
import pytesseract
import numpy as np
from pythonRLSA import rlsa

image = cv2.imread('page_4.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(image, 127, 255, 0)[1]

contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

avgLetterHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)

mask = np.ones(image.shape, dtype="uint8") * 255

for contour in contours:
    [x,y,w,h] = cv2.boundingRect(contour)
    if h > avgLetterHeight*2 and h < image.shape[0]:   # ---variable---
        cv2.drawContours(mask, contour, -1, 0)

mask = rlsa.rlsa(mask, True, False, 100)

kernel = np.ones((5,5), np.uint8) 
eroded = cv2.erode(mask, kernel, iterations=2)

'''#---------- DISPLAY ----------# 
cv2.imshow("~eroded",cv2.resize(~eroded,(500,500)))
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
		cv2.rectangle(image, (x,y,w,h), (0,255,0),2)
		flag = True
	elif flag:
		x0,y0,w0,h0 = possible_title[i-1]
		x_condition = abs(x0-x) < 10
		y_condition = abs(y0+h0-y) < 10
		if x_condition and y_condition:
			actual_title.append(possible_title[i])
			cv2.rectangle(image, (x,y,w,h), (0,255,0),2)
	else:
		flag = False
'''
x = actual_title[0][0]
y = actual_title[0][1]
x1 = max(x,actual_title[-1][0]) + max(actual_title[0][2],actual_title[-1][2])
y1 = max(y,actual_title[-1][1]) + max(actual_title[0][3],actual_title[-1][3])
cv2.rectangle(image, (x,y,x1,y1), (0,255,0),2)'''
print(actual_title)
cv2.imshow("image", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))
cv2.waitKey()