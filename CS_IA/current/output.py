import os
def toHTML(info, export_directory):

    with open(export_directory + "/index.html", "w") as file:
        file.write("<!DOCTYPE html> <html> <head> <title>Documents</title> All Documents </head> <body>")
        file.write("<ol>")
        for item in info:
            file.write("<li>")
            #file.write("<a href=\"" + directory + "\">asdf</a>")
            file.write(item[0])
            file.write("<ul> <li>" + item[1] + "</li> </ul>")
            file.write("</li>")

        file.write("</ol>")
        file.write("</body>")

def rename(file_name, info, directory):
    os.chdir(directory)
    for i in range(len(file_name)):
        old_name = file_name[i]
        new_name = info[i][0]
        if len(new_name) > 50:
            new_name = new_name[:50]
        new_name += ".pdf"
        os.rename(old_name, new_name)
