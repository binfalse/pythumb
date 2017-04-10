#!/usr/bin/env python
# encoding=utf8
from __future__ import unicode_literals 
from xml.dom import minidom
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
import subprocess
import tempfile
import urllib
import re
import os
import sys
import magic
import zipfile
import logging
import textwrap
from StringIO import StringIO

log = logging.getLogger(__name__)

reload(sys)
sys.setdefaultencoding('utf8')


_overwrite_thumb = False

default_thumb_width = 300
default_thumb_height = 300

_thumb_width = default_thumb_width
_thumb_height = default_thumb_height

# TODO: option to set the color
_font_color = (50, 50, 50)
_line_color = (80, 80, 80)

_img_ext_regex = re.compile (r'^.*\.(jpg|jpeg|png)$', flags=re.IGNORECASE)
_cover_regex = re.compile (r'.*cover.*\.(jpg|jpeg|png)', flags=re.IGNORECASE)


# DEBUGGING
import pdb
#pdb.set_trace()



# set the desired thumbnail dimensions
def set_thumb_dimensions (width, height):
	global _thumb_width
	global _thumb_height
	_thumb_width = width
	_thumb_height = height

# should existing thumbnails be overwritten?
def set_overwrite_thumb (boolean):
	_overwrite_thumb = boolean






# generate a thumbnail file displaying just the file name
# this should be the last resort, if we cannot create a better thumbnail from the data
def thumb_from_name (name, preview_file):
	# shorten the name to fit into the image
	if len (name) > 100:
		name = name[:95] + ".."
	
	fontsize = 26
	font = ImageFont.truetype ("font.ttf", fontsize)
	
	if len (name) > 90:
		name = textwrap.wrap (name, len (name) / 4)
	elif len (name) > 60:
		name = textwrap.wrap (name, len (name) / 3)
	elif len (name) > 30:
		name = textwrap.wrap (name, len (name) / 2)
	else:
		name = [name]
	
	# calculate image dimensions, depending
	# on width/height of the tokens
	lineheight = 0
	linewidth = 0
	
	for token in name:
		s = font.getsize (token)
		if s[0] > linewidth:
			linewidth = s[0]
		if s[1] > lineheight:
			lineheight = s[1]
	
	log.debug ("drawing title " + str (name) + " with fontsize: " + str (fontsize))
	
	pic_width = linewidth + 20
	pic_height = (len (name) * (lineheight + 2)) + 40
	
	img = Image.new("RGB", (pic_width, pic_height), (255,255,255))
	draw = ImageDraw.Draw (img)
	
	currentY = (pic_height - (lineheight + 2) * len (name)) / 2 - 2
	
	# write all tokens 
	for token in name:
		fontBox = font.getsize (token)
		x = (pic_width - fontBox[0]) / 2
		y = currentY
		
		log.debug ("drawing " + token + " at: " + str (x) + ":" + str(y))
		draw.text ((x, y), token, _font_color, font=font)
		currentY += lineheight + 2
	
	# add some lines, that the pic doesn't look too empty...
	# TODO: space for improvements.. ;-)
	draw.line((5, pic_height - 5, pic_width - 5, pic_height - 5), fill=_line_color)
	draw.line((5, 5, pic_width - 5, 5), fill=_line_color)
	
	draw.line((15, pic_height - 8, pic_width - 15, pic_height - 8), fill=_line_color)
	draw.line((15, 8, pic_width - 15, 8), fill=_line_color)
	
	
	with tempfile.NamedTemporaryFile (suffix='.png') as temp:
		img.save (temp.name)
		return thumb_from_image (temp.name, preview_file)
	return True


