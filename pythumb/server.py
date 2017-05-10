#!/usr/bin/env python
# encoding=utf8
import string
import cgi
import time
import argparse
import re
import os
import sys
import pythumb
import traceback
import tempfile
import logging
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


logging.basicConfig()
log = logging.getLogger("pythumb.pythumb")
log.setLevel(logging.DEBUG)
log = logging.getLogger("pythumb")
log.setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



ALLOW_UPLOAD = True
ALLOW_REMOTE = True
_url_regex = re.compile (r'^https?://', flags=re.IGNORECASE)

class WebHandler (BaseHTTPRequestHandler):
	def do_GET (self):
		self.send_response (200)
		self.send_header ('Content-type',	'text/html')
		self.end_headers ()
		self.wfile.write ("""
<!DOCTYPE html>
<html><head><title>PyThumb</title></head>
<body>
test
</body>
</html>
""")
		return
	
	def send_error (self, title, message, status=400):
		print ("ERROR: " + title + "\n" + message)
		self.send_response (status)
		self.send_header ('Content-type',	'text/html')
		self.wfile.write ("""
<!DOCTYPE html>
<html><head><title>PyThumb Error</title></head>
<body>
<h1>ERROR</h1>
something went wrong with your upload...
<h3>""" + title + "</h3><pre>" + message + """</pre>
</body>
</html>
""")
	
	def serve_thumb (self, thumbnail):
		with open (thumbnail, 'rb') as fh:
			self.send_response (200)
			self.send_header ('Content-type', 'image/png')
			self.end_headers ()
			self.wfile.write (fh.read ())
	
	def do_POST (self):
		try:
			ctype, pdict = cgi.parse_header (self.headers.getheader ('content-type'))
			
			if ctype == 'multipart/form-data':
				query = cgi.parse_multipart (self.rfile, pdict)
				target = query.get ('target', 'invalid')
				if isinstance (target, list):
					target = target[0]
				
				#print (target)
				
				if target == 'invalid':
					self.send_error ("Upload failed", "expected a target")
					return
				
				if target == 'upload':
					if not ALLOW_UPLOAD:
						self.send_error ("Upload disabled", "This server has the upload mechanism disabled.")
						return
					
					filename = query.get ('filename', 'file')
					if isinstance (filename, list):
						filename = filename[0]
					
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
				
				if _url_regex.match(target):
					if not ALLOW_REMOTE:
						self.send_error ("Remote thumbs disabled", "The feature for generating thumbnails of remote websites has been disabled in this server.")
						return
					
					with tempfile.NamedTemporaryFile (suffix='.png') as temp:
						if pythumb.thumb_from_website (target, temp.name):
							self.serve_thumb (temp.name)
							return
					self.send_error ("Error generating thumbnail", "there was an error generating the thumbnail", 500)
				
				self.send_error ("Invalid request", "do not understand target: " + target)
				
			else:
				self.send_error ("Upload failed", "expected multipart/form-data")
				
				#upfilecontent = query.get('upfile')
				#print "filecontent", upfilecontent[0]
				#self.wfile.write(upfilecontent[0]);
			
		except:
			#e = sys.exc_info()[0]
			#print (traceback.print_stack())
			#print (e)
			tb = traceback.format_exc()
			print tb
			self.send_error ("Upload failed", "exception raised")


def main():
	
	parser = argparse.ArgumentParser (description='PyThumb Webserver -- see https://github.com/binfalse/pythumb')
	
	parser.add_argument ('--port', nargs='?', default=80, type=int, help='TCP port of the web server (default: 80)')
	parser.add_argument ('--ip', nargs='?', default='0.0.0.0', help='IP address of the web server (default: 0.0.0.0)')
	
	parser.add_argument ('--no-upload', dest='noupload', action='store_true', default=False, help='disable file upload')
	parser.add_argument ('--no-remote', dest='noremote', action='store_true', default=False, help='disable thumbnails of remote websites')
	
	args = parser.parse_args ()
	
	ALLOW_UPLOAD = not args.noupload
	ALLOW_REMOTE = not args.noremote
	
	try:
		server = HTTPServer ((args.ip, args.port), WebHandler)
		print 'started server...'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'killing server...'
		server.socket.close()

if __name__ == '__main__':
	main()
