#!/usr/bin/env python
# encoding=utf8
#
# Copyright 2017 Martin Scharm <https://binfalse.de/contact/>
#
# This file is part of PyThumb.
# <https://github.com/binfalse/pythumb/>
# 
# PyThumb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyThumb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyThumb.  If not, see <http://www.gnu.org/licenses/>.

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
	
	def test_font (self):
		pythumb = PyThumb ()
		pythumb.set_font ("stuff")
		self.assertEqual ("stuff", pythumb._font, "didn't manage to replace font")
		
		
	
	def test_checks (self):
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp:
			
			# make sure we do not overwrite an existing file
			f = "test/files/image-1.jpeg"
			self.assertFalse (pythumb.thumb_from_file (f, temp.name, "testname"), "would overwrite file???")
			
			# set to overwrite!
			pythumb.set_overwrite_thumb (True)
			# can we now thumbnail it?
			self.assertTrue (pythumb.thumb_from_file (f, temp.name, "testname"), "would overwrite file???")
			
			# revert and make sure it fails again
			pythumb.set_overwrite_thumb (False)
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
