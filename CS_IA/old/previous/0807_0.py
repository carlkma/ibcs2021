import cv2
import math
import numpy as np
from pythonRLSA import rlsa

img = cv2.imread("page_3.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(img, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

count = 1
totalh = 0
for contour in contours:
    [x,y,w,h] = cv2.boundingRect(contour)
    #print(cv2.boundingRect(contour)[3])
    totalh += h
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 1)
    count+=1
avg = totalh/count
print(totalh)
asdf = sum(cv2.boundingRect(contour)[3] for contour in contours)
print(asdf)
cv2.imshow('img', img)
cv2.waitKey(0)
mask = np.ones(img.shape[:2], dtype="uint8") * 255

for c in contours:
    
    [x,y,w,h] = cv2.boundingRect(c)
    if h>avg*2 and h<avg*100:
        cv2.drawContours(mask, [c], -1, 0 , -1)

x,y = mask.shape
value = max(math.ceil(x/100),math.ceil(y/100))+20
mask = rlsa.rlsa(mask, True, False, value)


ret, thresh = cv2.threshold(~mask, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


mask2 = np.ones(img.shape, dtype="uint8") * 255

minx = 9999999
miny = 9999999
maxx = 0
maxy = 0


for contour in contours[2:-1]:
    
    [x,y,w,h] = cv2.boundingRect(contour)
    #cv2.drawContours(mask2, contour, -1, 0 , -1)

    if w>0.2*img.shape[1]:

        if x < minx:
            minx = x
        if y < miny:
            miny = y
        temp_maxx = x+w
        temp_maxy = y+h
        if temp_maxx > maxx:
            maxx = temp_maxx
        if temp_maxy > maxy:
            maxy = temp_maxy

        
        title = img[y:y+h,x:x+w]
        mask2[y:y+h,x:x+w] = title
        img[y:y+h,x:x+w]  =255
        mask[y:y+h,x:x+w] = 255
        

cv2.rectangle(mask2,(minx,miny),(maxx,maxy),(0,255,0),10)
       
ret, thresh = cv2.threshold(mask, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(mask,contours,-1,(0,255,0),1,hierarchy=hierarchy[0])
mask3 = np.ones(img.shape, dtype="uint8") * 255

good = []
for c in contours:
    
    [x,y,w,h] = cv2.boundingRect(c)
    good.append([x,y,w,h])
    if h>avg*2 and h<avg*100 or True:
        cv2.drawContours(mask3, [c], -1, 127 , -1)
        print([x,y,w,h])
        cv2.rectangle(mask3,(x,y),(x+w,y+h),127)
        imS = cv2.resize(mask3, (500, 500)) 
        cv2.imshow('Image mask', imS)
        cv2.waitKey(0)

good.reverse()
note = []
troll = {}
for a_good in good:
    temp_y = a_good[1]
    if temp_y in troll:
        troll[temp_y] += 1
    else:
        troll[temp_y] = 1
    if troll[temp_y] > 2 and not (temp_y in note):
        note.append(temp_y)
y = note[0]
mask4 = np.ones(img.shape, dtype="uint8") * 255
x = 0
author = img[y-10:y+30,x:]
mask4[y-10:y+30,x:] = author
cv2.imshow('Image mask4', mask4)
cv2.waitKey(0)

cv2.destroyAllWindows()
