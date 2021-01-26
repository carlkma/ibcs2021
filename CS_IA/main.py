print("Preparing the GUI")
print("This will take less than a minute.")
# Imports
import os
import re
import sys
import cv2
import time
import output
import _thread
import webbrowser
import numpy as np
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pdf2image import convert_from_path

#Custom imports
import ocr_scan
import metadata_scan

import ctypes
def hideConsole():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)

def GUI():
    hideConsole()
    global root, progressbar, lblProgress, listbox, documents, btnSelect, btnConfirm, btnExport, btnRename, btnExit
    #documents = [ [title, author, keywords, publisher, remarks, original_name, new_name, status], ... ]

    root = tk.Tk()
    
    root.title("PDFriend")
    root.geometry("500x500")
    root.resizable(False, False)

    #photo = PhotoImage(file="icon.png")
    icon = b'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'
    photo = tk.PhotoImage(data=icon)
    root.iconphoto(False,photo)

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

    frame1 = tk.Frame(root)
    frame1.pack(side="top",fill=tk.X,padx=10)

    btnSelect = tk.Button(root, text="Select", command=btnSelect, width=15)
    btnSelect.pack(in_=frame1, side=tk.LEFT)
    
    lblDir = tk.Label(root, font=("Consolas",8),text=tk.StringVar())
    lblDir["text"] = "directory with target PDF files"
    lblDir.pack(in_=frame1, side=tk.LEFT)

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
    frame2 = tk.Frame(root)
    frame2.pack(fill=tk.BOTH,pady=15)
                         
    lblProgress = tk.Label(frame2, text=tk.StringVar())
    lblProgress.pack(in_=frame2)
    lblProgress["text"] = "Progress: 0%"
    
    progressbar = Progressbar(frame2, orient = tk.HORIZONTAL, length = 500, mode = "determinate") 
    progressbar.pack(in_=frame2,fill=tk.X, padx=10)

    # Listbox (Frame3)
    frame3 = tk.Frame(root)
    frame3.pack(fill=tk.BOTH,padx=10,pady=10)
    scrollbary = tk.Scrollbar(frame3, orient=tk.VERTICAL)
    scrollbarx = tk.Scrollbar(frame3, orient=tk.HORIZONTAL)
    listbox = tk.Listbox(frame3, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
    scrollbary.config(command=listbox.yview)
    scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbarx.config(command=listbox.xview)
    scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


    # Buttons (Frame4)
    frame4 = tk.Frame(root)
    frame4.pack(fill=tk.X,padx=10)
    
    def btnExit():
        root.destroy()
        sys.exit()
        
        
    btnExit = tk.Button(frame4, text="Exit", command=btnExit, width=15)
    btnExit.pack(in_=frame4, side=tk.LEFT)
    
    def btnExport():
        
        export_directory = filedialog.askdirectory()
        if export_directory != "":
            output.toHTML(documents, directory, export_directory)
            documents[0][7] = 1
            messagebox.showinfo(title="Success!", message="Successfully exported!")
        
    btnExport = tk.Button(frame4, text="Export", command=btnExport, width=15)
    btnExport.pack(in_=frame4, side=tk.RIGHT)

    def btnRename():

        status = output.rename(documents, directory)
        if status == "%$OK":
            
            if documents[0][7] == 0:
                messagebox.showinfo(title="Success", message="Successfully renamed!")
            else:
                messagebox.showinfo(title="Success", message="Successfully renamed! But the HTML file you previously exported contains outdated information, you will have to export again.")
        else:
            messagebox.showinfo(title="Error", message="Something went wrong when renaming the file " + status + ". Do you have it opened using another application?")
    btnRename = tk.Button(frame4, text="Rename", command=btnRename, width=15)
    btnRename.pack(in_=frame4, side=tk.RIGHT, padx=10)
    
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
    global progressbar, lblProgress, listbox, documents, btnSelect, btnConfirm, btnExport, btnRename, btnExit
    
    docs = []
    documents = []
    global directory

    count = 0
    for original_name in os.listdir(directory):
        if original_name.endswith(".pdf"):
            
            count+=1
            val = count/len(os.listdir(directory)) * 95
            progressbar["value"] = val
            lblProgress["text"] = "Progress: " + "{:.2f}".format(val) + "%"
            
            
            original_path = directory + "//" + original_name
            title = metadata_scan.getInfo(original_path, "title")
            author = metadata_scan.getInfo(original_path, "creator") or ""
            keywords = metadata_scan.getInfo(original_path, "subject") or ""
            publisher = metadata_scan.getInfo(original_path, "publisher") or ""
            description = metadata_scan.getInfo(original_path, "description") or ""
            
            if title != None:
                new_name = title
                new_name = re.sub(":"," -",new_name)
                new_name = re.sub(r"[^a-zA-Z0-9 _-]+","",new_name).strip()
                if len(new_name) > 50:
                    new_name = new_name[:50].strip()
                new_name += ".pdf"

                documents.append([title,author,keywords,publisher,description,original_name,new_name,0])
                listbox.insert(tk.END, str(count)+ ". "+title)
                listbox.insert(tk.END, "")
                continue
            try:
                wd = sys._MEIPASS
            except AttributeError:
                wd = os.getcwd()
            
            
            try:
                for item in os.listdir(r"."):
                    listbox.insert(tk.END, item)
                listbox.insert(tk.END, "Enter")
                
                page = convert_from_path(pdf_path=original_path)[0]
            except Exception as e:
                listbox.insert(tk.END, e)
                for item in os.listdir(wd):
                    listbox.insert(tk.END, item)
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                
                #a = input()
                continue
            image = np.array(page)
            listbox.insert(tk.END, "JING LEE!")

            # ---------- findTitle ---------- #
            pytesseract.pytesseract.tesseract_cmd = './Tesseract_OCR/tesseract.exe'
            title_rect = ocr_scan.findTitle(image)
            if title_rect == None:
                title = "N/A"
            else:
                (x,y,w,h) = title_rect
                listbox.insert(tk.END, "YAOSI!")
                try:
                    title = pytesseract.image_to_string(image[y:y+h,x:])
                except Exception as e:
                    listbox.insert(tk.END, "shit")
                    listbox.insert(tk.END, e)
                listbox.insert(tk.END, "end!")
                try:
                    title = re.sub(r"[^a-zA-Z0-9 &,;:-]+", " ", title)
                except Exception as e:
                    listbox.insert(tk.END, "shit2")
                    listbox.insert(tk.END, e)
                listbox.insert(tk.END, "end!")
                title = re.sub(r"\s\s+", " ", title)
                title = re.sub(r"\s,", ",", title)
                #cv2.rectangle(image, title_rect, (0,255,0), 5)
                #v2.imshow("title", cv2.resize(image, (image.shape[1]//2,image.shape[0]//2)))
                

            # ---------- findAuthor ---------- # 
            author_rect = ocr_scan.findAuthor(image, title_rect)
            listbox.insert(tk.END, "endauthor!")
            if author_rect == None:
                author = "N/A"
            else:
                (x,y,w,h) = author_rect
                listbox.insert(tk.END, "author tess!")
                author = pytesseract.image_to_string(image[y:y+h,x:])
                author = re.sub(r"[^a-zA-Z &,;:-]+", " ", author)
                author = re.sub(r"\s\s+", " ", author)
                author = re.sub(r"\s(,|-|&)", ",", author)
                author = author.strip()
            
            new_name = title
            new_name = re.sub(":"," -",new_name)
            new_name = re.sub(r"[^a-zA-Z0-9 _-]+","",new_name).strip()
            if len(new_name) > 50:
                new_name = new_name[:50].strip()
            new_name += ".pdf"
            listbox.insert(tk.END, "here!")

            documents.append([title,author,"","","",original_name,new_name,0])
            listbox.insert(tk.END, "almost here!")
            listbox.insert(tk.END, str(count)+ ". "+title)
            listbox.insert(tk.END, "")


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
