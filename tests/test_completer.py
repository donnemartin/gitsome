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
from __future__ import division

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
