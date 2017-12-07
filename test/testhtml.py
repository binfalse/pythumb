#!/usr/bin/env python
# encoding=utf8

from testhelpers import TestHelper

import os
import tempfile
from pythumb.pythumb import PyThumb


# test image files
class TestHtml (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/html-1/index.html", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("https://binfalse.de", False)
	
	def test_three (self):
		# smaller website
		self.generate_and_verify_thumb ("https://binfalse.de/contact/", False)
	
	def test_four (self):
		# wider website
		self.generate_and_verify_thumb ("https://binfalse.de/assets/media/pics/2016/automatic-os-update.svg", False)
	
	def test_five (self):
		# check fail of invalid url
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			os.remove (temp1.name)
			self.assertFalse (pythumb.thumb_from_website ("htttps://binfalse.den", temp1.name))
	
	