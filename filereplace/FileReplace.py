

import json,os

def fetch(file,str):
	fetch_list = []
	try:
		f = open(file,'r+')
	except Exception as e:
		print (str(e))
		return

	file_content = json.loads(f.read())

	for k,v in file_content.items():
		if k == "mysql_server_address":
			file_content[k] = str

	with open('test.txt','w+') as obj2:
		obj3 = json.dumps(file_content)
		for i in obj3:
			# print (i,'*' * 10)
			if i == "}":
				obj2.write("\n" + i + "\n")
				continue
			if i == "{":
				obj2.write(i + "\n")
				continue
			if i == ",":
				obj2.write(i+ '\n' + "  "),
				continue
			else:
				obj2.write(i)


		# obj3.write(json.dumps(file_content))

if __name__ ==  '__main__':
	obj = fetch('post-mc.conf','127.0.0.2')



