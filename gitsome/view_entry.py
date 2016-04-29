# coding: utf-8

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


class ViewEntry(object):
    """A table entry used with the `gh view` command.

    :type index: int
    :param index: The row index.

    :type item: :class:`github3` repo, issue, thread, etc.
    :param item: An instance of a `github3` repo, issue, thread, etc.

    :param sort_key_primary: A class member representing the primary
        sort key.

    :param sort_key_secondary: A class member representing the secondary
        sort key.

    :param sort_key_tertiary: A class member representing the tertiary
        sort key.

    :type url: str
    :param url: The item's url.
    """

    def __init__(self, item, url=None, index=-1,
                 sort_key_primary=None,
                 sort_key_secondary=None,
                 sort_key_tertiary=None):
        self.item = item
        self.url = url
        self.index = index
        self.sort_key_primary = sort_key_primary
        self.sort_key_secondary = sort_key_secondary
        self.sort_key_tertiary = sort_key_tertiary

    def __lt__(self, other):
        """Implement 'less than' used for sorting.

        :type other: :class:`ViewEntry`
        :param other: An instance of `ViewEntry` used for comparison.

        :rtype: bool
        :return: Determines whether the current ViewEntry is less than the
                `other` view entry.
        """
        if self.sort_key_primary != other.sort_key_primary or \
                not self.sort_key_secondary:
            return self.sort_key_primary < other.sort_key_primary
        else:
            if self.sort_key_secondary != other.sort_key_secondary or \
                    not self.sort_key_tertiary:
                return self.sort_key_secondary < other.sort_key_secondary
            else:
                return self.sort_key_tertiary < other.sort_key_tertiary
