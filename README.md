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

### Optional: Installing `PIL` or `Pillow`

Displaying the avatar for the `gh me` and `gh user` commands will require installing the optional `PIL` or `Pillow` dependency.

Windows* and Mac:

    $ pip install Pillow

*See the [Windows Support](#windows-support) section for limitations on the avatar.

Ubuntu users, check out these [instructions on askubuntu](http://askubuntu.com/a/272095)

### Supported Python Versions

* Python 3.4
* Python 3.5

`gitsome` is powered by `xonsh` which does not currently support Python 2.x, as discussed in this [ticket](https://github.com/scopatz/xonsh/issues/66).

### Supported Platforms

* Mac OS X
    * Tested on OS X 10.10
* Linux, Unix
    * Tested on Ubuntu 14.04 LTS
* Windows
    * Tested on Windows 10

### Windows Support

`gitsome` has been tested on Windows 10.

![Imgur](http://i.imgur.com/DxomJNE.png)

#### Pager Support

Pager support on Windows is more limited.

On Windows, the following commands do not send results to a pager:

    $ gh view
    $ gh issue
    $ gh pull-request

You can instead output to a pager with the `| more` command, although color is stripped:

    $ gh view 1 -c | more

#### Config File

On Windows, the `.gitsomeconfig ` file can be found in `%userprofile%`.  For example:

    C:\Users\dmartin\.gitsomeconfig

#### Text Only Avatar

The commands `gh user` and `gh me` will always have the `-t/--text_avatar` flag enabled, since `img2txt` does not support the ansi avatar on Windows.

#### `cmder` and `conemu`

Although you can use the standard Windows command prompt, you'll probably have a better experience with either [cmder](https://github.com/cmderdev/cmder) or [conemu](https://github.com/Maximus5/ConEmu).

## Developer Installation

If you're interested in contributing to `gitsome`, run the following commands:

    $ git clone https://github.com/donnemartin/gitsome.git
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ gitsome
    $ gh <command> [param] [options]
