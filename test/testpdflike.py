#!/usr/bin/env python3
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

import os
import tempfile
from pythumb.pythumb import PyThumb


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

	def test_six (self):
		# check ps2pdf error
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp2:
				os.remove (temp1.name)
				os.remove (temp2.name)
				self.assertFalse (pythumb.thumb_from_postscript (temp1.name, temp2.name), "no ps2pdf error for nonexisting file?")
