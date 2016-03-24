# -*- coding: utf-8 -*-
from requests.compat import is_py3


class NullObject(object):
    def __init__(self, initializer=None):
        self.__dict__['initializer'] = initializer

    def __int__(self):
        return 0

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __str__(self):
        return ''

    def __unicode__(self):
        return '' if is_py3 else ''.decode()

    def __repr__(self):
        return '<NullObject({0})>'.format(
            repr(self.__getattribute__('initializer'))
            )

    def __getitem__(self, index):
        return self

    def __setitem__(self, index, value):
        pass

    def __getattr__(self, attr):
        return self

    def __setattr__(self, attr, value):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, other):
        return False

    def __iter__(self):
        return iter([])

    def __next__(self):
        raise StopIteration

    next = __next__

    def is_null(self):
        return True
