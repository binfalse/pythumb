# PyThumb

This will be a tool to create thumbnails for whatever.. ;-)

It is intented to run as a Docker container, as it has many dependencies...

key features:
* several formats
* as library or web application
* docker
* thus available for multiple languages (not just python!!)

supported formats:
* zip (will try to find images in the zip and use the one that has 'cover' in its name, or the largest image)

output always in PNG format




## Requirements

* cutycapt
* libre office
* image magic
* ps2pdf
* python-magic


## Usage


### As a Library

pythumb 

general version: thumb from file


special functions -> thumb from zip etc
may fail (return false)
then use thumb from name

### As Executable



### As a web server

you can run a tiny web server that generates the thumbnails

options:


* `--ip` the IP address of the web server. Default is `0.0.0.0`, which will listen to all available address. Use `127.0.0.1` to just listen to localhost.


does not support SSL -- use proxies such as nginx

from website:

    curl -v -F target=https://binfalse.de  localhost:12346 > /tmp/thumb.png

from file:



--max-witdh --max-height

### Through Docker

TODO

## Running Tests

There are a number of tests shipped with that repository. You can find them in the [`test/` directory](`test/`).
The easiest way to run all the tests is to install [python-nose](https://nose.readthedocs.io/en/latest/) and just run

    nosetests

from the root directory of this repository. python-nose will discover and run all the tests.


Run `nosetests` with enhanced verbosity to find the resulting files in a newly created `/test-results/` directory:

    nosetests -v

The resulting files will be named as `test.module-test_method-linenumber.png`.


To get more information about the runs even if they all succeeded you may want to run 

    nosetests -v --nologcapture --nocapture

To just run a single test you may just use the default [unittest module](https://docs.python.org/2/library/unittest.html):

    python -m unittest test.testepub

or call `nosetests` with the test-file as an argument:

    nosetests test/testepub.py


This will run all the tests defined in `test/testepub.py`.


To see the code-coverage of the unit tests run `nosetests` with the following arguments:

	nosetests --with-coverage --cover-erase --cover-package=pythumb --cover-html

This will show an output such as:

	Name                  Stmts   Miss  Cover   Missing
	---------------------------------------------------
	pythumb/__init__.py       8      4    50%   6-9
	pythumb/pythumb.py      310     18    94%   167, 196-197, 336-338, 355-357, 373-374, 381, 443-444, 452-453, 543, 554
	---------------------------------------------------
	TOTAL                   318     22    93%
	----------------------------------------------------------------------
	Ran 44 tests in 38.982s

	OK


Thus, here we have a code-coverage of 94%, which is probably in the meantime much higher ;-)

A detailed coverage report will then be available in `cover/index.html`.

## License

	PyThumb is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with PyThumb.  If not, see <http://www.gnu.org/licenses/>.

