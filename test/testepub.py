#!/usr/bin/env python
# encoding=utf8

from testhelpers import TestHelper


# test the epub files
class TestEpub (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/book-1.epub", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/book-2.epub", False)
	
	def test_set_size (self):
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 50, 50)
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 500, 500)
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 600, 300)

