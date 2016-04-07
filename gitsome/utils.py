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

import six
import shlex


class TextUtils(object):
    """Utilities for parsing and matching text.

    Attributes:
        * None.
    """

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
