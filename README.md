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

### Enabling Bash Completions

By default, `gitsome` looks at the following [locations to enable bash completions](https://github.com/donnemartin/gitsome/blob/master/xonsh/environ.py#L123-L131).

To add additional bash completions, update the `~/.xonshrc` file with the location of your bash completions.

If `~/.xonshrc` does not exist, create it:

    $ touch ~/.xonshrc

For example, if additional completions are found in `usr/local/etc/my_bash_completion.d/completion.bash`, add the following line in `~/.xonshrc`:

```
$BASH_COMPLETIONS.append('/usr/local/etc/my_bash_completion.d/completion.bash')
```

You will need to restart `gitsome` for the changes to take effect.

### Enabling `gh` Tab Completions Outside of `gitsome`

You can run `gh` commands outside of the `gitsome` shell completer.  To enable `gh` tab completions for this workflow, copy the [`gh_complete.sh`](https://github.com/donnemartin/gitsome/blob/master/scripts/gh_complete.sh) file locally.

Let bash know completion is available for the `gh` command within your current session:

    $ source /path/to/gh_complete.sh

To enable tab completion for all terminal sessions, add the following to your `bashrc` file:

    source /path/to/gh_complete.sh

Reload your `bashrc`:

    $ source ~/.bashrc

Tip: `.` is the short form of `source`, so you can run this instead:

    $ . ~/.bashrc
