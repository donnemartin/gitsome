Installation
============

### Pip Installation

[![PyPI version](https://badge.fury.io/py/gitsome.svg)](http://badge.fury.io/py/gitsome) [![PyPI](https://img.shields.io/pypi/pyversions/gitsome.svg)](https://pypi.python.org/pypi/gitsome/)

`gitsome` is hosted on [PyPI](https://pypi.python.org/pypi/gitsome).  The following command will install `gitsome`:

    $ pip install gitsome

You can also install the latest `gitsome` from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/donnemartin/gitsome.git

If you are not installing in a virtualenv, run with `sudo`:

    $ sudo pip install gitsome

#### `pip3`

Depending on your system, you might need to run `pip3`, possibly with the `-H` flag:

    $ sudo -H pip3 install gitsome

See this [ticket](https://github.com/donnemartin/gitsome/issues/4) for more details.

#### Starting the `gitsome` Shell

Once installed, run the optional `gitsome` autocompleter with interactive help:

    $ gitsome

Running the optional `gitsome` shell will provide you with autocompletion, interactive help, fish-style suggestions, a Python REPL, etc.

#### Running `gh` Commands

Run GitHub-integrated commands:

    $ gh <command> [param] [options]

Note: Running the `gitsome` shell is not required to execute `gh` commands.  After [installing](#installation) `gitsome` you can run `gh` commands from any shell.

## Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential issues with dependencies or permissions.

If you are a Windows user or if you would like more details on `virtualenv`, check out this [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install `virtualenv` and `virtualenvwrapper`:

    $ pip install virtualenv
    $ pip install virtualenvwrapper
    $ export WORKON_HOME=~/.virtualenvs
    $ source /usr/local/bin/virtualenvwrapper.sh

Create a `gitsome` `virtualenv` and install `gitsome`:

    $ mkvirtualenv gitsome
    $ pip install gitsome

If that does not work, you might be running Python 2 by default.  Check what version of Python you are running:

    $ python --version

If the call above results in Python 2, find the path for Python 3:

    $ which python3  # Python 3 path for mkvirtualenv's --python option

Install Python 3 if needed.  Set the Python version when calling `mkvirtualenv`:

    $ mkvirtualenv --python [Python 3 path from above] gitsome
    $ pip install gitsome

If you want to activate the `gitsome` `virtualenv` again later, run:

    $ workon gitsome

To deactivate the `gitsome` `virtualenv`, run:

    $ deactivate
