# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import unicode_literals
from __future__ import print_function

import re

import six
import shlex


class TextUtils(object):
    """Utilities for parsing and matching text.

    Attributes:
        * None.
    """

    def _fuzzy_finder(self, text, collection, case_sensitive=True):
        """Customized fuzzy finder with optional case-insensitive matching.

        Adapted from: https://github.com/amjith/fuzzyfinder.

        Args:
            text: A string which is typically entered by a user.
            collection: An iterable that represents a collection of strings
                which will be filtered based on the input `text`.
            case_sensitive: A boolean that indicates whether the find
                will be case sensitive.

        Returns:
            A generator object that produces a list of suggestions
            narrowed down from `collections` using the `text` input.
        """
        suggestions = []
        if case_sensitive:
            pat = '.*?'.join(map(re.escape, text))
        else:
            pat = '.*?'.join(map(re.escape, text.lower()))
        regex = re.compile(pat)
        for item in collection:
            if case_sensitive:
                r = regex.search(item)
            else:
                r = regex.search(item.lower())
            if r:
                suggestions.append((len(r.group()), r.start(), item))

        return (z for _, _, z in sorted(suggestions))

    def _shlex_split(self, text):
        """Wrapper for shlex, because it does not seem to handle unicode in 2.6.

        Args:
            * text: A string to split.

        Returns:
            A list that contains words for each split element of text.
        """
        if six.PY2:
            text = text.encode('utf-8')
        return shlex.split(text)

    def _safe_split(self, text):
        """Safely splits the input text.

        Shlex can't always split. For example, "\" crashes the completer.

        Args:
            * text: A string to split.

        Returns:
            A list that contains words for each split element of text.

        """
        try:
            words = self._shlex_split(text)
            return words
        except:
            return text
