#!/usr/bin/env python
# encoding=utf8

from pythumb.pythumb import PyThumb
from testhelpers import TestHelper
import tempfile
import os



class TestStuff (TestHelper):
	
	def file_ext_checker (self, pythumb, filename, wo_ext, ext):
		
		print (filename)
		got_wo_ext = pythumb._get_file_name_wo_ext (filename)
		got_ext = pythumb._get_file_ext (filename)
		
		print (got_wo_ext)
		print (got_ext)
		
		self.assertEqual (got_wo_ext, wo_ext, "did not manage to get filename correctly: " + got_wo_ext + " != " + wo_ext)
		self.assertEqual (got_ext, ext, "did not manage to get file extension correctly: " + got_ext + " != " + ext)
	
	
	def test_file_ext (self):
		pythumb = PyThumb ()
		
		self.file_ext_checker (pythumb, "file.name", "file", ".name")
		self.file_ext_checker (pythumb, "/tmp/file.name.tar.gz", "file.name.tar", ".gz")
		self.file_ext_checker (pythumb, "/tmp/file", "file", "")
		self.file_ext_checker (pythumb, "/tmp/", "", "")
		
	def test_checks (self):
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
			
			# make sure we do not overwrite an existing file
			f = "test/files/image-1.jpeg"
			self.assertFalse (pythumb.thumb_from_file (f, temp.name, "testname"), "would overwrite file???")
			
			# remove file and make sure it now works
			os.remove (temp.name)
			self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "cannot create thumbnail of " + f)
			
			
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp2:
				os.remove (temp.name)
				os.remove (temp2.name)
				# make sure it fails to generate thumbnail of non-existing file
				self.assertFalse (pythumb.thumb_from_file (temp.name, temp2.name, "testname"), "how could it create a thumb of a non-existing file?")
				
			
			
	def test_thumb_dimensions (self):
		pythumb = PyThumb ()
		
		pythumb.set_thumb_dimensions (300, 300)
		self.assertEqual (pythumb._thumb_width, 300, "wasn't able to update the thumb width")
		self.assertEqual (pythumb._thumb_height, 300, "wasn't able to update the thumb height")
		
		pythumb.set_thumb_dimensions (500, 600)
		self.assertEqual (pythumb._thumb_width, 500, "wasn't able to update the thumb width")
		self.assertEqual (pythumb._thumb_height, 600, "wasn't able to update the thumb height")
		
		pythumb.set_thumb_dimensions (0, -1)
		self.assertTrue (pythumb._thumb_width > 0, "thumb with is not >0")
		self.assertTrue (pythumb._thumb_height > 0, "thumb height is not >0")
		
		pythumb.set_thumb_dimensions (-1, 0)
		self.assertTrue (pythumb._thumb_width > 0, "thumb with is not >0")
		self.assertTrue (pythumb._thumb_height > 0, "thumb height is not >0")
		
		pythumb.set_thumb_dimensions (100, -5)
		self.assertTrue (pythumb._thumb_width > 0, "thumb with is not >0")
		self.assertTrue (pythumb._thumb_height > 0, "thumb height is not >0")
		
		pythumb.set_thumb_dimensions (-5, 100)
		self.assertTrue (pythumb._thumb_width > 0, "thumb with is not >0")
		self.assertTrue (pythumb._thumb_height > 0, "thumb height is not >0")
