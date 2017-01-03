#!/usr/bin/env python
# coding=utf-8

"""The gitsome installer."""
from __future__ import print_function, unicode_literals
import os
import sys
try:
    from setuptools import setup, find_packages
    from setuptools.command.sdist import sdist
    from setuptools.command.install import install
    from setuptools.command.develop import develop
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    from distutils.command.sdist import sdist as sdist
    from distutils.command.install import install as install
    HAVE_SETUPTOOLS = False
from gitsome.__init__ import __version__ as VERSION


TABLES = ['xonsh/lexer_table.py', 'xonsh/parser_table.py']


def clean_tables():
    for f in TABLES:
        if os.path.isfile(f):
            os.remove(f)
            print('Remove ' + f)


def build_tables():
    print('Building lexer and parser tables.')
    sys.path.insert(0, os.path.dirname(__file__))
    from xonsh.parser import Parser
    Parser(lexer_table='lexer_table', yacc_table='parser_table',
           outputdir='xonsh')
    sys.path.pop(0)


class xinstall(install):
    def run(self):
        clean_tables()
        build_tables()
        install.run(self)


class xsdist(sdist):
    def make_release_tree(self, basedir, files):
        clean_tables()
        build_tables()
        sdist.make_release_tree(self, basedir, files)


if HAVE_SETUPTOOLS:
    class xdevelop(develop):
        def run(self):
            clean_tables()
            build_tables()
            develop.run(self)


def main():
    if sys.version_info[0] < 3:
        sys.exit('gitsome currently requires Python 3.4+')
    try:
        if '--name' not in sys.argv:
            print(logo)
    except UnicodeEncodeError:
        pass
    skw = dict(
        name='gitsome',
        description='A Supercharged Git/Shell Autocompleter with GitHub Integration.',  # NOQA
        license='Apache License 2.0',
        version=VERSION,
        author='Donne Martin',
        maintainer='Donne Martin',
        author_email='donne.martin@gmail.com',
        url='https://github.com/donnemartin/gitsome',
        platforms='Cross Platform',
        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        packages=find_packages(),
        scripts=['scripts/xonsh',
                 'scripts/xonsh.bat',
                 'scripts/gitsome',
                 'scripts/gitsome.bat'],
        cmdclass={'install': xinstall, 'sdist': xsdist},
        )
    if HAVE_SETUPTOOLS:
        skw['setup_requires'] = ['ply']
        skw['install_requires'] = [
            'numpydoc>=0.5,<1.0',
            'ply>=3.4,<4.0',
            'prompt-toolkit>=1.0.0,<1.1.0',
            'requests>=2.8.1,<3.0.0',
            'colorama>=0.3.3,<1.0.0',
            'click>=5.1,<7.0',
            'pygments>=2.0.2,<3.0.0',
            'feedparser>=5.2.1,<6.0.0',
            'pytz>=2016.3,<2017.0',
            'docopt>=0.6.2,<1.0.0',
            'uritemplate.py>=1.0.0,<4.0.0',
        ],
        skw['entry_points'] = {
            'pygments.lexers': ['gitsome = xonsh.pyghooks:XonshLexer',
                                'gitsomecon = xonsh.pyghooks:XonshConsoleLexer',
                                ],
            'console_scripts': ['gh = gitsome.main_cli:cli',
                                ],
            }
        skw['cmdclass']['develop'] = xdevelop
    setup(**skw)


logo = ''


if __name__ == '__main__':
    main()
