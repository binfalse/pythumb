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


## License

