#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import unittest
import os
import tempfile
import logging

# unittest ref:
# https://docs.python.org/2/library/unittest.html#test-cases

logging.basicConfig()
log = logging.getLogger("pythumb.pythumb")
log.setLevel(logging.DEBUG)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

## Change logging level here.


# test the epub files
class TestEpub (unittest.TestCase):
	# checks for a thumbnail
	def check_thumbnail (self, thumb):
		self.failUnless (os.path.exists (thumb), "did not find preview")
		self.failUnless (os.path.getsize (thumb) > 100)
		## TODO: check thumbnail size
	
	def testOne (self):
			log.info ("\ntest one")
			f = "test/files/test-1.epub"
			self.failUnless (os.path.exists (f), "cannot find first epub")
			with tempfile.NamedTemporaryFile (suffix='.png') as temp:
				os.remove (temp.name)
				self.failUnless (pythumb.thumb_from_file (f, temp.name, "testname"), "couldn't create thumbnail from epub")
				self.check_thumbnail (temp.name)

