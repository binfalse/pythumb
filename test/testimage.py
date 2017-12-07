#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper

import os
import tempfile
from pythumb.pythumb import PyThumb


# test image files
class TestImage (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/image-1.jpeg", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/image-2.jpg", False)
	
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/image-3.png", False)
	
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/image-4.svg", False)
	
	def test_five (self):
		# check error of convert
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp2:
				os.remove (temp1.name)
				os.remove (temp2.name)
				try:
					pythumb.thumb_from_image (temp1.name, temp2.name)
					self.fail ("no convert error for nonexisting file?")
				except IOError, e:
					pass


