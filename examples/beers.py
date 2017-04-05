from functools import partial
from logging import getLogger, basicConfig, INFO

from simplerxpy import Observable

# https://yakovfain.com/2017/04/03/rx-reactive-libraries/
_logger = getLogger(__name__)
basicConfig(level=INFO)

beers = [
    {'name': 'Stella', 'country': 'Belgium', 'price': 9.50},
    {'name': 'Sam Adams', 'country': 'USA', 'price': 8.50},
    {'name': 'Bud Light', 'country': 'USA', 'price': 6.50},
    {'name': 'Brooklyn Lager', 'country': 'USA', 'price': 8.00},
    {'name': 'Sapporo', 'country': 'Japan', 'price': 7.50}
]

# The observer will be provided at the time of subscription
o = Observable.from_iterable(beers)


def show_all():
    # # The function subscribe() receives the Observer, represented by three functions
    o.subscribe(
        lambda beer: _logger.info('Subscriber got {}'.format(beer)),  # handling the arrived data
        lambda error: _logger.error('Error: {}'.format(error)),  # an error arrived
        partial(_logger.info, "Stream over")  # the signal that the stream completed arrived
    )

    o.run()


def only_cheap_ones():
    o.filter(lambda beer: beer['price'] < 8).map(lambda beer: '{name}: {price}$'.format(**beer)).subscribe(
        lambda beer: _logger.info('Subscriber got {}'.format(beer)),  # handling the arrived data
        lambda error: _logger.error('Error: {}'.format(error)),  # an error arrived
        partial(_logger.info, "Stream over")  # the signal that the stream completed arrived

    )
    o.run()


if __name__ == '__main__':
    only_cheap_ones()
