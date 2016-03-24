"""
github3.gists
=============

Module which contains all the gist related material.

Sub-modules:
    github3.gists.gist
    github3.gists.file
    github3.gists.comment
    github3.gists.history

See also: http://developer.github.com/v3/gists/
"""

from .gist import Gist

__all__ = [Gist]
