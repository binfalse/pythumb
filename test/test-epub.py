#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import unittest
import os
import tempfile

# unittest ref:
# https://docs.python.org/2/library/unittest.html#test-cases



# test the epub files
class TestEpub (unittest.TestCase):
	# checks for a thumbnail
	def check_thumbnail (self, thumb):
		self.assertTrue (os.path.exists (thumb), "did not find preview")
		self.assertTrue (os.path.getsize (thumb) > 100)
	
	def testOne (self):
			f = "test/files/test-1.epub"
			self.assertTrue (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				self.assertTrue (pythumb.thumb_from_file (f, temp, "testname"), "couldn't create thumbnail from epub")
				self.check_thumbnail (temp)
