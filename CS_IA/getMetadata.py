"""
Modified based on PDF Metadata at
https://gitlab.com/nxl4/pdf-metadata/-/blob/master/pdf-metadata.py
LICENSE TERMS APPLY

"""
import re

class BinaryPdfForensics:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_info_ref(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            regex = b'[/]Info[\s0-9]*?R'
            pattern = re.compile(regex, re.DOTALL)
            info_ref = re.findall(pattern, read_file)
            info_ref = de_dupe_list(info_ref)
            if len(info_ref) == 0:
                info_ref_exists = False
            else:
                info_ref_exists = True
            return (info_ref_exists, info_ref)

    def get_xmp_ref(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            regex = b'[/]Metadata[\s0-9]*?R'
            pattern = re.compile(regex, re.DOTALL)
            xmp_ref = re.findall(pattern, read_file)
            xmp_ref = de_dupe_list(xmp_ref)
            if len(xmp_ref) == 0:
                xmp_ref_exists = False
            else:
                xmp_ref_exists = True
            return (xmp_ref_exists, xmp_ref)


    def get_info_obj(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            info_ref_tuple = BinaryPdfForensics.get_info_ref(self)
            info_obj_dict = {}
            for ref in info_ref_tuple[1]:
                info_ref = ref.decode()
                info_ref = info_ref.replace('/Info ', '') \
                                   .replace(' R', '')
                info_ref = str.encode(info_ref)
                regex = b'[^0-9]' + info_ref + b'[ ]obj.*?endobj'
                pattern = re.compile(regex, re.DOTALL)
                info_obj = re.findall(pattern, read_file)
                info_obj = de_dupe_list(info_obj)
                if len(info_obj) > 0:
                    for obj in info_obj:
                        info_obj_dict[ref] = obj
            if len(info_obj_dict) == 0:
                info_obj_exists = False
            else:
                info_obj_exists = True
            return (info_obj_exists, info_obj_dict)


    def get_xmp_obj(self):
        
        with open(self.file_path, 'rb') as raw_file:
            read_file = raw_file.read()
            xmp_ref_tuple = BinaryPdfForensics.get_xmp_ref(self)
            xmp_obj_dict = {}
            for ref in xmp_ref_tuple[1]:
                xmp_ref = ref.decode()
                xmp_ref = xmp_ref.replace('/Metadata ', '') \
                                 .replace(' R', '')
                xmp_ref = str.encode(xmp_ref)
                regex = b'[^0-9]' + xmp_ref + b'[ ]obj.*?endobj'
                pattern = re.compile(regex, re.DOTALL)
                xmp_obj = re.findall(pattern, read_file)
                xmp_obj = de_dupe_list(xmp_obj)
                if len(xmp_obj) > 0:
                    for obj in xmp_obj:
                        xmp_obj_dict[ref] = obj
            if len(xmp_obj_dict) == 0:
                xmp_obj_exists = False
            else:
                xmp_obj_exists = True
            return (xmp_obj_exists, xmp_obj_dict)


    def gen_report(self):
        info_ref = BinaryPdfForensics.get_info_ref(self)
        info_obj = BinaryPdfForensics.get_info_obj(self)

        xmp_ref = BinaryPdfForensics.get_xmp_ref(self)
        xmp_obj = BinaryPdfForensics.get_xmp_obj(self)

        
        return info_obj, xmp_obj
            

def de_dupe_list(list_var):
    
    new_list = []
    for element in list_var:
        if element not in new_list:
            new_list.append(element)
    return new_list


new_file = BinaryPdfForensics(file_path="p003p.pdf")
asdf = new_file.gen_report()[1]
#a = asdf.decode("utf-8")
print(asdf)