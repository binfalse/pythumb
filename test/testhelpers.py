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

import os
import logging
from PIL import Image
import unittest
from shutil import copyfile
import sys
from pythumb.pythumb import PyThumb
import tempfile
import inspect

# unittest ref:
# https://docs.python.org/2/library/unittest.html#test-cases

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class TestHelper (unittest.TestCase):
	
	def setUp (self):
		if self.is_verbose ():
			tmplog = logging.getLogger("pythumb.pythumb")
			tmplog.setLevel(logging.DEBUG)
	
	# checks a thumbnail
	def _check_thumbnail (self, thumb, pythumb, thumb_width, thumb_height):
		self.assertTrue (os.path.exists (thumb), "did not find preview")
		size = os.path.getsize (thumb)
		self.assertFalse (size < 1000, "thumb size is too small: " + str (size) + "!?")
		
		if thumb_width <= 0:
			thumb_width = pythumb._thumb_width
		if thumb_height <= 0:
			thumb_height = pythumb._thumb_height
		
		with Image.open (thumb) as img:
			self.assertTrue (img.size[0] <= thumb_width, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
			self.assertTrue (img.size[1] <= thumb_height, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")
			self.assertTrue (img.size[0] == thumb_width or img.size[1] == thumb_height, "thumb dimensions are not as specified: " + str (img.size[0]) + "x" + str (img.size[1]) + "!? requested was: " + str (thumb_width) + "x" + str (thumb_height))

	def is_verbose (self):
		if ('-v' in sys.argv) or ('--verbose' in sys.argv):
			return True
		for i in sys.argv:
			if '--verbosity' in i:
				return True
		return False
	
	# fail: shoul we fail here? -> to print log and sysout etc
	def generate_and_verify_thumb (self, f, fail, thumb_width=-1, thumb_height=-1, filename="testname"):
		log.debug ("generating and verifying thumb: ")
		log.debug ("   f: " + str (f))
		log.debug ("   fail: " + str (fail))
		log.debug ("   thumb_width: " + str (thumb_width))
		log.debug ("   thumb_height: " + str (thumb_height))
		log.debug ("   filename: " + str (filename))

		pythumb = PyThumb ()
		
		if thumb_width > 0 or thumb_height > 0:
			pythumb.set_thumb_dimensions (thumb_width, thumb_height)
		
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			log.debug ("thumbnail will be written to: " + temp.name)
			os.remove (temp.name)
			if 'http' in f:
				log.debug ("this seems to be a website")
				self.assertTrue (pythumb.thumb_from_website (f, temp.name), "couldn't create thumbnail from " + f)
			else:
				log.debug ("this seems to be a file")
				self.assertTrue (os.path.exists (f), "cannot find " + f)
				self.assertTrue (pythumb.thumb_from_file (f, temp.name, filename), "couldn't create thumbnail from " + f)
			
			self.assertTrue (os.path.exists (temp.name), "thumb not generated: " + temp.name)
			
			if self.is_verbose():
				testresults='test-results/'
				if not os.path.exists(testresults):
					os.makedirs(testresults)
				frame = inspect.stack()[1]
				module = inspect.getmodule(frame[0])
				saveas = testresults + module.__name__ + "-" + str (frame[3]) + "-" + str (frame[2]) + ".png"
				log.debug ("storing resulting thumbnail as " + saveas)
				copyfile (temp.name, saveas)
			
			log.debug ("verifying thumbnail")
			self._check_thumbnail (temp.name, pythumb, thumb_width, thumb_height)
			
			if fail:
				log.debug ("will fail here as requested!")
				self.assertFalse (fail)
