# -*- coding: utf-8 -*-
"""
github3.licenses
================

This module contains the classes relating to licenses

See also: https://developer.github.com/v3/licenses/
"""
from __future__ import unicode_literals

from .models import GitHubCore


class License(GitHubCore):

    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.drax-preview+json'
    }

    def _update_attributes(self, license):
        self.name = license.get('name')
        self.permitted = license.get('permitted')
        self.category = license.get('category')
        self.forbidden = license.get('forbidden')
        self.featured = license.get('featured')
        self.html_url = license.get('html_url')
        self.body = license.get('body')
        self.key = license.get('key')
        self.description = license.get('description')
        self.implementation = license.get('implementation')
        self.required = license.get('required')

    def _repr(self):
        return '<License [{0}]>'.format(self.name)
