# PyThumb

This will be a tool to create thumbnails for whatever.. ;-)

It is intented to run as a Docker container, as it has many dependencies...

## Requirements

* cutycapt
* libre office
* image magic
* ps2pdf


## Usage


### As a Library

pythumb 

### As Executable



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

