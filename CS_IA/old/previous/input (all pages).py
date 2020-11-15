import os
from pdf2image import convert_from_path

all_docs = os.listdir()

for docs in all_docs:
    pages = convert_from_path(docs, 500)
    page_num = 0
    for page in pages:
        page_num += 1
        tmp_name = "page_" + str(page_num) + ".jpg"
        page.save(tmp_name,"JPEG")
