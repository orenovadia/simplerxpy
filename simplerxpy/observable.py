from itertools import ifilter, imap
from threading import Thread
from time import sleep

from attr import attrs, attrib, Factory


@attrs
class Observable(object):
    __iterable = attrib(default=Factory(tuple))
    __nexts = attrib(default=Factory(list))
    __errors = attrib(default=Factory(list))
    __ends = attrib(default=Factory(list))

    @classmethod
    def from_iterable(cls, iterable):
        # type: (Iterable) -> Observable
        return cls(iterable)

    def filter(self, condition):
        self.__iterable = ifilter(condition, self.__iterable)
        return self

    def map(self, callable_):
        self.__iterable = imap(callable_, self.__iterable)
        return self

    def subscribe(self, next_, error, end):
        self.__nexts.append(next_)
        self.__errors.append(error)
        self.__ends.append(end)

    def __iter(self):
        for item in self.__iterable:
            for subscriber in self.__nexts:
                subscriber(item)
        for end in self.__ends:
            end()

    def run(self):
        t = Thread(target=self.__iter)
        t.start()
        t.join()
        return self


def interval(sec):
    return lambda: sleep(sec)
