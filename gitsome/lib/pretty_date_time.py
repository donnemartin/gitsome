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

from __future__ import print_function
from __future__ import division

import calendar
from datetime import datetime
import pytz
import time


def pretty_date_time(date_time):
    """Prints a pretty datetime similar to what's seen on Hacker News.

    Gets a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc.

    Adapted from: http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python  # NOQA

    Args:
        * date_time: An instance of datetime.

    Returns:
        A string that represents the pretty datetime.
    """
    now = datetime.now(pytz.utc)
    if type(date_time) is int:
        diff = now - datetime.fromtimestamp(date_time)
    elif type(date_time) is time.struct_time:
        date_time = datetime.fromtimestamp(calendar.timegm(date_time),
                                           tz=pytz.utc)
        diff = now - date_time
    elif isinstance(date_time, datetime):
        diff = now - date_time
    elif not date_time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "1 minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "1 hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " week(s) ago"
    if day_diff < 365:
        return str(day_diff // 30) + " month(s) ago"
    return str(day_diff // 365) + " year(s) ago"
