# -*- coding: utf-8 -*-
"""A collection of useful utilities."""
import collections
import datetime
import re

from requests import compat

# with thanks to https://code.google.com/p/jquery-localtime/issues/detail?id=4
ISO_8601 = re.compile("^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0"
                      "[1-9]|[1-2][0-9])(T(2[0-3]|[0-1][0-9]):([0-5][0-9]):([0"
                      "-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[0-1][0-9]):[0-5]["
                      "0-9])?)?$")


def timestamp_parameter(timestamp, allow_none=True):
    """Function to check the conformance of timestamps passed by users.

    This will check that a string is a valid format and allow users to pass a
    datetime object which we will then convert to a proper ISO8601 date-time
    string.

    :param timestamp: string to be validated or datetime object to be
        converted.
    :param bool allow_none: whether or not to allow timestamp to be None.
        Default: ``True``
    :returns: valid ISO8601 string
    :rtype: str
    :raises: ValueError
    """
    if timestamp is None:
        if allow_none:
            return None
        raise ValueError("Timestamp value cannot be None")

    if isinstance(timestamp, datetime.datetime):
        return timestamp.isoformat() + 'Z'

    if isinstance(timestamp, compat.basestring):
        if not ISO_8601.match(timestamp):
            raise ValueError(("Invalid timestamp: %s is not a valid ISO-8601"
                              " formatted date") % timestamp)
        return timestamp

    raise ValueError("Cannot accept type %s for timestamp" % type(timestamp))


class UTC(datetime.tzinfo):

    """Yet another UTC reimplementation, to avoid a dependency on pytz or
    dateutil."""

    ZERO = datetime.timedelta(0)

    def __repr__(self):
        return 'UTC()'

    def dst(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return 'UTC'

    def utcoffset(self, dt):
        return self.ZERO


def stream_response_to_file(response, path=None):
    """Stream a response body to the specified file.

    Either use the ``path`` provided or use the name provided in the
    ``Content-Disposition`` header.

    :param response: A Response object from requests
    :type response: requests.models.Response
    :param str path: The full path and file name used to save the response
    :return: path to the file
    :rtype: str
    """
    pre_opened = False
    fd = None
    filename = None
    if path:
        if isinstance(getattr(path, 'write', None), collections.Callable):
            pre_opened = True
            fd = path
            filename = getattr(fd, 'name', None)
        else:
            fd = open(path, 'wb')
            filename = path
    else:
        header = response.headers['content-disposition']
        i = header.find('filename=') + len('filename=')
        filename = header[i:]
        fd = open(filename, 'wb')

    for chunk in response.iter_content(chunk_size=512):
        fd.write(chunk)

    if not pre_opened:
        fd.close()

    return filename
