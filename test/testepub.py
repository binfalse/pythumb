#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import unittest
import os
import tempfile
import logging
from PIL import Image

# unittest ref:
# https://docs.python.org/2/library/unittest.html#test-cases

logging.basicConfig()
log = logging.getLogger("pythumb.pythumb")
log.setLevel(logging.DEBUG)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

## Change logging level here.


# test the epub files
class TestEpub (unittest.TestCase):
	# checks for a thumbnail
	def check_thumbnail (self, thumb):
		self.assertTrue (os.path.exists (thumb), "did not find preview")
		size = os.path.getsize (thumb)
		self.assertFalse (size < 1000, "thumb size is too small: " + str (size) + "!?")
		with Image.open (thumb) as img:
			print (img.size)
			self.assertTrue (img.size[0] <= pythumb.default_thumb_width, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
			self.assertTrue (img.size[1] <= pythumb.default_thumb_height, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")
	
	def test_one (self):
			log.info ("")
			f = "test/files/test-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				self.check_thumbnail (temp.name)
	
	def test_two (self):
			log.info ("")
			f = "test/files/test-2.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				self.check_thumbnail (temp.name)
	
	def test_set_size (self):
			log.info ("")
			f = "test/files/test-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				pythumb.set_thumb_dimensions (50, 50)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				# restore original dimensions
				pythumb.set_thumb_dimensions (pythumb.default_thumb_width, pythumb.default_thumb_height)
				self.check_thumbnail (temp.name)
				# extra checks for smaller thumbnail
				with Image.open (temp.name) as img:
					self.assertTrue (img.size[0] <= 50, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
					self.assertTrue (img.size[1] <= 50, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")

