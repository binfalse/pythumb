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

import cgi
import argparse
import re
import os
from pythumb import PyThumb
import traceback
import tempfile
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from shutil import copyfile

logging.basicConfig()
log = logging.getLogger(__name__)



ALLOW_UPLOAD = True
ALLOW_REMOTE = True
_url_regex = re.compile (r'^https?://', flags=re.IGNORECASE)

class WebHandler (BaseHTTPRequestHandler):
	def do_GET (self):
		self.send_response (200)
		self.send_header ('Content-type',	'text/html')
		self.end_headers ()
		help_text = """
<!DOCTYPE html>
<html><head><title>PyThumb</title></head>
<body>
test
</body>
</html>
"""
		self.wfile.write (help_text.encode ())
		return
	
	def send_error (self, title, message, status=400):
		print ("ERROR: " + title + "\n" + message)
		self.send_response (status)
		self.send_header ('Content-type',	'text/html')
		output = """
<!DOCTYPE html>
<html><head><title>PyThumb Error</title></head>
<body>
<h1>ERROR</h1>
something went wrong...
<h3>""" + title + "</h3><pre>" + message + """</pre>
</body>
</html>
"""
		self.wfile.write (output.encode())
	
	def serve_thumb (self, thumbnail):
		with open (thumbnail, 'rb') as fh:
			self.send_response (200)
			self.send_header ('Content-type', 'image/png')
			self.end_headers ()
			self.wfile.write (fh.read ())
	
	def parse_dimension (self, val):
		log.debug ("parsing dimension: " + str (val))
		if val:
			if isinstance (val, list):
					val = val[0]
			try:
				return int (val.decode ())
			except:
				log.debug ("exception when parsing dimension")
				return -1
			
		log.debug ("val is not valid?")
		return -1
	
	def do_POST (self):
		try:
			ctype, pdict = cgi.parse_header (self.headers['content-type'])
			if ctype == 'multipart/form-data':
				pdict['boundary'] = bytes (pdict['boundary'], "utf-8")
				query = cgi.parse_multipart (self.rfile, pdict)
				
				maxwidth = self.parse_dimension (query.get ('maxwidth', b'-1'))
				maxheight = self.parse_dimension (query.get ('maxheight', b'-1'))
				target = query.get ('target', b'invalid')
				if isinstance (target, list):
					target = target[0]
				
				target = target.decode ()
				if target == 'invalid':
					self.send_error ("Upload failed", "expected a target")
					return
				
				pythumb = PyThumb ()
				pythumb.set_thumb_dimensions (maxwidth, maxheight)
				
				if target == 'upload':
					if not ALLOW_UPLOAD:
						self.send_error ("Upload disabled", "This server has the upload mechanism disabled.")
						return
					
					filename = query.get ('filename', b'file')
					if isinstance (filename, list):
						filename = filename[0]
					filename = filename.decode ()
					
					content = query.get ('file', 'invalid')
					if isinstance (content, list):
						content = content[0]
					
					if content == 'invalid':
						self.send_error ("Upload failed", "did not find a file")
						return
					
					
					with tempfile.NamedTemporaryFile (suffix=filename) as orig:
						with tempfile.NamedTemporaryFile (suffix='.png') as temp:
							os.remove (temp.name)
							with open (orig.name, 'wb') as fh:
								fh.write (content)
							
							if pythumb.thumb_from_file (orig.name, temp.name, filename):
								self.serve_thumb (temp.name)
								return
					
					self.send_error ("Error generating thumbnail", "there was an error generating the thumbnail", 500)
					
					return
				
				if _url_regex.match (target):
					if not ALLOW_REMOTE:
						self.send_error ("Remote thumbnails disabled", "The feature for generating thumbnails of remote websites has been disabled in this instance.")
						return
					
					with tempfile.NamedTemporaryFile (suffix='.png') as temp:
						if pythumb.thumb_from_website (target, temp.name):
							self.serve_thumb (temp.name)
							return
					self.send_error ("Error generating thumbnail", "there was an error generating the thumbnail", 500)
				
				self.send_error ("Invalid request", "do not understand target: " + target)
		        
			else:
				self.send_error ("Upload failed", "expected multipart/form-data")
	
		except:
			tb = traceback.format_exc ()
			print (tb)
			self.send_error ("Upload failed", "exception raised")



def main():
	
	parser = argparse.ArgumentParser (description='PyThumb Webserver -- see https://github.com/binfalse/pythumb')
	
	parser.add_argument ('--port', nargs='?', default=80, type=int, help='TCP port of the web server (default: 80)')
	parser.add_argument ('--ip', nargs='?', default='0.0.0.0', help='IP address of the web server (default: 0.0.0.0)')
	
	parser.add_argument ('--verbose', action='store_true', default=False, help='print debugging information')
	
	parser.add_argument ('--no-upload', dest='noupload', action='store_true', default=False, help='disable file upload')
	parser.add_argument ('--no-remote', dest='noremote', action='store_true', default=False, help='disable thumbnails of remote websites')
	
	
	
	args = parser.parse_args ()
	
	if args.verbose:
		print ("verbosity turned on")
		log.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger(__name__)
		tmplog.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger("pythumb.pythumb")
		tmplog.setLevel(logging.DEBUG)
		
		tmplog = logging.getLogger("pythumb")
		tmplog.setLevel(logging.DEBUG)
	
	
	ALLOW_UPLOAD = not args.noupload
	ALLOW_REMOTE = not args.noremote
	
	try:
		server = HTTPServer ((args.ip, args.port), WebHandler)
		print ('started server...')
		server.serve_forever()
	except KeyboardInterrupt:
		print ('killing server...')
		server.socket.close()

if __name__ == '__main__':
	main()
