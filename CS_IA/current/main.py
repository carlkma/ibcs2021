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
from tkinter import ttk, filedialog, messagebox
import _thread
import time


def GUI():
    global root, progress1, progress2, lblPg1, lblPg2, listbox, file_name, info, btnSelect, btnConfirm, btnExport, btnRename
    
    root = tk.Tk()
    root.title("PDF Title Extraction")
    root.geometry("1000x500")
    root.resizable(False, False)

    lblIntro = tk.Label(root, text="Welcome!", pady=10)
    lblIntro.pack()

    def btnSelect():
        global directory
        directory = filedialog.askdirectory()
        if directory != "":
            lblDir["text"] = directory
            btnConfirm["state"] = "normal"
        else:
            lblDir["text"] = "directory with target PDF files"
        #lblIntro.pack(in_=frame1, side=LEFT)

   
    frame1 = Frame(root)
    frame1.pack(side="top",fill=tk.X,padx=10)

    btnSelect = tk.Button(root, text="Select", command=btnSelect, width=15)
    btnSelect.pack(in_=frame1, side=LEFT)
    lblDir = tk.Label(root, text=tk.StringVar())
    lblDir["text"] = "directory with target PDF files"
    lblDir.pack(in_=frame1, side=LEFT)
                         
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
        btnSelect["state"] = "disabled"
        btnConfirm["state"] = "disabled"
        btnExport["state"] = "disabled"
        btnRename["state"] = "disabled"
        _thread.start_new_thread(main, ())
        
    btnConfirm = tk.Button(root, text="Confirm", command=btnConfirm)
    btnConfirm.pack(padx=10,pady=10, fill=tk.X)

    frame2 = Frame(root)
    frame2.pack(fill=BOTH,padx=10)
    scrollbar = Scrollbar(frame2, orient=VERTICAL)
    listbox = Listbox(frame2, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)

    listbox.insert(END, "All PDFs")
    listbox.insert(END, "")
    listbox.insert(END, "")

    frame3 = Frame(root)
    frame3.pack(fill=tk.X,padx=10)
    
    def btnRestart():
        #listbox clear
        listbox.delete(3,listbox.size()-1)
        btnSelect["state"] = "normal"
        btnConfirm["state"] = "disabled"
        btnExport["state"] = "disabled"
        btnRename["state"] = "disabled"
        lblDir["text"] = "directory with target PDF files"
        lblPg1["text"] = "Process #1: PDF to image"
        lblPg2["text"] = "Process #2: image to information"
        progress1["value"] = 0
        progress2["value"] = 0
        
    btnRestart = tk.Button(frame3, text="Restart", command=btnRestart, width=15)
    btnRestart.pack(in_=frame3, side=LEFT)
    
    def btnExport():
        
        export_directory = filedialog.askdirectory()
        if export_directory != "":
            output.toHTML(info, export_directory)
            messagebox.showinfo(title="Success!", message="Successfully exported!")
        
    btnExport = tk.Button(frame3, text="Export", command=btnExport, width=15)
    btnExport.pack(in_=frame3, side=RIGHT)

    def btnRename():
        output.rename(file_name, info, directory)
        messagebox.showinfo(title="Success!", message="Successfully renamed!")
    btnRename = tk.Button(frame3, text="Rename", command=btnRename, width=15)
    btnRename.pack(in_=frame3, side=RIGHT, padx=10)
    
    btnConfirm["state"] = "disabled"
    btnExport["state"] = "disabled"
    btnRename["state"] = "disabled"

    root.mainloop()


def main():
    global progress1, progress2, lblPg1, lblPg2, listbox, file_name, info, btnSelect, btnConfirm, btnExport, btnRename
    docs = []
    info = []
    file_name = []
    global directory

    count = 0
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            page = convert_from_path(file)[0]
            docs.append(page)
            file_name.append(file)
            #break
        count+=1
        val = count/len(os.listdir(directory)) * 100
        progress1["value"] = val
        lblPg1["text"] = "Converting PDF to image, Progress: " + str(int(val)) + "%"

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
        listbox.insert(END, str(count)+ " "+title)
        listbox.insert(END, "")
    progress2["value"] = 100
    lblPg2["text"] = "Converting image to information, Progress: 100%"
    messagebox.showinfo(title="Success!", message="Successfully extracted!")
    btnExport["state"] = "normal"
    btnRename["state"] = "normal"
    

    


if __name__ == '__main__':
    _thread.start_new_thread(GUI, ())
    
