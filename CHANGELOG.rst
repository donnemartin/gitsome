.. figure:: http://i.imgur.com/0SXZ90y.gif
   :alt:

gitsome
=======

|Build Status| |Codecov|

|PyPI version| |PyPI| |License|

To view the latest ``README``, ``docs``, and ``code``, visit the GitHub
repo:

https://github.com/donnemartin/gitsome

To submit bugs or feature requests, visit the issue tracker:

https://github.com/donnemartin/gitsome/issues

Changelog
=========

0.6.0 (2016-05-29)
------------------

Features
~~~~~~~~

-  `#3 <https://github.com/donnemartin/gitsome/issues/3>`__ - Add GitHub
   Enterprise support.
-  `#33 <https://github.com/donnemartin/gitsome/issues/33>`__ - Revamp
   the info shown with the ``gh feed`` command.

Bug Fixes
~~~~~~~~~

-  `#30 <https://github.com/donnemartin/gitsome/issues/30>`__ - Fix a
   typo in the ``pip3`` install instructions.
-  `#39 <https://github.com/donnemartin/gitsome/issues/39>`__ - Fix
   ``gh feed`` ``-pr/--private`` flag in docs.
-  `#40 <https://github.com/donnemartin/gitsome/issues/40>`__ - Fix
   ``create-issue`` ``NoneType`` error if no ``-b/--body`` is specified.
-  `#46 <https://github.com/donnemartin/gitsome/issues/46>`__ - Fix
   ``gh view`` with the -b/--browser option only working for repos, not
   for issues or PRs.
-  `#48 <https://github.com/donnemartin/gitsome/issues/48>`__ - Fix
   ``create-repo`` ``NoneType`` error if no ``-d/--description`` is
   specified.
-  `#54 <https://github.com/donnemartin/gitsome/pull/54>`__ - Update to
   ``prompt-toolkit`` 1.0.0, which includes performance improvements
   (especially noticeable on Windows) and bug fixes.
-  Fix ``Config`` docstrings.

Updates
~~~~~~~

-  `#26 <https://github.com/donnemartin/gitsome/issues/26>`__,
   `#32 <https://github.com/donnemartin/gitsome/issues/32>`__ - Add
   copyright notices for third party libraries.
-  `#44 <https://github.com/donnemartin/gitsome/pull/44>`__,
   `#53 <https://github.com/donnemartin/gitsome/pull/53>`__ - Update
   packaging dependencies based on semantic versioning.
-  Tweak ``README`` intro.

0.5.0 (2016-05-15)
------------------

Features
~~~~~~~~

-  `#12 <https://github.com/donnemartin/gitsome/issues/12>`__ - Allow
   2FA-enabled users to log in with a password + 2FA code. Previously
   2FA-enabled users could only log in with a `personal access
   token <https://github.com/settings/tokens>`__. Also includes an
   update of login prompts to improve clarity.

Bug Fixes
~~~~~~~~~

-  `#16 <https://github.com/donnemartin/gitsome/pull/16>`__,
   `#28 <https://github.com/donnemartin/gitsome/pull/28>`__ - Fix typos
   in README.
-  `#18 <https://github.com/donnemartin/gitsome/pull/18>`__ - Fix dev
   install instructions in README.
-  `#24 <https://github.com/donnemartin/gitsome/pull/24>`__ - Fix style
   guide broken link in CONTRIBUTING.

Updates
~~~~~~~

-  `#1 <https://github.com/donnemartin/gitsome/issues/1>`__ - Add
   Codecov coverage testing status to README.
-  `#2 <https://github.com/donnemartin/gitsome/issues/2>`__ - Add note
   about enabling Zsh completions to README.
-  `#4 <https://github.com/donnemartin/gitsome/issues/4>`__ - Add note
   about using ``pip3`` to README.
-  `#5 <https://github.com/donnemartin/gitsome/issues/5>`__ - Decrease
   speed of README gif.
-  `#6 <https://github.com/donnemartin/gitsome/pull/6>`__ - Update url
   for ``click``.
-  `#20 <https://github.com/donnemartin/gitsome/issues/20>`__ - Add note
   about enabling more completions to README.
-  `#21 <https://github.com/donnemartin/gitsome/issues/21>`__ - Bump up
   ``prompt-toolkit`` version from ``0.51`` to ``0.52``.
-  `#26 <https://github.com/donnemartin/gitsome/issues/26>`__ - Add
   ``xonsh`` copyright notice to LICENSE.
-  `#32 <https://github.com/donnemartin/gitsome/pull/32>`__ - Add
   ``github3.py``, ``html2text``, and ``img2txt`` copyright notices to
   LICENSE.
-  Update installation instructions in README.
-  Update color customization discussion in README.

0.4.0 (2016-05-09)
------------------

-  Initial release.

.. |Build Status| image:: https://travis-ci.org/donnemartin/gitsome.svg?branch=master
   :target: https://travis-ci.org/donnemartin/gitsome
.. |Codecov| image:: https://img.shields.io/codecov/c/github/donnemartin/gitsome.svg
   :target: https://codecov.io/github/donnemartin/gitsome
.. |PyPI version| image:: https://badge.fury.io/py/gitsome.svg
   :target: http://badge.fury.io/py/gitsome
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/gitsome.svg
   :target: https://pypi.python.org/pypi/gitsome/
.. |License| image:: https://img.shields.io/:license-apache-blue.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
