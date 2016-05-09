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

import platform
import re
import sys

import click

from .view_entry import ViewEntry


class Table(object):
    """Display table information for repos, issues, prs, etc.

    :type config: :class:`config.Config`
    :param config: An instance of `config.Config`.
    """

    def __init__(self, config):
        self.config = config

    def build_table(self, view_entries, limit, pager, format_method,
                    build_urls=True, print_output=True):
        """Build the table used for the gh view command.

        :type view_entries: list
        :param view_entries: A list of `github3` items.

        :type limit: int
        :param limit: Determines the number of items to show.

        :type format_method: callable
        :param format_method: A method called to format each item in the table.

        :type build_urls: bool
        :param build_urls: Determines whether to build urls for the
                gh view # command.

        :type print_output: bool
        :param print_output: determines whether to print the output
                (True) or return the output as a string (False).

        :rtype: str
        :return: the output if print_output is True, else, return None.
        """
        if build_urls:
            self.build_table_urls(view_entries)
        index = 0
        output = ''
        for view_entry in view_entries:
            index += 1
            view_entry.index = index
            output += format_method(view_entry) + '\n'
            if index >= limit:
                break
        if build_urls:
            if len(view_entries) > limit:
                output += click.style(('       <Hiding ' +
                                       str(len(view_entries) - limit) +
                                       ' item(s) with the -l/--limit flag>\n'),
                                      fg=self.config.clr_message)
        if index == 0:
            output += click.style('No results found',
                                  fg=self.config.clr_message)
        elif build_urls:
            output += click.style(self.create_tip(index))
        else:
            output += click.style('')
        if print_output:
            if pager:
                color = None
                if platform.system() == 'Windows':
                    color = True
                    # Strip out Unicode, which seems to have issues on
                    # Windows with click.echo_via_pager.
                    output = re.sub(r'[^\x00-\x7F]+', '', output)
                click.echo_via_pager(output, color)
            else:
                click.secho(output)
            return None
        else:
            return output

    def build_table_setup(self, items, format_method,
                          limit, pager, build_urls=True):
        """Convert items to a list of ViewEntry before calling `build_table`.

        :type items: list
        :param items: A list of `github3` items.

        :type format_method: callable
        :param format_method: A method called to format each item in the table.

        :type limit: int
        :param limit: Determines the number of items to show.

        :type pager: bool
        :param pager: Determines whether to show results in a pager,
            if available.

        :type build_urls: bool
        :param build_urls: determines whether to build urls for the
                `gh view` [#] command.
        """
        view_entries = []
        for item in items:
            view_entries.append(ViewEntry(item))
        self.build_table(view_entries,
                         limit,
                         pager,
                         format_method,
                         build_urls)

    def build_table_setup_feed(self, items, format_method, pager):
        """Perform feed-specific processing before calling `build_table`.

        :type items: list
        :param items: A list of `github3` items.

        :type format_method: callable
        :param format_method: A method called to format each item in the table.

        :type pager: bool
        :param pager: Determines whether to show results in a pager,
            if available.
        """
        self.build_table_setup(items.entries,
                               format_method,
                               limit=sys.maxsize,
                               pager=pager,
                               build_urls=False)

    def build_table_setup_user(self, items, format_method,
                               limit, pager, build_urls=True):
        """Convert items to a list of ViewEntry before calling `build_table`.

        Specific to GitHub3.User.users.

        :type items: list
        :param items: A list of `github3` items.

        :type format_method: callable
        :param format_method: A method called to format each item in the table.

        :type limit: int
        :param limit: Determines the number of items to show.

        :type pager: bool
        :param pager: Determines whether to show results in a pager,
            if available.

        :type build_urls: bool
        :param build_urls: determines whether to build urls for the
                `gh view` [#] command.
        """
        view_entries = []
        for item in items:
            view_entries.append(ViewEntry(item=item, url=item.login))
        self.build_table(view_entries,
                         limit=sys.maxsize,
                         pager=pager,
                         format_method=format_method)

    def build_table_setup_trending(self, items, format_method,
                                   limit, pager, build_urls=True):
        """Convert items to a list of ViewEntry before calling `build_table`.

        Specific to feedparser entries.

        :type items: list
        :param items: A list of `github3` items.

        :type format_method: callable
        :param format_method: A method called to format each item in the table.

        :type limit: int
        :param limit: Determines the number of items to show.

        :type pager: bool
        :param pager: Determines whether to show results in a pager,
            if available.

        :type build_urls: bool
        :param build_urls: determines whether to build urls for the
                `gh view` [#] command.
        """
        view_entries = []
        for item in items:
            url = 'https://github.com/' + '/'.join(item['link'].split('/')[-2:])
            view_entries.append(ViewEntry(item=item, url=url))
        self.build_table(view_entries,
                         limit=sys.maxsize,
                         pager=pager,
                         format_method=format_method)

    def build_table_urls(self, view_entries):
        """Build the GitHub urls for the specified view_entries.

        :type view_entries: list
        :param view_entries: A list of ViewEntry items.
        """
        for view_entry in view_entries:
            self.config.urls.append(view_entry.url)
        self.config.save_urls()

    def create_tip(self, max_index):
        """Create the tip about the view command after showing a table.

        :type max_index: int
        :param max_index: The index upper bound.

        :rtype: str
        :return: The formatted tip.
        """
        tip = click.style('  View the page for ',
                          fg=self.config.clr_message)
        tip += click.style('1 through ', fg=self.config.clr_view_index)
        tip += click.style(str(max_index), fg=self.config.clr_view_index)
        tip += click.style(' with the following command:\n',
                           fg=self.config.clr_message)
        tip += click.style('    gh view [#] ', fg=self.config.clr_view_index)
        tip += click.style('optional: [-b/--browser] [--help]\n',
                           fg=self.config.clr_message)
        return tip
