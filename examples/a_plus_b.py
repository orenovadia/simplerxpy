from logging import getLogger, basicConfig, INFO

from simplerxpy import Observable
from simplerxpy.combined_observable import combine_latest

_logger = getLogger(__name__)
basicConfig(level=INFO)

a1 = Observable.from_iterable([2, 55]).subscribe(lambda a: _logger.info("a = {}".format(a)))

b1 = Observable.from_iterable([4, 20]).subscribe(lambda b: _logger.info("B = {}".format(b)))

n = combine_latest((a1, b1), lambda a, b: a + b).subscribe(
    lambda c: _logger.info("c1 = {}".format(c))
)
a1.run()
b1.run()


# yields:
# INFO:__main__:a = 2
# INFO:__main__:a = 55
# INFO:__main__:B = 4
# INFO:__main__:c1 = 59
# INFO:__main__:B = 20
# INFO:__main__:c1 = 75