# crop a very large image to a size of max 1000x1000
# necessary for imagemagick, as that won't handle extremely large images...
def crop_preview (orginal_file):
	img = Image.open (orginal_file)
	
	if img.size[0] < width and img.size[1] < height:
		return True
	
	width = 1000
	height = 1000
	if img.size[0] < 1000:
		width = img.size[0]
	if img.size[1] < 1000:
		height = img.size[1]
	
	log.debug ("cropping the image " + orginal_file + " (" + img.size + ")" + " to " + str (width) + "x" + str (height))
	return img.crop ((0, 0, width, height)).save (orginal_file)


# generate a thumbnail with imagemagick
def thumb_from_image (orginal_file, preview_file):
	log.info ("generating thumbnail with imagemagick for " + orginal_file)
	cmd = ["convert", "-thumbnail", str (_thumb_width) + "x" + str (_thumb_height), "-flatten", orginal_file, preview_file]
	
	log.debug ("executing " + str (cmd))
	return_code = subprocess.call(cmd)
	
	if return_code != 0:
		log.error ("error converting: " + orginal_file + " to " + preview_file + " -- command was: " + str (cmd) + "\n")
		return False
	return True


# extract an image from a zip file (eg. epub) and create a thumbnail from it
def _thumb_from_zipped_image (zipContainer, path, preview_file):
	log.debug ("creating thumb from zipped image:" + path)
	# extract the image
	with tempfile.NamedTemporaryFile () as temp:
		temp.write (zipContainer.read(path))
		temp.flush ()
		# convert to thumbnail
		return thumb_from_image (temp.name, preview_file)
	return False


# find a cover image in the epub manifest
def _thumb_from_epub_manifest (epub, preview_file):
	log.debug ("searching for image in epub manifest")
	
	# open the main container
	container = epub.open ("META-INF/container.xml")
	container_root = minidom.parseString (container.read())
	
	# locate the rootfile
	elem = container_root.getElementsByTagName ("rootfile")[0]
	rootfile_path = elem.getAttribute ("full-path")
	
	# open the rootfile
	rootfile = epub.open (rootfile_path)
	rootfile_root = minidom.parseString (rootfile.read ())
	
	# find possible cover in meta
	cover_id = None
	for meta in rootfile_root.getElementsByTagName ("meta"):
			if meta.getAttribute ("name") == "cover":
					cover_id = meta.getAttribute ("content")
					log.debug ("cover id: " + cover_id)
					break
				
	# find the manifest element
	manifest = rootfile_root.getElementsByTagName ("manifest")[0]
	for item in manifest.getElementsByTagName ("item"):
			item_id = item.getAttribute ("id")
			item_href = item.getAttribute ("href")
			if (item_id == cover_id) or ("cover" in item_id and _img_ext_regex.match (item_href.lower ())):
					#return 
					path = os.path.join (os.path.dirname (rootfile_path), item_href)
					log.debug ("images from epub manifest: " + path)
					return _thumb_from_zipped_image (epub, path, preview_file)
	
	# nothing found
	return False


# find an image in the zip file and generate the thumbnail from it
def _thumb_from_epub_file_cover (epub, preview_file):
	log.debug ("searching for an image in the zip")
	
	# images in the zip:
	candidates = []
	
	# iterate images
	for fileinfo in epub.filelist:
		# does the image match the cover-file regex?
		# then we're good to go with that :)
		if _cover_regex.match(fileinfo.filename):
			if _thumb_from_zipped_image (epub, fileinfo.filename, preview_file):
				return True
		
		# otherwise add it to candidates if it is and image
		if _img_ext_regex.match(fileinfo.filename):
			candidates.append(fileinfo)
	
	log.debug ("found candidates: " + str (candidates))
	if candidates:
		candidate = max (candidates, key=lambda f: f.file_size)
		log.debug ("best candidate: " + candidate.filename)
		return _thumb_from_zipped_image (epub, candidate.filename, preview_file)
	
	return False



