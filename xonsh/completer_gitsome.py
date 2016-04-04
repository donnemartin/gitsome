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

from prompt_toolkit.completion import Completer

from .completions import SUBCOMMANDS, COMPLETIONS_GH
from .utils import TextUtils


class CompleterGitsome(Completer):
    """Completer haxor-news.

    Attributes:
        * text_utils: An instance of TextUtils.
        * fuzzy_match: A boolean that determines whether to use fuzzy matching.
        * subcommand_to_options_map: A dict mapping the subcommand to
                its args.
    """

    def __init__(self):
        """Initializes Completer.

        Args:
            * None

        Returns:
            None.
        """
        self.fuzzy_match = False
        self.text_utils = TextUtils()
