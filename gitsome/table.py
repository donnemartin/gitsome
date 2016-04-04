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

import sys

import click

from .view_entry import ViewEntry


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

    def build_table(self, view_entries, limit, pager, format_method,
                    build_urls=True, print_output=True):
        """Builds the table used for the gh view command.

        Args:
            * view_entries: A list of github3 items.
            * limit: An int that specifies the number of items to show.
            * format_method: A method called to format each item in the table.
            * build_urls: A bool that determines whether to build urls for the
                gh view # command.
            * print_output: A bool that determines whether to print the output
                (True) or return the output as a string (False)

        Returns:
            A string representing the output if print_output is True
            else, returns None.
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
                                       ' item(s), use -l/--limit ' +
                                       str(len(view_entries)) +
                                       ' to view all items.>'),
                                      fg=None)
        if index == 0:
            output += click.style('No results found', fg=None)
        elif build_urls:
            output += click.style(self.create_tip(index))
        else:
            output += click.style('')
        if print_output:
            if pager:
                click.echo_via_pager(output)
            else:
                click.secho(output)
            return None
        else:
            return output

    def build_table_setup(self, items, format_method,
                          limit, pager, build_urls=True):
        """Converts items to a list of ViewEntry before calling `build_table`.

        Args:
            * items: A list of github3 items.
            * format_method: A method called to format each item in the table.
            * limit: An int that specifies the number of items to show.
            * build_urls: A bool that determines whether to build urls for the
                gh view # command.

        Returns:
            None.
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
        """Performs feed-specific processing before calling `build_table`.

        Args:
            * items: A list of github3 items.
            * format_method: A method called to format each item in the table.

        Returns:
            None.
        """
        self.build_table_setup(items.entries,
                               format_method,
                               limit=sys.maxsize,
                               pager=pager,
                               build_urls=False)

    def build_table_setup_user(self, items, format_method,
                               limit, pager, build_urls=True):
        """Converts items to a list of ViewEntry before calling `build_table`.

        Specific to GitHub3.User.users.

        Args:
            * items: A list of github3 items.
            * format_method: A method called to format each item in the table.
            * limit: An int that specifies the number of items to show.
            * build_urls: A bool that determines whether to build urls for the
                gh view # command.

        Returns:
            None.
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
        """Converts items to a list of ViewEntry before calling `build_table`.

        Specific to feedparser entries.

        Args:
            * items: A list of feedparser entries.
            * format_method: A method called to format each item in the table.
            * limit: An int that specifies the number of items to show.
            * build_urls: A bool that determines whether to build urls for the
                gh view # command.

        Returns:
            None.
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
        """Builds the GitHub urls for the specified view_entries.

        Args:
            * table: A list of view_entry.

        Returns:
            None.
        """
        for view_entry in view_entries:
            self.config.urls.append(view_entry.url)
        self.config.save_urls()

    def create_tip(self, max_index):
        """Creates the tip about the view command.

        Args:
            * max_index: A string that represents the index upper bound.

        Returns:
            A string representation of the formatted tip.
        """
        tip = click.style('  View the repo or issue for ', fg=None)
        tip += click.style('1 through ', fg='magenta')
        tip += click.style(str(max_index), fg='magenta')
        tip += click.style(' with the following command:\n', fg=None)
        tip += click.style('    gh view [#] ', fg='magenta')
        tip += click.style('optional: [-b/--browser] [--help]\n', fg=None)
        return tip
