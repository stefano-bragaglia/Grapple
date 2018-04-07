from typing import Dict, Tuple, Optional, Union


class Agenda(object):
    # TODO Graph might be needed to assure that we insert rules and parameters from the same graph

    def __init__(self):
        self._queue = {}

    def extract(self) -> Optional['Activation']:
        for salience in sorted(self._queue, reverse=True):
            if self._queue[salience]:
                return self._queue[salience].pop(0)

    def append(self, activation: 'Activation'):
        self._queue.setdefault(activation.salience, []).append(activation)
