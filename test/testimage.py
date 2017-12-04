#!/usr/bin/env python
# encoding=utf8


from testhelpers import TestHelper



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


