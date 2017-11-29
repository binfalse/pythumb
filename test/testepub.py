#!/usr/bin/env python
# encoding=utf8

from pythumb.pythumb import PyThumb
import unittest
import os
import tempfile
import logging
from PIL import Image
from testhelpers import check_thumbnail

# unittest ref:
# https://docs.python.org/2/library/unittest.html#test-cases

#logging.basicConfig()
#log = logging.getLogger("pythumb.pythumb")
#log.setLevel(logging.DEBUG)


#log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

# test the epub files
class TestEpub (unittest.TestCase):
	
	def test_one (self):
			pythumb = PyThumb ()
			f = "test/files/book-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_two (self):
			pythumb = PyThumb ()
			f = "test/files/book-2.epub"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_set_size (self):
			pythumb = PyThumb ()
			f = "test/files/book-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				pythumb.set_thumb_dimensions (50, 50)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				# restore original dimensions
				pythumb.set_thumb_dimensions (pythumb.default_thumb_width, pythumb.default_thumb_height)
				check_thumbnail (self, temp.name, pythumb)
				# extra checks for smaller thumbnail
				with Image.open (temp.name) as img:
					self.assertTrue (img.size[0] <= 50, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
					self.assertTrue (img.size[1] <= 50, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")

