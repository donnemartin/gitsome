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
import urllib
try:
    # Python 3
    import configparser
    from urllib.parse import urlparse
    from urllib.request import urlretrieve
    from urllib.error import URLError
except ImportError:
    # Python 2
    import ConfigParser as configparser
    from urlparse import urlparse
    from urllib import urlretrieve
    from urllib2 import URLError
if sys.version_info < (3, 3):
    import HTMLParser
else:
    import html as HTMLParser
