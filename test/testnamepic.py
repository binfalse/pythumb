#!/usr/bin/env python
# encoding=utf8

from pythumb.pythumb import PyThumb
import unittest
import os
import tempfile
import logging
from PIL import Image
from testhelpers import check_thumbnail


# test image files
class TestNamePic (unittest.TestCase):
	
	def test_one (self):
			pythumb = PyThumb ()
			f = "test/files/office-3.ods"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_two (self):
			pythumb = PyThumb ()
			f = "test/files/office-3.ods"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_three (self):
			pythumb = PyThumb ()
			f = "test/files/office-3.ods"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "Loremipsumdolorsitamet,consectetur adipiscingelit,seddoeiusmod tempor incididunt ut labore et dolore magna aliqua."), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_four (self):
			pythumb = PyThumb ()
			f = "test/files/office-3.ods"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name, pythumb)

