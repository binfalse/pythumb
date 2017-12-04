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

reload(sys)
sys.setdefaultencoding('utf8')

# DEBUGGING
import pdb
#pdb.set_trace()




class PyThumb:

	log = logging.getLogger(__name__)

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
	_url_regex = re.compile (r'^https?://', flags=re.IGNORECASE)


	def __init__(self):
		self._thumb_width = self.default_thumb_width
		self._thumb_height = self.default_thumb_height


	# set the desired thumbnail dimensions
	def set_thumb_dimensions (self, width, height):
		self._thumb_width = width
		self._thumb_height = height

	# should existing thumbnails be overwritten?
	def set_overwrite_thumb (self, boolean):
		self._overwrite_thumb = boolean






	# generate a thumbnail file displaying just the file name
	# this should be the last resort, if we cannot create a better thumbnail from the data
	def thumb_from_name (self, name, preview_file):
		self.log.info ("generating thumbnail from string: " + name)
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
			
		print name
		
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
		
		self.log.debug ("drawing title " + str (name) + " with fontsize: " + str (fontsize))
		
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
			
			self.log.debug ("drawing " + token + " at: " + str (x) + ":" + str(y))
			draw.text ((x, y), token, self._font_color, font=font)
			currentY += lineheight + 2
		
		# add some lines, that the pic doesn't look too empty...
		# TODO: space for improvements.. ;-)
		draw.line((5, pic_height - 5, pic_width - 5, pic_height - 5), fill=self._line_color)
		draw.line((5, 5, pic_width - 5, 5), fill=self._line_color)
		
		draw.line((15, pic_height - 8, pic_width - 15, pic_height - 8), fill=self._line_color)
		draw.line((15, 8, pic_width - 15, 8), fill=self._line_color)
		
		
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			img.save (temp.name)
			return self.thumb_from_image (temp.name, preview_file)
		return True


	# crop a very large image to a size of max 1000x1000
	# necessary for imagemagick, as that won't handle extremely large images...
	def crop_preview (self, orginal_file):
		img = Image.open (orginal_file)
		
		width = 1000
		height = 1000
		
		if img.size[0] < width and img.size[1] < height:
			return True
		
		if img.size[0] < 1000:
			width = img.size[0]
		if img.size[1] < 1000:
			height = img.size[1]
		
		self.log.debug ("cropping the image " + orginal_file + " (" + str (img.size) + ")" + " to " + str (width) + "x" + str (height))
		return img.crop ((0, 0, width, height)).save (orginal_file)


	# generate a thumbnail with imagemagick
	def thumb_from_image (self, orginal_file, preview_file):
		self.log.info ("generating thumbnail with imagemagick for " + orginal_file)
		cmd = ["convert", "-trim", "-thumbnail", str (self._thumb_width) + "x" + str (self._thumb_height), "-flatten", orginal_file, preview_file]
		
		self.log.debug ("executing " + str (cmd))
		return_code = subprocess.call(cmd)
		
		if return_code != 0:
			self.log.error ("error converting: " + orginal_file + " to " + preview_file + " -- command was: " + str (cmd) + "\n")
			return False
		return True


	# convert to PDF and do the pdf conversion
	def thumb_from_postscript (self, orginal_file, preview_file):
		self.log.info ("generating thumbnail with ps2pdf for " + orginal_file)
		with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
			cmd = ["ps2pdf", orginal_file, temp.name]	
			
			self.log.debug ("executing " + str (cmd))
			return_code = subprocess.call(cmd)
			
			if return_code != 0:
				self.log.error ("error converting: " + orginal_file + " to " + temp.name + " -- command was: " + str (cmd) + "\n")
				return False
			return self.thumb_from_image (temp.name + "[0]", preview_file)
		return False
	
	


	# convert to PDF and do the pdf conversion
	def thumb_from_eps (self, orginal_file, preview_file):
		self.log.info ("generating thumbnail with epstopdf for " + orginal_file)
		with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
			cmd = ["epstopdf", orginal_file, temp.name]	
			
			self.log.debug ("executing " + str (cmd))
			return_code = subprocess.call(cmd)
			
			if return_code != 0:
				self.log.error ("error converting: " + orginal_file + " to " + temp.name + " -- command was: " + str (cmd) + "\n")
				return False
			return self.thumb_from_image (temp.name + "[0]", preview_file)
		return False
	


	# this is just a helper function
	# extract an image from a zip file (eg. epub) and create a thumbnail from it
	def _thumb_from_zipped_image (self, zipContainer, path, preview_file):
		self.log.debug ("creating thumb from zipped image:" + path)
		# extract the image
		
		# TODO: image extension
		with tempfile.NamedTemporaryFile () as temp:
			temp.write (zipContainer.read(path))
			temp.flush ()
			# convert to thumbnail
			return self.thumb_from_image (temp.name, preview_file)
		return False


	# this is just a helper function
	# find a cover image in the epub manifest
	def _thumb_from_epub_manifest (self, epub, preview_file):
		self.log.debug ("searching for image in epub manifest")
		
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
						self.log.debug ("cover id: " + cover_id)
						break
					
		# find the manifest element
		manifest = rootfile_root.getElementsByTagName ("manifest")[0]
		for item in manifest.getElementsByTagName ("item"):
				item_id = item.getAttribute ("id")
				item_href = item.getAttribute ("href")
				if (item_id == cover_id) or ("cover" in item_id and self._img_ext_regex.match (item_href.lower ())):
						#return 
						path = os.path.join (os.path.dirname (rootfile_path), item_href)
						self.log.debug ("images from epub manifest: " + path)
						return self._thumb_from_zipped_image (epub, path, preview_file)
		
		# nothing found
		return False


	# this is just a helper function
	# find an image in the zip file and generate the thumbnail from it
	def _thumb_from_zip_images (self, zippy, preview_file):
		self.log.debug ("searching for an image in the zip")
		
		# images in the zip:
		candidates = []
		
		# iterate images
		for fileinfo in zippy.filelist:
			# does the image match the cover-file regex?
			# then we're good to go with that :)
			if self._cover_regex.match(fileinfo.filename):
				if self._thumb_from_zipped_image (zippy, fileinfo.filename, preview_file):
					return True
			
			# otherwise add it to candidates if it is and image
			if self._img_ext_regex.match(fileinfo.filename):
				candidates.append(fileinfo)
		
		self.log.debug ("found candidates: " + str (candidates))
		if candidates:
			# take 'largest' candidate, assuming this is the best picture ;-)
			candidate = max (candidates, key=lambda f: f.file_size)
			self.log.debug ("best candidate: " + candidate.filename)
			return self._thumb_from_zipped_image (zippy, candidate.filename, preview_file)
		
		return False



	# inspired by https://github.com/marianosimone/epub-thumbnailer
	def thumb_from_epub (self, orginal_file, preview_file):
		self.log.info ("generating preview of EPUB for " + orginal_file)
		file_url = urllib.urlopen (orginal_file)
		
		with zipfile.ZipFile (StringIO (file_url.read ()), "r") as epub:
			
			try:
				if self._thumb_from_epub_manifest (epub, preview_file):
					return True
			except Exception as e:
				self.log.warn (e)
				self.log.warn ("couldn't handle epub manifest...")
		
		return self.thumb_from_zip (orginal_file, preview_file)




	# generate a thumbnail for a zip container
	def thumb_from_zip (self, orginal_file, preview_file):
		self.log.info ("generating preview of EPUB for " + orginal_file)
		file_url = urllib.urlopen (orginal_file)
		
		with zipfile.ZipFile (StringIO (file_url.read ()), "r") as zippy:
			
			try:
				if self._thumb_from_zip_images (zippy, preview_file):
					return True
			except Exception as e:
				self.log.warn (e)
				self.log.warn ("couldn't handle image search in zip...")
			
			return False




	# this is just a helper function
	# run cutycapt to capture a website...
	def _run_cutycapt (self, orginal_file, preview_file, max_wait):
		self.log.info ("running cutycapt for " + orginal_file)
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			cmd = ["cutycapt", "--max-wait=" + str (max_wait), "--url=" + orginal_file, "--out=" + temp.name]
			self.log.debug ("executing " + str (cmd))
			return_code = subprocess.call (cmd)
			if return_code != 0:
				self.log.error ("error converting html file: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
				return False
			
			# crop super-long (height) HTML pages, otherwise imagemagick will complain...
			self.crop_preview (temp.name)
			
			# use imagemagick to create the actual thumbnail
			return self.thumb_from_image (temp.name, preview_file)
		return False


	# generate a thumbnail from an HTML document
	def thumb_from_html (self, orginal_file, preview_file):
		self.log.info ("generating html preview for " + orginal_file)
		return self._run_cutycapt ("file://" + os.getcwd () + "/" + orginal_file, preview_file, 1000)


	# this is just a helper function
	# for file.tar.gz it returns (file.tar, .gz)
	def _get_file_name_and_ext (self, filename):
		filename = os.path.basename (filename)
		if len(filename.split('.')) > 2:
			return ('.'.join (filename.split ('.')[0:-1]), '.' + filename.split('.')[-1])
		return os.path.splitext(filename)


	# this is just a helper function
	# get the extension of a file (for 'file.tar.gz' it is 'file.tar')
	def _get_file_name_wo_ext (self, filename):
		return self._get_file_name_and_ext (filename)[0]

	# this is just a helper function
	# get the extension of a file (for 'file.tar.gz' it is '.gz')
	def _get_file_ext (self, filename):
		return self._get_file_name_and_ext (filename)[1]


	# generate a thumbnail from an office file
	def thumb_from_office_doc (self, orginal_file, preview_file):
		self.log.info ("generating preview for office document " + orginal_file)
		
		
		# try imagemagic to generate PDF of the office file:
		with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
			cmd = ["convert", orginal_file, temp.name]
			self.log.debug ("executing " + str (cmd))
			return_code = subprocess.call (cmd)
			
			if return_code != 0:
					self.log.error ("error converting office file with imagemagick: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
			else:
				# use imagemagick to convert the PDF
				return_code = self.thumb_from_image (temp.name + "[0]", preview_file)
				if return_code:
					return True
				else:
					self.log.error ("error converting pdf of office file with imagemagick: " + orginal_file + " to " + preview_file)
		
		# try libreoffice to generate the PDF
		temp = tempfile.mkdtemp (prefix='pythumb-working-office-')
		cmd = ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", temp, orginal_file]
		self.log.debug ("executing " + str (cmd))
		return_code = subprocess.call (cmd)
		
		if return_code != 0:
			self.log.error ("error converting office file: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
			return False
		
		# use imagemagick to convert the PDF
		f = os.path.join (temp, self._get_file_name_wo_ext (orginal_file) + ".pdf")
		self.log.debug ("expecting output in " + f)
		if (os.path.isfile (f)):
			return self.thumb_from_image (f + "[0]", preview_file)
		else:
			self.log.error ("did not find outputfile in " + f)
		return False


	# generate a thumbnail from a plain text file
	def thumb_from_plain_text (self, orginal_file, preview_file):
		self.log.info ("generating preview for plain text document " + orginal_file)
		
		with open(orginal_file, 'r') as f:
			string = f.read (200).strip()
			self.log.info ("read first few characters from plain text file: " + string)
			
			# strip unnecessary white space
			string = ' '.join(string.split())
			self.log.info ("eliminated unnecessary white space: " + string)
			
			# if there is enough content we can use it:
			if len (string) > 5:
				self.log.info ("got enough content to generate thumb")
				return self.thumb_from_name (string, preview_file)
			
			
			self.log.warn ("failed... not enough content to generate thumb")
			
		return False


	# generate a thumbnail for a file
	def thumb_from_file (self, orginal_file, preview_file, orginal_fileName):
		self.log.info ("generating preview for file " + orginal_file + " to " + preview_file)
		
		if not self._overwrite_thumb and os.path.exists (preview_file):
			self.log.warn ("will not overwrite file " + preview_file + " as _overwrite_thumb is set to " + str (self._overwrite_thumb))
			return False
		
		if not os.path.exists(orginal_file):
			raise IOError ("file does not exist: " + orginal_file)
		
		# guess the mime type of the file
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		mime = m.file (orginal_file)
		self.log.debug ("mime: " + mime)
		
		# pdf like document? -> image magic...
		if any (option in mime for option in ['application/pdf', 'djvu']):
			self.log.debug ("is pdf like")
			if self.thumb_from_image (orginal_file + "[0]", preview_file):
				return True
		
		# is that an image? -> just use image magic...
		if 'image/' in mime:
			self.log.debug ("is an image")
			if self.thumb_from_image (orginal_file, preview_file):
				return True
		
		# ps document? -> convert to pdf and do the pdf tricks
		if 'application/postscript' in mime:
			self.log.debug ("is pdf like")
			if self.thumb_from_postscript (orginal_file, preview_file):
				return True
		
		# epub? -> extract image if possible
		if 'epub+zip' in mime:
			self.log.debug ("is an epub")
			if self.thumb_from_epub (orginal_file, preview_file):
				return True
		
		# HTML page? -> screenshot
		if 'text/html' in mime:
			self.log.debug ("is html")
			if self.thumb_from_html (orginal_file, preview_file):
				return True
		
		# office document?
		if any (option in mime for option in ['application/msword', 'application/vnd.ms-', 'application/vnd.oasis.opendocument.', 'application/vnd.openxmlformats-officedocument.']):
			self.log.debug ("is office doc")
			if self.thumb_from_office_doc (orginal_file, preview_file):
				return True
		
		# plain text file -> read first chars and print into pic
		if 'text/' in mime:
			self.log.debug ("is plain text")
			if self.thumb_from_plain_text (orginal_file, preview_file):
				return True
		
		# zip archive? -> extract image if possible
		if 'zip' in mime:
			self.log.debug ("is a zip file")
			if self._thumb_from_zip_images (orginal_file, preview_file):
				return True
			
		# TODO:
		# * application/zip; -> like eupb?
		# * image/vnd.dwg;
			
		# no solution so far?
		self.log.warn ("failed to generate file-specific thumbnail for mime " + mime + " (" + orginal_file + ")")
		# create a thumb just displaying a name
		if self.thumb_from_name (orginal_fileName, preview_file):
			return True
		
		return False





	# generate a thumbnail from an HTML document
	def thumb_from_website (self, url, preview_file):
		self.log.info ("generating html preview for " + url)
		if self._url_regex.match (url):
			return self._run_cutycapt (url, preview_file, 15000)
		self.log.warn ("doesn't seem to be a proper url: " + url)
		return False




