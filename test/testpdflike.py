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
class TestPdfLike (unittest.TestCase):
	
	def test_one (self):
			f = "test/files/pdflike-1.pdf"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name)
	
	def test_two (self):
			f = "test/files/pdflike-2.pdf"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name)
	
	def test_three (self):
			f = "test/files/pdflike-3.djvu"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name)
	
	def test_four (self):
			f = "test/files/pdflike-4.ps"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				check_thumbnail (self, temp.name)
