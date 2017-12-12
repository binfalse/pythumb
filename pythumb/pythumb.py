#!/usr/bin/env python3
# encoding=utf8
#
# Copyright 2017 Martin Scharm <https://binfalse.de/contact/>
#
# This file is part of PyThumb.
# <https://github.com/binfalse/pythumb/>
# 
# PyThumb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyThumb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyThumb.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals 
from xml.dom import minidom
import subprocess
import tempfile
import re
import os
import sys
import magic
import zipfile
import logging
import argparse
import textwrap
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from shutil import copyfile
from io import StringIO
from xvfbwrapper import Xvfb

# reload(sys)
# sys.setdefaultencoding('utf8')

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

	_img_ext_regex = re.compile (r'^.*\.(jpg|jpeg|png|gif)$', flags=re.IGNORECASE)
	_cover_regex = re.compile (r'.*cover.*\.(jpg|jpeg|png)', flags=re.IGNORECASE)
	_url_regex = re.compile (r'^https?://', flags=re.IGNORECASE)
	
	_font = "/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf"
	

	default_crop_width = 10000
	default_crop_height = 10000
	
	_crop_width = default_crop_width
	_crop_height = default_crop_height


	def __init__(self):
		self._thumb_width = self.default_thumb_width
		self._thumb_height = self.default_thumb_height
		
		self._crop_width = self.default_crop_width
		self._crop_height = self.default_crop_height


	# set the desired cropping dimensions
	def set_crop_dimensions (self, width, height):
		width = int (width)
		height = int (height)
		if width > 0:
			self._crop_width = width
		else:
			self.log.warn("will not set width to " + str (width))
		
		if height > 0:
			self._crop_height = height
		else:
			self.log.warn("will not set height to " + str (height))


	# set the desired thumbnail dimensions
	def set_thumb_dimensions (self, width, height):
		width = int (width)
		height = int (height)
		if width > 0:
			self._thumb_width = width
		else:
			self.log.warn("will not set width to " + str (width))
		
		if height > 0:
			self._thumb_height = height
		else:
			self.log.warn("will not set height to " + str (height))

	# should existing thumbnails be overwritten?
	def set_overwrite_thumb (self, boolean):
		self._overwrite_thumb = boolean


	# set the font to use for text in default images
	# needs to be the path to a true-type-font
	def set_font (self, fontpath):
		self._font = fontpath



	# generate a thumbnail file displaying just the file name
	# this should be the last resort, if we cannot create a better thumbnail from the data
	def thumb_from_name (self, name, preview_file):
		self.log.info ("generating thumbnail from string: " + name)
		# shorten the name to fit into the image
		if len (name) > 100:
			name = name[:95] + ".."
		
		fontsize = 26
		font = ImageFont.load_default()
		if self._font and os.path.isfile (self._font):
			font = ImageFont.truetype (self._font, fontsize)
		
		if len (name) > 90:
			name = textwrap.wrap (name, round (len (name) / 4))
		elif len (name) > 60:
			name = textwrap.wrap (name, round (len (name) / 3))
		elif len (name) > 30:
			name = textwrap.wrap (name, round (len (name) / 2))
		else:
			name = [name]
			
		self.log.info ("name to print: " + str (name))
		
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


	# crop a very large image to a size of max 1000x1000
	# necessary for imagemagick, as that won't handle extremely large images...
	# BE CAREFUL: will crop in-place!! so do not provide original/raw files!
	def _crop_preview (self, preview_file):
		img = Image.open (preview_file)
		
		width = self._crop_width
		height = self._crop_height
		
		if img.size[0] < width and img.size[1] < height:
			return True
		
		if img.size[0] < 10000:
			width = img.size[0]
		if img.size[1] < 10000:
			height = img.size[1]
		
		self.log.debug ("cropping the image " + preview_file + " " + str (img.size) + "" + " to " + str (width) + "x" + str (height))
		img.crop ((0, 0, width, height)).save (preview_file)
		return True


	# converts orginal_file to preview_file using imagemagick
	def _run_convert (self, orginal_file, preview_file):
		self.log.info ("running convert utility for " + orginal_file + " to " + preview_file)
		cmd = ["convert", "-trim", "-thumbnail", str (self._thumb_width) + "x" + str (self._thumb_height), "-flatten", orginal_file, preview_file]
		self.log.debug ("executing " + str (cmd))
		
		return_code = subprocess.call(cmd)
		if return_code != 0:
			self.log.error ("error converting: " + orginal_file + " to " + preview_file + " -- command was: " + str (cmd) + "\n")
			return False
		return True


	# generate a thumbnail with imagemagick
	def thumb_from_image (self, orginal_file, preview_file):
		self.log.info ("generating thumbnail with imagemagick for " + orginal_file)
		with tempfile.NamedTemporaryFile (suffix=str(self._get_file_ext(orginal_file)), delete=False) as temp:
			
			self.log.info ("copying " + orginal_file + " to " + temp.name + " for cropping")
			copyfile (orginal_file, temp.name)
			
			# only cropping supported formats by PIL
			if self._img_ext_regex.match (orginal_file) and not self._crop_preview (temp.name):
				self.log.error ("could not crop copied original...")
				return False
			
			return self._run_convert (temp.name, preview_file)
	
	# generate a thumbnail from a PDF file with image magick
	def thumb_from_pdf (self, orginal_file, preview_file):
		self.log.info ("generating thumbnail with imagemagick for " + orginal_file)
		return self._run_convert (orginal_file, preview_file)


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
			return self.thumb_from_pdf (temp.name + "[0]", preview_file)
	
	

	# probably not necessary as we can do ps2pdf
	# convert to PDF and do the pdf conversion
	#def thumb_from_eps (self, orginal_file, preview_file):
	#	self.log.info ("generating thumbnail with epstopdf for " + orginal_file)
	#	with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
	#		cmd = ["epstopdf", orginal_file, temp.name]	
	#		
	#		self.log.debug ("executing " + str (cmd))
	#		return_code = subprocess.call(cmd)
	#		
	#		if return_code != 0:
	#			self.log.error ("error converting: " + orginal_file + " to " + temp.name + " -- command was: " + str (cmd) + "\n")
	#			return False
	#		return self.thumb_from_pdf (temp.name + "[0]", preview_file)
	#	return False
	


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
		if len (candidates) > 0:
			# take 'largest' candidate, assuming this is the best picture ;-)
			candidate = max (candidates, key=lambda f: f.file_size)
			self.log.debug ("best candidate: " + candidate.filename)
			return self._thumb_from_zipped_image (zippy, candidate.filename, preview_file)
		
		return False



	# inspired by https://github.com/marianosimone/epub-thumbnailer
	def thumb_from_epub (self, orginal_file, preview_file):
		self.log.info ("generating preview of EPUB for " + orginal_file)
		
		with zipfile.ZipFile (orginal_file, "r") as epub:
			
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
		
		with zipfile.ZipFile (orginal_file, "r") as zippy:
			
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
			with Xvfb() as xvfb:
				cmd = ["cutycapt", "--max-wait=" + str (max_wait), "--private-browsing=on", "--user-agent=PyThumb (https://github.com/binfalse/pythumb/)", "--url=" + orginal_file, "--out=" + temp.name]
				self.log.debug ("executing " + str (cmd))
				return_code = subprocess.call (cmd)
				if return_code != 0:
					self.log.error ("error converting html file: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
					return False
			
			# crop super-long (height) HTML pages, otherwise imagemagick will complain...
			#self._crop_preview (temp.name)
			
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
# 		with tempfile.NamedTemporaryFile (suffix='.pdf') as temp:
			
		if self._run_convert(orginal_file, preview_file):
			return True
		else:
			self.log.error ("error converting office file with imagemagick: " + orginal_file + " to " + preview_file)
# 			cmd = ["convert", orginal_file, temp.name]
# 			self.log.debug ("executing " + str (cmd))
# 			return_code = subprocess.call (cmd)
# 			
# 			if return_code != 0:
# 					self.log.error ("error converting office file with imagemagick: " + orginal_file + " to " + preview_file + " -- command was " + str (cmd))
# 			else:
# 				# use imagemagick to convert the PDF
# 				return_code = self.thumb_from_pdf (temp.name + "[0]", preview_file)
# 				if return_code:
# 					return True
# 				else:
# 					self.log.error ("error converting pdf of office file with imagemagick: " + orginal_file + " to " + preview_file)
		
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
			return self.thumb_from_pdf (f + "[0]", preview_file)
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
			self.log.error ("file does not exist: " + orginal_file)
			return False
		
		# guess the mime type of the file
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		mime = m.file (orginal_file)
		self.log.debug ("mime: " + mime)
		
		# pdf like document? -> image magic...
		if any (option in mime for option in ['application/pdf', 'djvu']):
			self.log.debug ("is pdf like")
			if self.thumb_from_pdf (orginal_file + "[0]", preview_file):
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
			if self.thumb_from_zip (orginal_file, preview_file):
				return True
			
		# TODO:
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




def main():
	
	pythumb = PyThumb ()
	
	parser = argparse.ArgumentParser (description='PyThumb -- see https://github.com/binfalse/pythumb')
	
	parser.add_argument ('--max-width', nargs='?', dest='maxwidth', type=int, default=pythumb.default_thumb_width, help='max width of the thumbnail (default: ' + str (pythumb.default_thumb_width) + ')')
	parser.add_argument ('--max-height', nargs='?', dest='maxheight', type=int, default=pythumb.default_thumb_height, help='max height of the thumbnail (default: ' + str (pythumb.default_thumb_height) + ')')
	
	parser.add_argument ('--crop-width', nargs='?', dest='cropwidth', type=int, default=pythumb.default_crop_width, help='crop to this width before scaling the thumbnail, especially useful for very unproportional pictures or long websites (default: ' + str (pythumb.default_crop_width) + ')')
	parser.add_argument ('--crop-height', nargs='?', dest='cropheight', type=int, default=pythumb.default_crop_height, help='crop to this height before scaling the thumbnail, especially useful for very unproportional pictures or long websites (default: ' + str (pythumb.default_crop_height) + ')')
	
	parser.add_argument ('--font', nargs='?', dest='font', default=pythumb._font, help='font to use for manually generated thumbnails, only true type fonts are supported (default: ' + str (pythumb._font) + ')')
	
	parser.add_argument ('--verbose', action='store_true', default=False, help='print debugging information')
	
	parser.add_argument ('--website', dest='website', action='store_true', default=False, help='generate thumbnail of a website (not of a file)')
	
	parser.add_argument ('document', help="path to file or website for which you want to generate a thumbnail")
	parser.add_argument ('thumbnail', help="where to store the thumbnail? must be a non-exising file")
	
	
	
	
	args = parser.parse_args ()
	
	if args.verbose:
		print ("verbosity turned on")
		log.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger(__name__)
		tmplog.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger("pythumb.pythumb")
		tmplog.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger("pythumb")
		tmplog.setLevel(logging.DEBUG)
	
	pythumb.set_thumb_dimensions (int (args.maxwidth), int (args.maxheight))
	pythumb.set_crop_dimensions (int (args.cropwidth), int (args.cropheight))
	pythumb.set_font (args.font)
	
	if args.website:
		if pythumb.thumb_from_website (args.document, args.thumbnail):
			print ("successfully generated a thumbnail in " + args.thumbnail)
			sys.exit (0)
		else:
			print ("failed to generate a thumbnail of " + args.document)
			print ("try running with --verbose")
			sys.exit (1)
	else:
		if pythumb.thumb_from_file (args.document, args.thumbnail, os.path.basename (args.document)):
			print ("successfully generated a thumbnail in " + args.thumbnail)
			sys.exit (0)
		else:
			print ("failed to generate a thumbnail of " + args.document)
			print ("try running with --verbose")
			sys.exit (1)
	

if __name__ == '__main__':
	main()


