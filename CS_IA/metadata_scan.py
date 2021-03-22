import re

def getInfo(file_path, field): # field = [title, publisher, creator, subject, description]
	with open(file_path, 'rb') as raw_file:
		read_file = raw_file.read()

		regex = b'[/]Metadata[\s0-9]*?R'
		# NOTE: b'...' refers to a byte literal
		# ^use of regular expressions to find all XMP ref
		pattern = re.compile(regex, re.DOTALL)
		xmp_ref = re.findall(pattern, read_file)
		# Here, xmp_ref is a Python list of all XMP ref, e.g.:
		# list [b'/Metadata 547 0 R', b'/Metadata 603 0 R', ...]
		
		xmp_obj_dict = {}
		for ref in xmp_ref:
			# XMP ref name is, e.g., b'/Metadata 547 0 R'
			# Corresponding object name is: b'547 0' 
			ref = ref.decode()
			ref = ref.replace('/Metadata ', '')
			ref = ref.replace(' R', '')
			ref = str.encode(ref)
			# Now the variable ref becomes the object name b'547 0'
			# b'547 0'
			
			regex = b'[^0-9]' + ref + b'[ ]obj.*?endobj'
			# ^every XMP object starts with: object name + 'obj' and ends with 'endobj'
			# e.g., 547 0 obj ...... endobj
			pattern = re.compile(regex, re.DOTALL)
			xmp_obj = re.findall(pattern, read_file)
			# Here, xmp_obj is a Python list of a XMP obj, e.g.:
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
	# ^find the substring within the desirable tags

	in_brackets = False
	endpoints = []
	# however, there may still be unwanted tags within the substring
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
		# ^discard undesirable tags
	#results = results[endpoints[0]:endpoints[-1]+1]
	
	answer = ""
	for i in range(len(endpoints)):
		if i>0:
			if endpoints[i] - 1 != endpoints[i-1]:
				answer += ", "
		answer += results[endpoints[i]]
	answer = re.sub(" ,",",",answer)
	# a title is a consecutive phrase
	# but authors or keywords, originally separated by the undesirable tags,
	# should now be separated by commas
	if "Adobe" in answer or "Apple" in answer or "Windows" in answer or "TeX" in answer:
		answer = None
	return answer