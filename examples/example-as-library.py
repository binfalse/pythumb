#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import tempfile
import os


# create thumbnail from a website

url = "https://binfalse.de/"
thumb = "/tmp/pythumb-tmp-web.png"

if os.path.isfile (thumb):
	os.remove (thumb)

if pythumb.thumb_from_website (url, thumb):
	print "thumbnail of " + url + " stored in " + thumb
else:
	print "couldn't create thumbnail from " + url



# create thumbnail from file

filename = "test/files/pdflike-2.pdf"
thum = "/tmp/pythumb-tmp-file.png"

if os.path.isfile (thumb):
	os.remove (thumb)

if pythumb.thumb_from_file (filename, thumb, "some default string"):
	print "thumbnail of " + filename + " stored in " + thumb
else:
	print "couldn't create thumbnail from " + filename

