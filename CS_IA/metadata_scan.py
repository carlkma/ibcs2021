"""
Modified based on PDF Metadata at
https://gitlab.com/nxl4/pdf-metadata/-/blob/master/pdf-metadata.py
LICENSE TERMS APPLY
"""
import re

class pdfMetadata:

    def __init__(self, file_path):
        self.file_path = file_path


    def get_xmp_ref(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            regex = b'[/]Metadata[\s0-9]*?R'
            pattern = re.compile(regex, re.DOTALL)
            xmp_ref = re.findall(pattern, read_file)
            xmp_ref = remove_duplicates(xmp_ref)
            if len(xmp_ref) == 0:
                xmp_ref_exists = False
            else:
                xmp_ref_exists = True
            return (xmp_ref_exists, xmp_ref)


    def get_xmp_obj(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            xmp_ref_tuple = pdfMetadata.get_xmp_ref(self)
            xmp_obj_dict = {}
            for ref in xmp_ref_tuple[1]:
                xmp_ref = ref.decode()
                xmp_ref = xmp_ref.replace('/Metadata ', '') \
                                 .replace(' R', '')
                xmp_ref = str.encode(xmp_ref)
                regex = b'[^0-9]' + xmp_ref + b'[ ]obj.*?endobj'
                pattern = re.compile(regex, re.DOTALL)
                xmp_obj = re.findall(pattern, read_file)
                xmp_obj = remove_duplicates(xmp_obj)
                if len(xmp_obj) > 0:
                    for obj in xmp_obj:
                        xmp_obj_dict[ref] = obj
            if len(xmp_obj_dict) == 0:
                xmp_obj_exists = False
            else:
                xmp_obj_exists = True
            return (xmp_obj_exists, xmp_obj_dict)


    def gen_report(self):
        xmp_ref = pdfMetadata.get_xmp_ref(self)
        xmp_obj = pdfMetadata.get_xmp_obj(self)
        return xmp_obj
            

def remove_duplicates(list_var):
    
    new_list = []
    for element in list_var:
        if element not in new_list:
            new_list.append(element)
    return new_list


def getInfo(file_path, field): # field = [title, publisher, creator, subject, description]

    new_file = pdfMetadata(file_path=file_path)

    try:
        file_info = list(new_file.gen_report()[1].values())[0]
    except IndexError:
        return None
    except FileNotFoundError:
        return None
    try:
        file_info = file_info.decode("utf-8")
    except UnicodeDecodeError:
        return None
    file_info = re.sub('\s\s+', ' ', file_info)
    
    
    info_start = "<dc:" + field + ">"
    info_end = "</dc:" + field + ">"
    results = file_info[file_info.find(info_start)+len(info_start):file_info.find(info_end)].strip()
    results = re.sub('> <', '><', results)
    in_brackets = False
    endpoints = []
    for i in range(len(results)):
        char = results[i]
        if char == "\n":
            continue
        if char == "<":
            in_brackets = True
        if in_brackets == False and (char != "<" or char != ">"):
            endpoints.append(i)
        if char == ">":
            in_brackets = False
    #results = results[endpoints[0]:endpoints[-1]+1]
    answer = ""
    
    for i in range(len(endpoints)):
        if i>0:
            if endpoints[i] - 1 != endpoints[i-1]:
                answer += ", "
        answer += results[endpoints[i]]
    answer = re.sub(" ,",",",answer)
    if "Adobe" in answer or "Apple" in answer or "Windows" in answer or "TeX" in answer:
        answer = None
    return answer
