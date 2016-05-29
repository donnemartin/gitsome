![](http://i.imgur.com/0SXZ90y.gif)

gitsome
=======

[![Build Status](https://travis-ci.org/donnemartin/gitsome.svg?branch=master)](https://travis-ci.org/donnemartin/gitsome) [![Codecov](https://img.shields.io/codecov/c/github/donnemartin/gitsome.svg)](https://codecov.io/github/donnemartin/gitsome)

[![PyPI version](https://badge.fury.io/py/gitsome.svg)](http://badge.fury.io/py/gitsome) [![PyPI](https://img.shields.io/pypi/pyversions/gitsome.svg)](https://pypi.python.org/pypi/gitsome/) [![License](https://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

To view the latest `README`, `docs`, and `code`, visit the GitHub repo:

https://github.com/donnemartin/gitsome

To submit bugs or feature requests, visit the issue tracker:

https://github.com/donnemartin/gitsome/issues

Changelog
=========

0.6.0 (2016-05-29)
------------------

### Features

* [#3](https://github.com/donnemartin/gitsome/issues/3) - Add GitHub Enterprise support.
* [#33](https://github.com/donnemartin/gitsome/issues/33) - Revamp the info shown with the `gh feed` command.

### Bug Fixes

* [#30](https://github.com/donnemartin/gitsome/issues/30) - Fix a typo in the `pip3` install instructions.
* [#39](https://github.com/donnemartin/gitsome/issues/39) - Fix `gh feed` `-pr/--private` flag in docs.
* [#40](https://github.com/donnemartin/gitsome/issues/40) - Fix `create-issue` `NoneType` error if no `-b/--body` is specified.
* [#46](https://github.com/donnemartin/gitsome/issues/46) - Fix `gh view` with the -b/--browser option only working for repos, not for issues or PRs.
* [#48](https://github.com/donnemartin/gitsome/issues/48) - Fix `create-repo` `NoneType` error if no `-d/--description` is specified.
* [#54](https://github.com/donnemartin/gitsome/pull/54) - Update to `prompt-toolkit` 1.0.0, which includes performance improvements (especially noticeable on Windows) and bug fixes.
* Fix `Config` docstrings.

### Updates

* [#26](https://github.com/donnemartin/gitsome/issues/26), [#32](https://github.com/donnemartin/gitsome/issues/32) - Add copyright notices for third
party libraries.
* [#44](https://github.com/donnemartin/gitsome/pull/44), [#53](https://github.com/donnemartin/gitsome/pull/53) - Update packaging dependencies based on semantic versioning.
* Tweak `README` intro.

0.5.0 (2016-05-15)
------------------

### Features

* [#12](https://github.com/donnemartin/gitsome/issues/12) - Allow 2FA-enabled users to log in with a password + 2FA code.  Previously 2FA-enabled users could only log in with a [personal access token](https://github.com/settings/tokens).  Also includes an update of login prompts to improve clarity.

### Bug Fixes

* [#16](https://github.com/donnemartin/gitsome/pull/16), [#28](https://github.com/donnemartin/gitsome/pull/28) - Fix typos in README.
* [#18](https://github.com/donnemartin/gitsome/pull/18) - Fix dev install instructions in README.
* [#24](https://github.com/donnemartin/gitsome/pull/24) - Fix style guide broken link in CONTRIBUTING.

### Updates

* [#1](https://github.com/donnemartin/gitsome/issues/1) - Add Codecov coverage testing status to README.
* [#2](https://github.com/donnemartin/gitsome/issues/2) - Add note about enabling Zsh completions to README.
* [#4](https://github.com/donnemartin/gitsome/issues/4) - Add note about using `pip3` to README.
* [#5](https://github.com/donnemartin/gitsome/issues/5) - Decrease speed of README gif.
* [#6](https://github.com/donnemartin/gitsome/pull/6) - Update url for `click`.
* [#20](https://github.com/donnemartin/gitsome/issues/20) - Add note about enabling more completions to README.
* [#21](https://github.com/donnemartin/gitsome/issues/21) - Bump up `prompt-toolkit` version from `0.51` to `0.52`.
* [#26](https://github.com/donnemartin/gitsome/issues/26) - Add `xonsh` copyright notice to LICENSE.
* [#32](https://github.com/donnemartin/gitsome/pull/32) - Add `github3.py`, `html2text`, and `img2txt` copyright notices to LICENSE.
* Update installation instructions in README.
* Update color customization discussion in README.

0.4.0 (2016-05-09)
------------------

* Initial release.
