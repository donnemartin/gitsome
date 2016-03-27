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

import click


class Table(object):
    """Displays table information for repos, issues, prs, etc.

    Attributes:
        * None
    """

    def __init__(self, config):
        """Inits GitHub.

        Args:
            * config: An instance of Config.

        Returns:
            None.
        """
        self.config = config