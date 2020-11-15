import os
import re
import cv2
import output
import findTitle
import findAuthor
import numpy as np
import pytesseract
from pdf2image import convert_from_path

import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import _thread
import time


def GUI():
    global root, progress1, progress2, lblPg1, lblPg2
    root = tk.Tk()
    root.title("PDF Title Extraction")
    root.geometry("500x500")
    root.resizable(False, False)

    lblIntro = tk.Label(root, text="Welcome!", pady=10)
    lblIntro.pack()

    def btnSelect():
        global directory
        directory = filedialog.askdirectory()
        
        lblDir["text"] = directory
        #lblIntro.pack(in_=top, side=LEFT)

   
    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP,fill=tk.X,padx=10)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)    

    btnSelect = tk.Button(root, text="Select", command=btnSelect)
    btnSelect.pack(in_=top, side=LEFT)
    lblDir = tk.Label(root, text=tk.StringVar())
    lblDir["text"] = "directory with target PDF files"
    lblDir.pack(in_=top, side=LEFT)
                         
    lblPg1 = tk.Label(root, text=tk.StringVar())
    lblPg1.pack(pady=10)
    lblPg1["text"] = "Process #1: PDF to image"

    
    progress1 = ttk.Progressbar(root, orient = HORIZONTAL, length = 500, mode = "determinate") 
    progress1.pack(fill=tk.X, padx=10)

    lblPg2 = tk.Label(root, text=tk.StringVar())
    lblPg2.pack(pady=10)
    lblPg2["text"] = "Process #2: image to information"

    
    progress2 = ttk.Progressbar(root, orient = HORIZONTAL, length = 500, mode = "determinate") 
    progress2.pack(fill=tk.X, padx=10,pady=10)

    

    def btnConfirm():
       _thread.start_new_thread(main, ())
    btnConfirm = tk.Button(root, text="Confirm", command=btnConfirm)
    btnConfirm.pack(pady=10, fill=tk.X)


    listbox = Listbox(bottom, bg="white")
    listbox.pack(fill=tk.X, pady=10, padx=10)
    
    btnExit = tk.Button(bottom, text="Exit", command=root.destroy)
    btnExit.pack(fill=tk.X, side=BOTTOM, padx=10, pady=20)

    root.mainloop()


def main():
    global progress1, progress2, lblPg1, lblPg2
    docs = []
    file_name = []
    info = []
    global directory

    count = 0
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            page = convert_from_path(file)[0]
            #page.save("asdf.jpg","JPEG")
            docs.append(page)
            file_name.append(file)
            #break
        count+=1
        val = count/len(os.listdir(directory)) * 100
        progress1["value"] = val
        lblPg1["text"] = "Converting PDF to image, Progress: " + str(int(val)) + "%"
        print(count/len(os.listdir(directory)) * 100)

    progress1["value"] = 100
    lblPg1["text"] = "Converting PDF to image, Progress: 100%"
    count = 0
    for page in docs:
        image = np.array(page)
        title_rect = findTitle.findTitle(image)
        if title_rect == None:
            title = "N/A"
        else:
            (x,y,w,h) = title_rect
            title = pytesseract.image_to_string(image[y:y+h,x:])
            title = re.sub(r"[^a-zA-Z0-9 &,;:-]+", " ", title)
            title = re.sub(r"\s\s+", " ", title)
            title = re.sub(r"\s,", ",", title)
            #cv2.rectangle(image, title_rect, (0,255,0), 5)
            #cv2.imshow("title", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))

        author_rect = findAuthor.findAuthor(image, title_rect)
        if author_rect == None:
            author = "N/A"
        else:
            (x,y,w,h) = author_rect
            author = pytesseract.image_to_string(image[y:y+h,x:])
            author = re.sub(r"[^a-zA-Z &,;:-]+", " ", author)
            author = re.sub(r"\s\s+", " ", author)
            author = re.sub(r"\s(,|-|&)", ",", author)
            author = author.strip()
            #cv2.rectangle(image, author_rect, (0,255,0), 5)
            #cv2.imshow("author", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))

        info.append([title,author])
        count+=1
        val = count/len(docs) * 100
        progress2["value"] = val
        lblPg2["text"] = "Converting image to information, Progress: " + str(int(val)) + "%"
        output.toHTML(info)
    progress2["value"] = 100
    lblPg2["text"] = "Converting image to information, Progress: 100%"

    


if __name__ == '__main__':
    _thread.start_new_thread(GUI, ())
    
