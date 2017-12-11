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

from pythumb.server import WebHandler
from test.testhelpers import TestHelper
import tempfile
import os
import requests

import threading

# from http import server
# from io import BytesIO as IO
from http.server import HTTPServer

HOST='127.0.0.1'
PORT=9753
SERVER='http://' + HOST + ":" + str (PORT)


class TestServer (TestHelper):
	@classmethod
	def setUpClass (self):
		server = HTTPServer ((HOST, PORT), WebHandler)
		httpd_thread = threading.Thread (target=server.serve_forever)
		httpd_thread.daemon = True
		httpd_thread.start()
		
	def test_default (self):
		response = requests.post (SERVER, files=dict (file=open ('test/files/pdflike-2.pdf', 'rb')), data=dict (target='upload', filename='main.pdf'))
		self.assertEqual (response.status_code, 200, "expected an HTTP status 200")
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			temp.write(response.content)
			self._check_thumbnail (temp.name, None, 300, 300)
		
	def test_larger (self):
		response = requests.post (SERVER, files=dict (file=open ('test/files/pdflike-2.pdf', 'rb')), data=dict (target='upload', filename='main.pdf', maxwidth="600", maxheight="600"))
		self.assertEqual (response.status_code, 200, "expected an HTTP status 200")
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			temp.write(response.content)
			self._check_thumbnail (temp.name, None, 600, 600)
	
	def test_remote (self):
		response = requests.post (SERVER, files=dict (target='https://binfalse.de/'))
		self.assertEqual (response.status_code, 200, "expected an HTTP status 200")
		with tempfile.NamedTemporaryFile (suffix='.png') as temp:
			temp.write(response.content)
			self._check_thumbnail (temp.name, None, -1, -1)
	
	def test_missing_target (self):
		try:
			response = requests.post (SERVER, files=dict (target2='https://binfalse.de/'))
			self.fail ("expected an HTTP status 200")
		except:
			pass
	
	
	
	