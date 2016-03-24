# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from .commit import RepoCommit


class Branch(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a
    :class:`Repository <github3.repos.repo.Repository>`.
    """
    def _update_attributes(self, branch):
        #: Name of the branch.
        self.name = branch.get('name')
        #: Returns the branch's
        #: :class:`RepoCommit <github3.repos.commit.RepoCommit>` or ``None``.
        self.commit = branch.get('commit')
        if self.commit:
            self.commit = RepoCommit(self.commit, self)
        #: Returns '_links' attribute.
        self.links = branch.get('_links', {})

    def _repr(self):
        return '<Repository Branch [{0}]>'.format(self.name)
