from typing import Dict, Tuple, Optional


class Agenda(object):

    def __init__(self):
        self._queue = {}

    def append(self, rule: 'Rule', params: Dict[str, 'Entity']) -> None:
        if rule.salience not in self._queue:
            self._queue[rule.salience] = [(rule, params)]
        else:
            self._queue[rule.salience].append((rule, params))

    def next(self) -> Optional[Tuple[int, 'Rule', Dict[str, 'Entity']]]:
        for salience in sorted(self._queue, reverse=True):
            if self._queue[salience]:
                entry = self._queue[salience].pop(0)
                return salience, entry[0], entry[1]
        return None
