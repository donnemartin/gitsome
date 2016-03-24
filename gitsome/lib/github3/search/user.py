# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from ..users import User


class UserSearchResult(GitHubCore):
    def _update_attributes(self, data):
        result = data.copy()
        #: Score of this search result
        self.score = result.pop('score')
        #: Text matches
        self.text_matches = result.pop('text_matches', [])
        #: User object matching the search
        self.user = User(result, self)

    def _repr(self):
        return '<UserSearchResult [{0}]>'.format(self.user)
