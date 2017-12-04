#!/usr/bin/env python
# encoding=utf8

from pythumb.pythumb import PyThumb
import unittest
import os
import tempfile
import logging
from PIL import Image
from testhelpers import check_thumbnail
from shutil import copyfile


# test image files
class TestPlain (unittest.TestCase):
	
	def test_one (self):
			pythumb = PyThumb ()
			f = "test/files/plain-1.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-1.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
	def test_two (self):
			pythumb = PyThumb ()
			f = "test/files/plain-2.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-2.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
	def test_three (self):
			pythumb = PyThumb ()
			f = "test/files/plain-3.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-3.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
	def test_four (self):
			pythumb = PyThumb ()
			f = "test/files/plain-4.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-4.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
	def test_five (self):
			pythumb = PyThumb ()
			f = "test/files/plain-5.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-5.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
	def test_six (self):
			pythumb = PyThumb ()
			f = "test/files/plain-6.txt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				#copyfile (temp.name, "/tmp/pythumb-plain-6.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
				
