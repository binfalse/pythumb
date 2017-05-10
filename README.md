# PyThumb

This will be a tool to create thumbnails for whatever.. ;-)

It is intented to run as a Docker container, as it has many dependencies...

in PNG format

## Requirements

* cutycapt
* libre office
* image magic
* ps2pdf


## Usage


### As a Library

pythumb 

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

To just run a single test you may just use the default [unittest module](https://docs.python.org/2/library/unittest.html):

    python -m unittest test.testepub

This will run all the tests defined in `test/testepub.py`.


## License

