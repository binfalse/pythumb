#!/usr/bin/env python
# encoding=utf8

# add above dir to lib path
import sys
sys.path.append('../pythumb')

from pythumb import PyThumb
import tempfile
import os

# enable logging if desired
#import logging
#logging.basicConfig()
#tmplog = logging.getLogger("pythumb")
#tmplog.setLevel(logging.DEBUG)


# create pythumb instance
pythumb = PyThumb ()
# setup if not satisfied with default settings
pythumb.set_thumb_dimensions (100, 100)
pythumb.set_font ("../font.ttf")

# create thumbnail from a website
url = "https://binfalse.de/"
thumb = "/tmp/pythumb-tmp-web.png"

if os.path.isfile (thumb):
	os.remove (thumb)

if pythumb.thumb_from_website (url, thumb):
	print ("thumbnail of " + url + " stored in " + thumb)
else:
	print ("couldn't create thumbnail from " + url)



# create thumbnail from file
filename = "../test/files/pdflike-2.pdf"
thumb = "/tmp/pythumb-tmp-file.png"

if os.path.isfile (thumb):
	os.remove (thumb)

if pythumb.thumb_from_file (filename, thumb, "some default string"):
	print ("thumbnail of " + filename + " stored in " + thumb)
else:
	print ("couldn't create thumbnail from " + filename)

