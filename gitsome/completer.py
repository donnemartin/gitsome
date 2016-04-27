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

from prompt_toolkit.completion import Completer, Completion

from .completions import COMPLETIONS_GH, SUBCOMMANDS
from .completions_git import META_LOOKUP_GIT, META_LOOKUP_GIT_EXTRAS
from .utils import TextUtils


class CompleterGitsome(Completer):
    """Gitsome prompt toolkit completer.

    :type text_utils: :class:`utils.TextUtils`
    :param text_utils: An instance of `utils.TextUtils`.

    :type fuzzy_match: bool
    :param fuzzy_match: Determines whether to use fuzzy matching.
        Currently, this is always set to False but can be enabled.
    """

    def __init__(self):
        self.fuzzy_match = False
        self.text_utils = TextUtils()

    def build_completions_with_meta(self, line, prefix, completions):
        """Build prompt_toolkit Completions with meta info.

        :type line: list
        :param line: The input text as a list of words.

        :type prefix: string
        :param prefix: The current word.

        :type completions: list
        :param completions: Completions to build meta info for.

        :rtype: list
        :return: Completions with meta info.
        """
        completions_with_meta = []
        tokens = line.split(' ')
        if tokens[0] != 'gh':
            for comp in completions:
                display = None
                display_meta = None
                if 'git' in line and comp.strip() in META_LOOKUP_GIT:
                    display_meta = META_LOOKUP_GIT[comp.strip()]
                elif 'git' in line and comp.strip() in META_LOOKUP_GIT_EXTRAS:
                    display_meta = META_LOOKUP_GIT_EXTRAS[comp.strip()]
                completions_with_meta.append(
                    Completion(comp,
                               -len(prefix),
                               display=display,
                               display_meta=display_meta))
        return completions_with_meta

    def completing_command(self, words, word_before_cursor):
        """Determine if we are currently completing the gh command.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing the gh command.
        """
        if len(words) == 1 and word_before_cursor != '':
            return True
        else:
            return False

    def completing_subcommand(self, words, word_before_cursor):
        """Determine if we are currently completing a subcommand.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing a subcommand.
        """
        if (len(words) == 1 and word_before_cursor == '') \
                or (len(words) == 2 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_arg(self, words, word_before_cursor):
        """Determine if we are currently completing an arg.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing an arg.
        """
        if (len(words) == 2 and word_before_cursor == '') \
                or (len(words) == 3 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_subcommand_option(self, words, word_before_cursor):
        """Determine if we are currently completing an option.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: list
        :return: A list of options.
        """
        options = []
        for subcommand, args_opts in COMPLETIONS_GH.items():
            if subcommand in words and \
                (words[-2] == subcommand or
                    self.completing_subcommand_option_util(subcommand, words)):
                options.extend(COMPLETIONS_GH[subcommand]['opts'])
        return options

    def completing_subcommand_option_util(self, option, words):
        """Determine if we are currently completing an option.

        Called by completing_subcommand_option as a utility method.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: bool
        :return: Specifies whether we are currently completing an option.
        """
        # Example: Return True for: gh view 1 --pag
        if len(words) > 3:
            if option in words:
                return True
        return False

    def arg_completions(self, words, word_before_cursor):
        """Generates arguments completions based on the input.

        :type words: list
        :param words: The input text broken into word tokens.

        :type word_before_cursor: str
        :param word_before_cursor: The current word before the cursor,
            which might be one or more blank spaces.

        :rtype: list
        :return: A list of completions.
        """
        if 'gh' not in words:
            return []
        for subcommand, args_opts in COMPLETIONS_GH.items():
            if subcommand in words:
                args = list(COMPLETIONS_GH[subcommand]['args'].keys())
                if not args:
                    # Some commands don't have args, complete options instead.
                    args = list(COMPLETIONS_GH[subcommand]['opts'].keys())
                return args if args else []
        return []

    def get_completions(self, document, _):
        """Get completions for the current scope.

        :type document: :class:`prompt_toolkit.Document`
        :param document: An instance of `prompt_toolkit.Document`.

        :type _: :class:`prompt_toolkit.completion.Completion`
        :param _: (Unused).

        :rtype: generator
        :return: Yields an instance of `prompt_toolkit.completion.Completion`.
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if self.completing_command(words, word_before_cursor):
            commands = ['gh']
        else:
            if 'gh' not in words:
                return commands
            if self.completing_subcommand(words, word_before_cursor):
                commands = list(SUBCOMMANDS.keys())
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.arg_completions(words, word_before_cursor)
                else:
                    commands = self.completing_subcommand_option(
                        words,
                        word_before_cursor)
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match)
        return completions
