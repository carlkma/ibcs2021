from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("PDF Title Extraction")
root.geometry("500x500")



def btnClick():
	directory = filedialog.askdirectory()

btn = Button(root, text="Select", command=btnClick)
btn.pack(side = "top")

progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = "determinate") 

mainloop()