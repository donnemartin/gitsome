# -*- coding: utf-8 -*-
"""
github3.repos.tag
=================

This module contains the RepoTag object for GitHub's tag API.

"""
from __future__ import unicode_literals

from ..models import GitHubCore


class RepoTag(GitHubCore):
    """The :class:`RepoTag <RepoTag>` object. This stores the information
    representing a tag that was created on a repository.

    See also: http://developer.github.com/v3/repos/#list-tags
    """
    def _update_attributes(self, tag):
        #: Name of the tag.
        self.name = tag.get('name')
        #: URL for the GitHub generated zipball associated with the tag.
        self.zipball_url = tag.get('zipball_url')
        #: URL for the GitHub generated tarball associated with the tag.
        self.tarball_url = tag.get('tarball_url')
        #: Dictionary containing the SHA and URL of the commit.
        self.commit = tag.get('commit', {})

    def _repr(self):
        return '<Repository Tag [{0}]>'.format(self)

    def __str__(self):
        return self.name
