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

import mock
from tests.compat import unittest

from prompt_toolkit.document import Document

from gitsome.completer import CompleterGitsome


class CompleterTest(unittest.TestCase):

    def setUp(self):
        self.completer = CompleterGitsome()
        self.completer_event = self.create_completer_event()

    def create_completer_event(self):
        return mock.Mock()

    def _get_completions(self, command):
        position = len(command)
        result = set(self.completer.get_completions(
            Document(text=command, cursor_position=position),
            self.completer_event))
        return result

    def verify_completions(self, commands, expected):
        result = set()
        for command in commands:
            # Call the AWS CLI autocompleter
            result.update(self._get_completions(command))
        result_texts = []
        for item in result:
            # Each result item is a Completion object,
            # we are only interested in the text portion
            result_texts.append(item.text)
        assert result_texts
        if len(expected) == 1:
            assert expected[0] in result_texts
        else:
            for item in expected:
                assert item in result_texts

    def test_blank(self):
        text = ''
        expected = set([])
        result = self._get_completions(text)
        assert result == expected

    def test_no_completions(self):
        text = 'foo'
        expected = set([])
        result = self._get_completions(text)
        assert result == expected

    def test_command(self):
        text = ['g']
        expected = ['gh']
        self.verify_completions(text, expected)

    def test_subcommand(self):
        self.verify_completions(['gh c'], ['configure', 'create-comment',
                                           'create-issue', 'create-repo'])
        self.verify_completions(['gh e'], ['emails', 'emojis'])
        self.verify_completions(['gh f'], ['feed', 'followers', 'following'])
        self.verify_completions(['gh g'], ['gitignore-template',
                                           'gitignore-templates'])
        self.verify_completions(['gh i'], ['issue', 'issues'])
        self.verify_completions(['gh l'], ['license', 'licenses'])
        self.verify_completions(['gh m'], ['me'])
        self.verify_completions(['gh n'], ['notifications'])
        self.verify_completions(['gh o'], ['octo'])
        self.verify_completions(['gh p'], ['pull-request', 'pull-requests'])
        self.verify_completions(['gh r'], ['rate-limit', 'repo', 'repos'])
        self.verify_completions(['gh s'], ['search-issues', 'search-repos',
                                           'starred'])
        self.verify_completions(['gh t'], ['trending'])
        self.verify_completions(['gh u'], ['user'])
        self.verify_completions(['gh v'], ['view'])

    def test_args(self):
        self.verify_completions(['gh octo '], ['"Keep it logically awesome"'])

    def test_no_args_with_options(self):
        self.verify_completions(['gh octo '], ['"Keep it logically awesome"'])

    def test_options(self):
        self.verify_completions(['gh emojis '],
                                ['-p', '--pager'])

    def test_multiple_options(self):
        self.verify_completions(['gh feed -pr --pa'], ['--pager'])
        self.verify_completions(['gh feed foo -pr --pa'], ['--pager'])

    def test_fuzzy(self):
        self.completer.fuzzy_match = True
        self.verify_completions(['gh ot'], ['octo'])

    def test_build_completions_with_meta(self):
        result = self.completer.build_completions_with_meta('git ad',
                                                            'ad',
                                                            ['add'])
        assert result[0].display_meta == 'Add file contents to the index.'
        result = self.completer.build_completions_with_meta('git-alia',
                                                            'git-alia',
                                                            ['git-alias'])
        assert result[0].display_meta == 'Define, search and show aliases.'
