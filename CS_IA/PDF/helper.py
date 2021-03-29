from os.path import join
import os
from os import listdir
import random,string

for root in listdir():
    if root.endswith(".pdf"):
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        os.rename(root, x+".pdf")
