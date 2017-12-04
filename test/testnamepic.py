#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper


# test image files
class TestNamePic (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/office-3.ods", False, filename="testname")
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/office-3.ods", False, filename="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
	
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/office-3.ods", False, filename="Loremipsumdolorsitamet,consectetur adipiscingelit,seddoeiusmod tempor incididunt ut labore et dolore magna aliqua.")
	
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/office-3.ods", False, filename="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed")

