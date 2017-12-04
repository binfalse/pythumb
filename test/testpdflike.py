#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper



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
