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
    global root, progress
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
    #bottom = Frame(root)
    top.pack(side=TOP,fill=tk.X,padx=10)
    #bottom.pack(side=BOTTOM, fill=BOTH, expand=True)    

    btnSelect = tk.Button(root, text="Select", command=btnSelect)
    btnSelect.pack(in_=top, side=LEFT)
    lblDir = tk.Label(root, text=tk.StringVar())
    lblDir["text"] = "Locate the directory with unsorted PDF files"
    lblDir.pack(in_=top, side=LEFT)
                         
    
    progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 500, mode = "determinate") 
    progress.pack(fill=tk.X, padx=10)

    

    def btnConfirm():
       _thread.start_new_thread(main, ())
    btnConfirm = tk.Button(root, text="Confirm", command=btnConfirm)
    btnConfirm.pack(pady=10, fill=tk.X)
    

    btnExit = tk.Button(root, text="Exit", command=root.destroy)
    btnExit.pack(fill=tk.X, side=BOTTOM, padx=10, pady=20)

    root.mainloop()


def main():
    global progress
    docs = []
    file_name = []
    info = []
    count = 0
    global directory
    for file in os.listdir(directory):
        print(file)
        if file.endswith(".pdf"):
            page = convert_from_path(file)[0]
            #page.save("asdf.jpg","JPEG")
            docs.append(page)
            file_name.append(file)
            count+=1
            progress["value"] = count/len(os.listdir("D:/SHSID/IB/Computer Science/IA/program/current/1")) * 100
            #break

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
        print("ok")
        output.toHTML(info)

    progress["value"] = 0


if __name__ == '__main__':
    _thread.start_new_thread(GUI, ())
    
