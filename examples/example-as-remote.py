#!/usr/bin/env python
# encoding=utf8


import requests

# let's assume that the server is running at localhost:12346
SERVER='http://localhost:12346'
# to learn how to run the server have a look at https://github.com/binfalse/pythumb/



# create thumbnail of the file test/files/pdflike-2.pdf
# and store the thumbnail in /tmp/pythumb-tmp-file.png
response = requests.post(SERVER, files=dict(file=open('test/files/pdflike-2.pdf', 'rb')), data=dict(target='upload', filename='main.pdf'))
if response.status_code == 200:
	with open('/tmp/pythumb-tmp-file.png', 'wb') as f:
		f.write(response.content)
		print ("created thumbnail of test/files/pdflike-2.pdf in /tmp/pythumb-tmp-file.png")
else:
	print ("failed to create thumbnail, response code was: " + str (response.status_code))
	print (response.text)





# create a thumbnail of https://binfalse.de/
# and store it in /tmp/pythumb-tmp-web.png
response = requests.post(SERVER, files=dict(target='https://binfalse.de/'))
if response.status_code == 200:
	with open('/tmp/pythumb-tmp-web.png', 'wb') as f:
		f.write(response.content)
		print ("created thumbnail of https://binfalse.de/ in /tmp/pythumb-tmp-web.png")
else:
	print ("failed to create thumbnail, response code was: " + str (response.status_code))
	print (response.text)
