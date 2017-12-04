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
			
