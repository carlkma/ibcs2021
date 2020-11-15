import os
import re
import cv2
import output
import findTitle
import findAuthor
import numpy as np
import pytesseract
from pdf2image import convert_from_path

docs = []
file_name = []
info = []

for file in os.listdir(): 
    if file.endswith("ab.pdf"):
        page = convert_from_path(file)[0]
        #page.save("asdf.jpg","JPEG")
        docs.append(page)
        file_name.append(file)
        break

for page in docs:
    image = np.array(page)
    title_rect = findTitle.findTitle(image)
    if title_rect == None:
        title = "N/A"
    else:
        (x,y,w,h) = title_rect
        title = pytesseract.image_to_string(image[y:y+h,x:x+w])
        title = re.sub(r"[^a-zA-Z0-9 &,;:-]+", " ", title)
        title = re.sub(r"\s\s+", " ", title)
        title = re.sub(r"\s,", ",", title)
        cv2.rectangle(image, title_rect, (0,255,0), 5)
        cv2.imshow("title", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))

    author_rect = findAuthor.findAuthor(image, title_rect)
    if author_rect == None:
        author = "N/A"
    else:
        (x,y,w,h) = author_rect
        author = pytesseract.image_to_string(image[y:y+h,x:x+w])
        author = re.sub(r"[^a-zA-Z &,;:-]+", " ", author)
        author = re.sub(r"\s\s+", " ", author)
        author = re.sub(r"\s(,|-|&)", ",", author)
        author = author.strip()
        cv2.rectangle(image, author_rect, (0,255,0), 5)
        cv2.imshow("author", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))

    info.append([title,author])
    print("ok")
    output.toHTML(info)
    #cv2.waitKey()
