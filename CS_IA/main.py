import os
import re
import sys
import cv2
import output
import webbrowser
import findTitle
import findAuthor
import getMetadata

import numpy as np
import pytesseract
from pdf2image import convert_from_path

import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import _thread
import time

def GUI():
    global root, progressbar, lblProgress, listbox, file_name, info, btnSelect, btnConfirm, btnExport, btnRename, btnExit
    root = tk.Tk()
    
    root.title("PDFriend")
    root.geometry("500x500")
    root.resizable(False, False)

    # Title
    lblIntro = tk.Label(root, text="PDFriend - Here to help with file organization!", font=("Cambria bold",12), pady=20)
    lblIntro.pack()


    # Select (Frame1)
    def btnSelect():
        
        # reset things
        progressbar["value"] = 0
        listbox.delete(0,listbox.size()-1)
        btnExport["state"] = "disabled"
        btnRename["state"] = "disabled"
        lblDir["text"] = "directory with target PDF files"
        lblProgress["text"] = "Progress: 0%"
        
        global directory
        directory = filedialog.askdirectory()
        if directory != "":
            if len(directory) < 35:
                lblDir["text"] = directory
            else:
                lblDir["text"] = "..." + directory[-32:]
            btnConfirm["state"] = "normal"
        else:
            lblDir["text"] = "directory with target PDF files"

    frame1 = Frame(root)
    frame1.pack(side="top",fill=tk.X,padx=10)

    btnSelect = tk.Button(root, text="Select", command=btnSelect, width=15)
    btnSelect.pack(in_=frame1, side=LEFT)
    
    lblDir = tk.Label(root, font=("Consolas",8),text=tk.StringVar())
    lblDir["text"] = "directory with target PDF files"
    lblDir.pack(in_=frame1, side=LEFT)

    # Confirm & others
    def btnConfirm():
        btnSelect["state"] = "disabled"
        btnConfirm["state"] = "disabled"
        btnExport["state"] = "disabled"
        btnRename["state"] = "disabled"
        _thread.start_new_thread(main, ())
        
    btnConfirm = tk.Button(root, text="Confirm", command=btnConfirm)
    btnConfirm.pack(padx=10,pady=10, fill=tk.X)

    # Progress (Frame2)
    frame2 = Frame(root)
    frame2.pack(fill=BOTH,pady=15)
                         
    lblProgress = tk.Label(frame2, text=tk.StringVar())
    lblProgress.pack(in_=frame2)
    lblProgress["text"] = "Progress: 0%"
    
    progressbar = ttk.Progressbar(frame2, orient = HORIZONTAL, length = 500, mode = "determinate") 
    progressbar.pack(in_=frame2,fill=tk.X, padx=10)

    # Listbox (Frame3)
    frame3 = Frame(root)
    frame3.pack(fill=BOTH,padx=10,pady=10)
    scrollbary = Scrollbar(frame3, orient=VERTICAL)
    scrollbarx = Scrollbar(frame3, orient=HORIZONTAL)
    listbox = Listbox(frame3, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
    scrollbary.config(command=listbox.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=listbox.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)


    # Buttons (Frame4)
    frame4 = Frame(root)
    frame4.pack(fill=tk.X,padx=10)
    
    def btnExit():
        root.destroy()
        sys.exit()
        
        
    btnExit = tk.Button(frame4, text="Exit", command=btnExit, width=15)
    btnExit.pack(in_=frame4, side=LEFT)
    
    def btnExport():
        
        export_directory = filedialog.askdirectory()
        if export_directory != "":
            output.toHTML(info, export_directory)
            messagebox.showinfo(title="Success!", message="Successfully exported!")
        
    btnExport = tk.Button(frame4, text="Export", command=btnExport, width=15)
    btnExport.pack(in_=frame4, side=RIGHT)

    def btnRename():

        status = output.rename(file_name, info, directory)
        if status == "%$OK":
            messagebox.showinfo(title="Success", message="Successfully renamed!")
        else:
            messagebox.showinfo(title="Error", message="Something went wrong when renaming the file " + status + ". Do you have it opened using another application?")
    btnRename = tk.Button(frame4, text="Rename", command=btnRename, width=15)
    btnRename.pack(in_=frame4, side=RIGHT, padx=10)
    
    btnConfirm["state"] = "disabled"
    btnExport["state"] = "disabled"
    btnRename["state"] = "disabled"

    def viewDoc(link):
        if os.path.exists(link):
            webbrowser.open_new("file://" + link)
        else:
            messagebox.showinfo(title="Error", message="The documentation is currently unavailable (to be completed)")

    lblInfo = tk.Label(root, font=("Cambria",8),text="IBCS INTERNAL ASSESSMENT - Copyright (c) 2021 Carl Ma - CLICK TO VIEW DOCUMENTATION")
    lblInfo.pack(side="bottom", fill="x")
    
    lblInfo.bind("<Button-1>", lambda e: viewDoc(os.getcwd() + "\documentation.html"))

    root.mainloop()
    



def main():
    global progressbar, lblProgress, listbox, file_name, info, btnSelect, btnConfirm, btnExport, btnRename, btnExit
    docs = []
    info = []
    file_name = []
    global directory

    count = 0
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            
            count+=1
            val = count/len(os.listdir(directory)) * 100
            progressbar["value"] = val
            lblProgress["text"] = "Progress: " + str(int(val)) + "%"
            
            file_name.append(file)
            file = directory + "//" + file
            title = getMetadata.getInfo(file, "title")
            author = getMetadata.getInfo(file, "creator")
            keywords = getMetadata.getInfo(file, "subject")
            publisher = getMetadata.getInfo(file, "publisher")
            description = getMetadata.getInfo(file, "description")
            
            if title != None or author != None:
                
                info.append([title,author,keywords,publisher,description,file])
                listbox.insert(END, str(count)+ " "+title)
                listbox.insert(END, "")
                continue

            try:
                page = convert_from_path(file)[0]
            except ValueError:
                print("error")
                continue
            image = np.array(page)

            # ---------- findTitle ---------- # 
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

            # ---------- findAuthor ---------- # 
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

            info.append([title,author,"","","",file])
            listbox.insert(END, str(count)+ " "+title)
            listbox.insert(END, "")


    progressbar["value"] = 100
    lblProgress["text"] = "Progress: 100%"
    messagebox.showinfo(title="Success!", message="Successfully extracted!")
    count = 0
    btnExport["state"] = "normal"
    btnRename["state"] = "normal"
    btnSelect["text"] = "Reselect"
    btnSelect["state"] = "normal"

if __name__ == '__main__':
    GUI()
