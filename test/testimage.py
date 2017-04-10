#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import unittest
import os
import tempfile
import logging
from PIL import Image
from testhelpers import check_thumbnail



# test image files
class TestImage (unittest.TestCase):
	
	def test_one (self):
			f = "test/files/image-3.png"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_two (self):
			f = "test/files/image-4.svg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_three (self):
			f = "test/files/image-2.jpg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)
	
	def test_four (self):
			f = "test/files/image-1.jpeg"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				check_thumbnail (self, temp.name)


