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
from prompt_toolkit.completion import Completion

from .completions import META_LOOKUP_GH


class TextUtils(object):
    """Utilities for parsing and matching text.

    Attributes:
        * None.
    """

    def find_matches(self, word, collection, fuzzy):
        """Finds all matches in collection for word.

        Args:
            * word: A string representing the word before
                the cursor.
            * collection: A collection of words to match.
            * fuzzy: A boolean that specifies whether to use fuzzy matching.

        Yields:
            A list of prompt_toolkit's Completions.
        """
        word = self._last_token(word).lower()
        matches = []
        for suggestion in self._find_collection_matches(word,
                                                        collection,
                                                        fuzzy):
            matches.append(suggestion)
        return matches

    def get_tokens(self, text):
        """Parses out all tokens.

        Args:
            * text: A string to split into tokens.

        Returns:
            A list of strings for each word in the text.
        """
        if text is not None:
            text = text.strip()
            words = self._safe_split(text)
            return words
        return []

    def _last_token(self, text):
        """Finds the last word in text.

        Args:
            * text: A string to parse and obtain the last word.

        Returns:
            A string representing the last word in the text.
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = self._safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

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

    def _find_collection_matches(self, word, collection, fuzzy):
        """Yields all matching names in list.

        Args:
            * word: A string representing the word before the cursor.
            * collection: A collection of words to match.
            * fuzzy: A boolean that specifies whether to use fuzzy matching.

        Yields:
            A generator of prompt_toolkit's Completions.
        """
        word = word.lower()
        if fuzzy:
            for suggestion in self._fuzzy_finder(word,
                                                 collection,
                                                 case_sensitive=False):
                yield Completion(suggestion,
                                 -len(word),
                                 display_meta='display_meta')
        else:
            for name in sorted(collection):
                if name.lower().startswith(word) or not word:
                    display = None
                    display_meta = None
                    # print(len(words))
                    if name in META_LOOKUP_GH:
                        display_meta = META_LOOKUP_GH[name]
                    yield Completion(name,
                                     -len(word),
                                     display=display,
                                     display_meta=display_meta)

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
