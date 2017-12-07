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

import os
import tempfile
from pythumb.pythumb import PyThumb


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
	
	def test_five (self):
		# check error of convert
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp2:
				os.remove (temp1.name)
				os.remove (temp2.name)
				try:
					pythumb.thumb_from_image (temp1.name, temp2.name)
					self.fail ("no convert error for nonexisting file?")
				except IOError:
					pass


