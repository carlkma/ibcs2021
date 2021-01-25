import os
import re
import shutil
def toHTML(documents, directory, export_directory):

    with open(export_directory + "/index.html", "w") as file:
        file.write('''<!DOCTYPE html>
<html>
<head>
<title>Documents</title>
<style>
#documents {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#documents td, #documents th {
  border: 1px solid #ddd;
  padding: 8px;
}

#documents tr:nth-child(even){background-color: #f2f2f2;}

#documents tr:hover {background-color: #ddd;}

#documents th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #02696E;
  color: white;
}
</style>
</head>
<body>

<table id="documents">
  <tr>
    <th width=40%>Title</th>
    <th width=20%>Author</th>
    <th width=20%>Keywords</th>
    <th width=10%>Publisher</th>
    <th width=10%>Remarks</th>
  </tr>''')
        
        
        for document in documents:
            full_path = directory + "//" + document[5]
            if os.path.exists(full_path) == False:
                full_path = directory + "//" + document[6]
            file.write("<tr onclick=\"document.location = \'" + full_path + "\';\">")          
            file.write("<td>" + document[0] + "</td>")
            file.write("<td>" + document[1] + "</td>")
            file.write("<td>" + document[2] + "</td>")
            file.write("<td>" + document[3] + "</td>")
            file.write("<td>" + document[4] + "</td>")
            file.write("</tr>")

        file.write('''</table>
    </body>
    </html>''')

def rename(documents, directory):

    os.chdir(directory)
    postfix = 1
    while os.path.exists(".backup-" + str(postfix)):
        postfix += 1
    os.mkdir(".backup-" + str(postfix))

    for document in documents:
        try:
            shutil.copyfile(document[5], ".backup-" + str(postfix) + "//" + document[5])
        except FileNotFoundError:
            continue
        try:
            os.rename(document[5], document[6])
        except PermissionError:
            if os.path.exists(".backup-" + str(postfix) + "//" + document[5]):
                os.remove(".backup-" + str(postfix) + "//" + document[5])
            if len(os.listdir(".backup-" + str(postfix))) == 0:
                os.rmdir(".backup-" + str(postfix))
            return document[5]
    if len(os.listdir(".backup-" + str(postfix))) == 0:
        os.rmdir(".backup-" + str(postfix))

    return "%$OK"
