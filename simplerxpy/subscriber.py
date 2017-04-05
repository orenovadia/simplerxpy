from abc import ABCMeta, abstractmethod

from attr import attrs, attrib


class Subscriber(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def next_(self, item):
        pass

    @abstractmethod
    def error(self, error):
        pass

    @abstractmethod
    def end(self, item):
        pass


def _null_function(*args, **kwargs):
    pass


class SubscriberImpl(object):
    def __init__(self, next_, error=None, end=None):
        self.next_ = next_
        self.error = error or _null_function
        self.end = end or _null_function
