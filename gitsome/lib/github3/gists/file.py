# -*- coding: utf-8 -*-
"""
github3.gists.file
------------------

Module containing the logic for the GistFile object.
"""
from __future__ import unicode_literals

from ..models import GitHubCore


class GistFile(GitHubCore):

    """This represents the file object returned by interacting with gists.

    It stores the raw url of the file, the file name, language, size and
    content.

    """

    def _update_attributes(self, attributes):
        #: The raw URL for the file at GitHub.
        self.raw_url = attributes.get('raw_url')
        #: The name of the file.
        self.filename = attributes.get('filename')
        #: The name of the file.
        self.name = attributes.get('filename')
        #: The language associated with the file.
        self.language = attributes.get('language')
        #: The size of the file.
        self.size = attributes.get('size')
        #: The content of the file.
        self.original_content = attributes.get('content')

    def _repr(self):
        return '<Gist File [{0}]>'.format(self.name)

    def content(self):
        """Retrieve contents of file from key 'raw_url' if there is no
        'content' key in Gist object.
        """
        resp = self._get(self.raw_url)
        if self._boolean(resp, 200, 404):
            return resp.content
        return None
