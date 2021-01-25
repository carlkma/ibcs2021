import os
import re
import shutil
def toHTML(info, export_directory):

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
        
        
        for item in info:
            temp = []
            for i in range(len(item)-1):
                if item[i] != None:
                    if len(item[i]) <= 300:
                        temp.append(item[i])
                    else:
                        temp.append(item[i][:300])
                else:
                    temp.append("")
            file.write("<tr onclick=\"document.location = \'" + item[5] + "\';\">")            
            file.write("<td>" + temp[0] + "</td>")
            file.write("<td>" + temp[1] + "</td>")
            file.write("<td>" + temp[2] + "</td>")
            file.write("<td>" + temp[3] + "</td>")
            file.write("<td>" + temp[4] + "</td>")
            file.write("</tr>")

        file.write('''</table>
</body>
</html>''')

def rename(file_name, info, directory):
    os.chdir(directory)
    postfix = 1
    while os.path.exists(".backup-" + str(postfix)):
        postfix += 1
    os.mkdir(".backup-" + str(postfix))
    for i in range(len(file_name)):

        try:
            shutil.copyfile(file_name[i], ".backup-" + str(postfix) + "//" + file_name[i])
        except FileNotFoundError:
            continue
        old_name = file_name[i]
        new_name = info[i][0]
        new_name = re.sub(":"," -",new_name)
        new_name = re.sub(r"[^a-zA-Z0-9 _-]+","",new_name).strip()
        if len(new_name) > 50:
            new_name = new_name[:50].strip()
        new_name += ".pdf"
        try:
            os.rename(old_name, new_name)
        except PermissionError:
            if os.path.exists(".backup-" + str(postfix) + "//" + file_name[i]):
                os.remove(".backup-" + str(postfix) + "//" + file_name[i])
            if len(os.listdir(".backup-" + str(postfix))) == 0:
                os.rmdir(".backup-" + str(postfix))
            return file_name[i]
    if len(os.listdir(".backup-" + str(postfix))) == 0:
        os.rmdir(".backup-" + str(postfix))
    return "%$OK"
