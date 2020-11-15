import os
def toHTML(info):

	with open("index.html", "w") as file:
		file.write("<!DOCTYPE html> <html> <head> <title>Documents</title> All Documents </head> <body>")
		file.write("<ol>")
		for item in info:
			file.write("<li>")
			file.write(item[0])
			file.write("<ul> <li>" + item[1] + "</li> </ul>")
			file.write("</li>")

		file.write("</ol>")
		file.write("</body>")

def rename(file_name, info):
	for i in range(len(file_name)):
		old_name = file_name[i]
		new_name = info[i][0]
		if len(new_name) > 50:
			new_name = new_name[:50]
		os.rename(old_name, new_name)

def adjustWidth(string, divided):
        max_char = 70
        if len(string) > max_char:
        
                if string[max_char-1] == " ":
                        divided.append(string[:max_char-1])
                        string = string[max_char:]
                        
                        
                elif string[max_char] == " ":
                        divided.append(string[:max_char])
                        string = string[max_char+1:]
                        
                else:
                        divided.append(string[:max_char]+"-")
                        string = string[max_char:]
                adjustWidth(string, divided)
                        
        else:
                divided.append(string)
        return divided
