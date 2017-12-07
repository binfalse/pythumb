#!/usr/bin/env python
# encoding=utf8
#
# This file is part of PyThumb.
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
class TestHtml (TestHelper):
	
	def test_one (self):
		self.generate_and_verify_thumb ("test/files/html-1/index.html", False)
	
	def test_two (self):
		self.generate_and_verify_thumb ("https://binfalse.de", False)
	
	def test_three (self):
		# smaller website
		self.generate_and_verify_thumb ("https://binfalse.de/contact/", False)
	
	def test_four (self):
		# wider website
		self.generate_and_verify_thumb ("https://binfalse.de/assets/media/pics/2016/automatic-os-update.svg", False)
	
	def test_five (self):
		# check fail of invalid url
		pythumb = PyThumb ()
		with tempfile.NamedTemporaryFile (suffix='.png', delete=False) as temp1:
			os.remove (temp1.name)
			self.assertFalse (pythumb.thumb_from_website ("htttps://binfalse.den", temp1.name))
	
	