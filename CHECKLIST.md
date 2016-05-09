Release Checklist
=================

A. Install in a new venv and run unit tests

Note, you can't seem to script the virtualenv calls, see:
https://bitbucket.org/dhellmann/virtualenvwrapper/issues/219/cant-deactivate-active-virtualenv-from

    $ deactivate
    $ rmvirtualenv gitsome
    $ mkvirtualenv gitsome
    $ pip install -e .
    $ pip install -r requirements-dev.txt
    $ rm -rf .tox && tox

B. Run code checks

    $ scripts/run_code_checks.sh

C. Run manual [smoke tests](#smoke-tests) on Mac, Ubuntu, Windows

D. Update and review `README.rst` and `Sphinx` docs, then check gitsome/docs/build/html/index.html

    $ scripts/update_docs.sh

E. Push changes

F. Review Travis, Codecov, and Gemnasium

G. Start a new release branch

    $ git flow release start x.y.z

H. Increment the version number in `gitsome/__init__.py`

I. Update and review `CHANGELOG`

    $ scripts/create_changelog.sh

J. Commit the changes

K. Finish the release branch

    $ git flow release finish 'x.y.z'

L. Input a tag

    $ vx.y.z

M. Push tagged release to develop and master

    $ git checkout master
    $ git push

    Might need to recreate develop branch.

N. Set CHANGELOG as `README.md`

    $ scripts/set_changelog_as_readme.sh

O. Register package with PyPi

    $ python setup.py register -r pypi

P. Upload to PyPi

    $ python setup.py sdist upload -r pypi

Q. Upload Sphinx docs to PyPi

    $ python setup.py upload_sphinx

R. Restore `README.md`

    $ scripts/set_changelog_as_readme_undo.sh

S. Review newly released package from PyPi

T. Release on GitHub: https://github.com/donnemartin/gitsome/tags

    1. Click "Add release notes" for latest release
    2. Copy release notes from `CHANGELOG.md`
    3. Click "Publish release"

U. Install in a new venv and run manual [smoke tests](#smoke-tests) on Mac, Ubuntu, Windows

## Smoke Tests

Run the following on Python 3.4:

* Craete a new `virtualenv`
* Pip install `gitsome` into new `virtualenv`
* Run `gitsome`
* Run targeted tests based on recent code changes
