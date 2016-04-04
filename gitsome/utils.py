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

def format_repo(repo):
    """Formats a repo tuple for pretty print.

    Example:
        Input:  ('donnemartin', 'gitsome')
        Output: donnemartin/gitsome

    Args:
        * arg: A tuple that contains the user and repo.

    Returns:
        A string of the form user/repo.
    """
    return '/'.join(repo)

def listify(items):
    """Puts each list element in its own list.

    Example:
        Input: [a, b, c]
        Output: [[a], [b], [c]]

    This is needed for tabulate to print rows [a], [b], and [c].

    Args:
        * items: A list to listify.

    Returns:
        A list that contains elements that are listified.
    """
    output = []
    for item in items:
        item_list = []
        item_list.append(item)
        output.append(item_list)
    return output

def print_error(message):
    """Prints the given message using click.secho with fg='red'.

    Args:
        * message: A string to be printed.

    Returns:
        None.
    """
    click.secho(message, fg='red')
