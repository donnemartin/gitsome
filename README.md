## Installation

### Pip Installation

[![PyPI version](https://badge.fury.io/py/gitsome.svg)](http://badge.fury.io/py/gitsome) [![PyPI](https://img.shields.io/pypi/pyversions/gitsome.svg)](https://pypi.python.org/pypi/gitsome/)

`gitsome` is hosted on [PyPI](https://pypi.python.org/pypi/gitsome).  The following command will install `gitsome`:

    $ pip install gitsome

You can also install the latest `gitsome` from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/donnemartin/gitsome.git

If you are not installing in a virtualenv, run with `sudo`:

    $ sudo pip install gitsome

Once installed, run the optional `gitsome` autocompleter with interactive help:

    $ gitsome

Run GitHub-integrated commands:

    $ gh <command> [param] [options]

Note: Running the `gitsome` shell is not required to execute `gh` commands.  After [installing](#installation) `gitsome` you can run `gh` commands from your shell.

Running the `gitsome` shell will provide you with autocompletion, interactive help, fish-style suggestions, a Python REPL, etc.

### Virtual Environment Installation

It is recommended that you install Python packages in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid potential issues with dependencies or permissions.

To view `gitsome` `virtualenv` installation instructions, click [here](https://github.com/donnemartin/gitsome/blob/master/INSTALLATION.md).

### Running the `gh configure` Command

To properly integrate with GitHub, `gitsome` must be properly configured:

    $ gh configure

View more details in the [gh configure](https://github.com/donnemartin/haxor-news/blob/master/COMMANDS.md#gh-configure) section.
