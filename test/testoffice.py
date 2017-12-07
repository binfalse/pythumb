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
