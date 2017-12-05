#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper

import os
import tempfile
from pythumb.pythumb import PyThumb


# test image files
class TestPdfLike (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/pdflike-1.pdf", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/pdflike-2.pdf", False)
	
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/pdflike-3.djvu", False)
	
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/pdflike-4.ps", False)
	
	def test_five (self):
		self.generate_and_verify_thumb ("test/files/pdflike-5.eps", False)

	def test_six (self):
		# check ps2pdf error
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp2:
				os.remove (temp1.name)
				os.remove (temp2.name)
				self.assertFalse (pythumb.thumb_from_postscript (temp1.name, temp2.name), "no ps2pdf error for nonexisting file?")
