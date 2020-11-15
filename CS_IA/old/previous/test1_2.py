import cv2
import math
import pytesseract
import numpy as np
from pythonRLSA import rlsa

def getInfo(docs):
    for doc in docs:
        img = np.array(doc)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(~img, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        avgHeight = sum(cv2.boundingRect(contour)[3] for contour in contours) / len(contours)
        maxHeight = max(cv2.boundingRect(contour)[3] for contour in contours)
        minHeight = min(cv2.boundingRect(contour)[3] for contour in contours)
        print(maxHeight-minHeight)
        

        mask = np.ones(img.shape, dtype="uint8") * 255

        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            if h > avgHeight*2 and h < avgHeight*100:   # ---variable---
                cv2.drawContours(mask, contour, -1, 0)

        [x,y] = mask.shape
        value = max(math.ceil(x/100), math.ceil(y/100)) + 20   # ---variable---
        mask = rlsa.rlsa(mask, True, False, value)
        
        #---------- DISPLAY ----------#
        '''
        cv2.imshow("mask", mask)
        cv2.waitKey(0)
        '''
        #----------/DISPLAY ----------#

        _, thresh = cv2.threshold(~mask, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


        '''


'''

        
        


        
        min_x = img.shape[1]
        min_y = img.shape[1]
        max_x = 0
        max_y = 0
        allRect = []
        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            
            if w > 0.2*img.shape[1] and w < 0.9*img.shape[1]:
                
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if (x+w) > max_x:
                    max_x = (x+w)
                if (y+h) > max_y:
                    max_y = (y+h)
                
        title_region = img[min_y-10:max_y+10,min_x-10:max_x+10]   # ---variable---
        mask[min_y-20:max_y+20,min_x-20:max_x+20] = 255


        #---------- DISPLAY ----------#
        
        cv2.imshow("title region", title_region)
        cv2.waitKey(0)


        title = pytesseract.image_to_string(title_region).replace("\n"," ")
        print(title)


        #----------/DISPLAY ----------#

        # ----------/title ---------- #



        # ---------- author ---------- #


        _, thresh = cv2.threshold(~mask, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            allRect.append([x,y,w,h])

            
        allRect.reverse()

        frequent = []
        dic_counter = {}
        last_counted = -1
        previous = -1
        for rect in allRect:
            
            rect_y = rect[1]
            if rect_y == last_counted:
                pass
            elif rect_y == previous or rect_y - 1 == previous:
                rect_y = last_counted
            else:
                last_counted = rect_y 
            previous = rect[1]

            if rect_y in dic_counter:
                dic_counter[rect_y] += 1
            else:
                dic_counter[rect_y] = 1
            if dic_counter[rect_y] > 2 and not (rect_y in frequent):
                frequent.append(rect_y)

        y_upper = frequent[0]
        y_lower = int(y_upper + 37)
        author = img[y_upper:y_lower,]
        cv2.imshow("author", author)
        cv2.waitKey(0)
        #cv2.imshow("author", author)
        #cv2.waitKey(0)
        author = pytesseract.image_to_string(author).replace("\n"," ")
        print(author)

        #cv2.destroyAllWindows()