# inspired by https://github.com/marianosimone/epub-thumbnailer
def thumb_from_epub (orginal_file, preview_file):
	log.info ("generating preview of EPUB for " + orginal_file)
	file_url = urllib.urlopen (orginal_file)
	
	with zipfile.ZipFile (StringIO (file_url.read ()), "r") as epub:
		
		if _thumb_from_epub_manifest (epub, preview_file):
			return True
		
		if _thumb_from_epub_file_cover (epub, preview_file):
			return True
		
		return False



# generate a thumbnail from an HTML document
def thumb_from_html (orginal_file, preview_file):
	log.info ("generating html preview for " + orginal_file)
	
	# render the page with cutycapt
	with tempfile.NamedTemporaryFile (suffix='.png') as temp:
		cmd = ["cutycapt", "--max-wait=1000", "--url=file://" + os.getcwd () + "/" + orginal_file, "--out=" + temp.name]
		log.debug ("executing " + str (cmd))
		return_code = subprocess.call (cmd)
		if return_code != 0:
			log.error ("error converting html file: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
			return False
		
		# crop super-long (height) HTML pages, otherwise imagemagick will complain...
		crop_preview (temp.name)
		
		# use imagemagick to create the actual thumbnail
		return thumb_from_image (temp.name, preview_file)
	return False


# generate a thumbnail from an office file
def thumb_from_office_doc (orginal_file, preview_file):
	log.info ("generating preview for office document " + orginal_file)
	
	# first convert it into a PDF -> libre office is necessary
	with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
		cmd = ["convert", orginal_file, temp.name]
		log.debug ("executing " + str (cmd))
		return_code = subprocess.call (cmd)
		
		if return_code != 0:
			log.error ("error converting office file: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
			return False
		
		# use imagemagick to convert the PDF
		return thumb_from_image (temp.name + "[0]", preview_file)
	return False


# generate a thumbnail for a file
def thumb_from_file (orginal_file, preview_file, orginal_fileName):
	log.info ("generating preview for file " + orginal_file + " to " + preview_file)
	
	if not _overwrite_thumb and os.path.exists (preview_file):
		return False
	
	if not os.path.exists(orginal_file):
		raise IOError ("file does not exist: " + orginal_file)
	
	# guess the mime type of the file
	m = magic.open(magic.MAGIC_MIME)
	m.load()
	mime = m.file (orginal_file)
	log.debug ("mime: " + mime)
	
	# is that an image? -> just use image magic...
	if 'image/' in mime:
		log.debug ("is an image")
		if thumb_from_image (orginal_file, preview_file):
			return True
	
	# pdf like document? -> image magic...
	if any (option in mime for option in ['application/pdf', 'application/postscript', 'djvu']):
		log.debug ("is pdf like")
		if thumb_from_image (orginal_file + "[0]", preview_file):
			return True
	
	# epub? -> extract image if possible
	if 'epub+zip' in mime:
		log.debug ("is an epub")
		if thumb_from_epub (orginal_file, preview_file):
			return True
	
	# HTML page? -> screenshot
	if 'text/html' in mime:
		log.debug ("is html")
		if thumb_from_html (orginal_file, preview_file):
			return True
	
	# office document?
	if any (option in mime for option in ['application/msword', 'application/vnd.ms-', 'application/vnd.oasis.opendocument.', 'application/vnd.openxmlformats-officedocument.']):
		log.debug ("is office doc")
		if thumb_from_office_doc (orginal_file, preview_file):
			return True
		
		#2 application/msword;
		#3 application/postscript;
		#1 application/zip;
		#2 image/vnd.djvu;
		#1 image/vnd.dwg;
		#1 inode/x-empty;
		#237 text/html;
		#1 text/plain;
		
		
	#elif ''
		
		#image/x-icon
		#image/gif
		#text/html
		#text/plain
		#application/epub+zip
		
		
		
		
	# no solution so far?
	log.warn ("don't understand mime " + mime + " from " + orginal_file)
	# create a thumb just displaying a name
	if thumb_from_name (orginal_fileName, preview_file):
		return True
	
	return False





