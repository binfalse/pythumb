#!/usr/bin/env python
# encoding=utf8

from testhelpers import TestHelper



# test image files
class TestOffice (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/office-1.doc", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/office-2.docx", False)
	
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/office-3.ods", False)
	
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/office-4.odt", False)
	
	def test_five (self):
		self.generate_and_verify_thumb ("test/files/office-5.xls", False)
	
	def test_six (self):
		self.generate_and_verify_thumb ("test/files/office-6.xlsx", False)
	
	def test_seven (self):
		self.generate_and_verify_thumb ("test/files/office-7.odp", False)
