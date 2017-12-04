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
class TestOffice (unittest.TestCase):
	
	def test_one (self):
			pythumb = PyThumb ()
			f = "test/files/office-1.doc"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-1.png")
				check_thumbnail (self, temp.name, pythumb)
	
	def test_two (self):
			pythumb = PyThumb ()
			f = "test/files/office-2.docx"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-2.png")
				check_thumbnail (self, temp.name, pythumb)
	
	def test_three (self):
			pythumb = PyThumb ()
			f = "test/files/office-3.ods"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-3.png")
				check_thumbnail (self, temp.name, pythumb)
	
	def test_four (self):
			pythumb = PyThumb ()
			f = "test/files/office-4.odt"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-4.png")
				check_thumbnail (self, temp.name, pythumb)
	
	def test_five (self):
			pythumb = PyThumb ()
			f = "test/files/office-5.xls"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-5.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_six (self):
			pythumb = PyThumb ()
			f = "test/files/office-6.xlsx"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-6.png")
				#self.assertTrue (False)
				check_thumbnail (self, temp.name, pythumb)
	
	def test_seven (self):
			pythumb = PyThumb ()
			f = "test/files/office-7.odp"
			self.assertTrue (os.path.exists (f), "cannot find " + f)
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from " + f)
				copyfile (temp.name, "/tmp/pythumb-office-7.png")
				check_thumbnail (self, temp.name, pythumb)
