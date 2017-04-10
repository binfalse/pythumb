#!/usr/bin/env python
# encoding=utf8

from pythumb import pythumb
import os
import logging
from PIL import Image


# checks a thumbnail
def check_thumbnail (tester, thumb):
	tester.assertTrue (os.path.exists (thumb), "did not find preview")
	size = os.path.getsize (thumb)
	tester.assertFalse (size < 1000, "thumb size is too small: " + str (size) + "!?")
	with Image.open (thumb) as img:
		tester.assertTrue (img.size[0] <= pythumb.default_thumb_width, "thumb width is unexpectedly large: " + str (img.size[0]) + "!?")
		tester.assertTrue (img.size[1] <= pythumb.default_thumb_height, "thumb height is unexpectedly large: " + str (img.size[1]) + "!?")
