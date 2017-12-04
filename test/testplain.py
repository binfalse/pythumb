#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper

# test image files
class TestPlain (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/plain-1.txt", False)
				
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/plain-2.txt", False)
				
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/plain-3.txt", False)
				
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/plain-4.txt", False)
				
	def test_five (self):
		self.generate_and_verify_thumb ("test/files/plain-5.txt", False)
				
	def test_six (self):
		self.generate_and_verify_thumb ("test/files/plain-6.txt", False)
				
