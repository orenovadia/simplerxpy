from functools import partial

from simplerxpy import Observable
from simplerxpy.subscriber import SubscriberImpl

_did_not_receive = object()


class CombinedObservable(Observable):
    def __init__(self, observables, combiner_subscriber):
        super(CombinedObservable, self).__init__()
        n = len(observables)
        self.__lasts = [_did_not_receive, ] * n
        self.__ended = [False, ] * n
        self.__feeding_subscribers = [
            SubscriberImpl(
                partial(self.__next_, i),
                partial(self.__error, i),
                partial(self.__end, i),
            ) for i in range(n)
            ]
        self.__combiner_subscriber = combiner_subscriber
        self.__connect(observables)

    def __connect(self, observables):
        for observable, subscriber in zip(observables, self.__feeding_subscribers):
            observable.subscriber(subscriber)
        return self

    def __end(self, subscriber_id):
        self.__ended[subscriber_id] = True
        if all(self.__ended):
            self._end()

    def __next_(self, subscriber_id, item):
        self.__lasts[subscriber_id] = item
        if any(elem is _did_not_receive for elem in self.__lasts):
            return
        return self._publish(self.__combiner_subscriber.next_(*tuple(self.__lasts)))

    def __error(self, subscriber_id, error):
        pass


def combine_latest(observables, next_):
    return CombinedObservable(observables, SubscriberImpl(next_))
