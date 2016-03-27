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

    def build_table(self, view_entries, limit, format_method):
        """Builds the table and headers with tabulate.

        Args:
            * view_entries: xxx.
            * limit: An int that specifies the number of items to show.
            * format_method: A method called to format each item in the table.

        Returns:
            None.
        """
        self.build_table_urls(view_entries)
        index = 0
        for view_entry in view_entries:
            index += 1
            view_entry.index = index
            click.echo(format_method(view_entry))
            if index >= limit:
                break
        if len(view_entries) > limit:
            click.secho(('  Hiding ' +
                         str(len(view_entries) - limit) +
                         ' item(s), use -l/--limit ' +
                         str(len(view_entries)) +
                         ' to view all items.'),
                        fg='magenta')
        if index == 0:
            click.secho('No results found', fg=None)
        else:
            click.secho(self.create_tip(index))

    def build_table_urls(self, view_entries):
        """Builds the GitHub urls for the specified view_entries.

        Args:
            * table: A list of view_entry.

        Returns:
            None.
        """
        for view_entry in view_entries:
            self.config.urls.append('https://github.com/' + view_entry.url)
        self.config.save_urls()
