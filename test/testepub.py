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


# checks a thumbnail
def check_thumbnail (tester, thumb):
	tester.assertTrue (os.path.exists (thumb), "did not find preview")
	size = os.path.getsize (thumb)
	tester.assertFalse (size < 1000, "thumb size is too small: " + str (size) + "!?")
	with Image.open (thumb) as img:
		tester.assertTrue (img.size[0] <= pythumb.default_thumb_width, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
		tester.assertTrue (img.size[1] <= pythumb.default_thumb_height, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")


# test the epub files
class TestEpub (unittest.TestCase):
	
	def test_one (self):
			log.info ("")
			f = "test/files/book-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_two (self):
			log.info ("")
			f = "test/files/book-2.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_set_size (self):
			log.info ("")
			f = "test/files/book-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				pythumb.set_thumb_dimensions (50, 50)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				# restore original dimensions
				pythumb.set_thumb_dimensions (pythumb.default_thumb_width, pythumb.default_thumb_height)
				check_thumbnail (self, temp.name)
				# extra checks for smaller thumbnail
				with Image.open (temp.name) as img:
					self.assertTrue (img.size[0] <= 50, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
					self.assertTrue (img.size[1] <= 50, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")


# test the epub files
class TestImage (unittest.TestCase):
	
	def test_one (self):
			log.info ("")
			f = "test/files/image-3.png"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_two (self):
			log.info ("")
			f = "test/files/image-4.svg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_three (self):
			log.info ("")
			f = "test/files/image-2.jpg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_four (self):
			log.info ("")
			f = "test/files/image-1.jpeg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)

