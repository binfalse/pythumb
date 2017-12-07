#!/usr/bin/env python
# encoding=utf8
#
# Copyright 2017 Martin Scharm <https://binfalse.de/contact/>
#
# This file is part of PyThumb.
# <https://github.com/binfalse/pythumb/>
# 
# PyThumb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyThumb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyThumb.  If not, see <http://www.gnu.org/licenses/>.

from test.testhelpers import TestHelper


# test the epub files
class TestEpub (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/book-1.epub", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("test/files/book-2.epub", False)
	
	def test_three (self):
		self.generate_and_verify_thumb ("test/files/book-wo-cover-in-opf.epub", False)
	
	def test_four (self):
		self.generate_and_verify_thumb ("test/files/book-wo-meta-cover.epub", False)
	
	def test_five (self):
		self.generate_and_verify_thumb ("test/files/book-wo-cover.epub", False)
	
	def test_six (self):
		self.generate_and_verify_thumb ("test/files/book-wo-images.epub", False)
	
	def test_set_size (self):
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 50, 50)
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 500, 500)
		self.generate_and_verify_thumb ("test/files/book-1.epub", False, 600, 300)

