from itertools import ifilter, imap
from threading import Thread
from time import sleep

from simplerxpy.subscriber import SubscriberImpl


class Observable(object):
    def __init__(self, iterable=None):
        super(Observable, self).__init__()
        self._subscribers = []
        self._iterable = iterable or []
        self._interval = lambda: None

    @classmethod
    def from_iterable(cls, iterable):
        # type: (Iterable) -> Observable
        return cls(iterable)

    def filter(self, condition):
        self._iterable = ifilter(condition, self._iterable)
        return self

    def interval(self, sec):
        # TODO: remove when implementing zip
        self._interval = interval(sec)
        return self

    def map(self, callable_):
        self._iterable = imap(callable_, self._iterable)
        return self

    def subscribe(self, next_, error=None, end=None):
        subscriber_impl = SubscriberImpl(next_, error, end)
        self._subscribers.append(subscriber_impl)
        return self

    def subscriber(self, subscriber):
        self._subscribers.append(subscriber)
        return self

    def _publish(self, item):
        for subscriber in self._subscribers:
            subscriber.next_(item)

    def _end(self):
        for subscriber in self._subscribers:
            subscriber.end()

    def __iter(self):
        for item in self._iterable:
            self._publish(item)
            self._interval()
        self._end()

    def run(self):
        t = Thread(target=self.__iter)
        t.start()
        t.join()
        return self


def interval(sec):
    return lambda: sleep(sec)
