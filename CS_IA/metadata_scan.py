import re

def getInfo(file_path, field): # field = [title, publisher, creator, subject, description]
	with open(file_path, 'rb') as raw_file:
		read_file = raw_file.read()

		regex = b'[/]Metadata[\s0-9]*?R'
		pattern = re.compile(regex, re.DOTALL)
		xmp_ref = re.findall(pattern, read_file)
		# list [b'/Metadata 547 0 R', b'/Metadata 603 0 R', ...]
		
		xmp_obj_dict = {}
		for ref in xmp_ref:
			ref = ref.decode()
			ref = ref.replace('/Metadata ', '')
			ref = ref.replace(' R', '')
			ref = str.encode(ref)
			# b'547 0'
			
			regex = b'[^0-9]' + ref + b'[ ]obj.*?endobj'
			pattern = re.compile(regex, re.DOTALL)
			xmp_obj = re.findall(pattern, read_file)
			# list (len=1) [b'<dc:title> \n <rdf:Alt> \n <rdf:li xml:lang="x-default"> Learning efficient logic programs </rdf:li> ...']
			
			if len(xmp_obj) > 0:
				for obj in xmp_obj:
					xmp_obj_dict[ref] = obj

	try:
		file_info = list(xmp_obj_dict.values())[0]
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

print(getInfo("PDF/k002k.pdf","creator"))
