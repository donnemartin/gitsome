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

class ViewEntry(object):
    """Encapsulates a table entry used with the `gh view` command.

    Attributes:
        * item: An instance of a github3 repo, issue, thread, etc.
        * url: A string representing the item's url.
        * index: An int representing the row index.
        * sort_key_primary: A member representing the primary sort key.
        * sort_key_secondary: A member representing the secondary sort key.
        * sort_key_tertiary: A member representing the tertiary sort key.
    """

    def __init__(self, item, url, index=-1,
                 sort_key_primary=None,
                 sort_key_secondary=None,
                 sort_key_tertiary=None):
        """Inits ViewEntry.

        Args:
            * None.

        Returns:
            None.
        """
        self.item = item
        self.url = url
        self.index = index
        self.sort_key_primary = sort_key_primary
        self.sort_key_secondary = sort_key_secondary
        self.sort_key_tertiary = sort_key_tertiary

    def __lt__(self, other):
        """Implements 'less than' used for sorting.

        Args:
            * other: An instance of ViewEntry used for comparison.

        Returns:
            A bool indicating whether the current ViewEntry is less than the
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
