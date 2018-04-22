from typing import List


class Rule(object):

    def __init__(self, selectors: List['Selector'] = None):
        self._description = ''
        self._salience = 0
        self._match = []
        self._delete = []
        self._create = []
        self._selectors = {s.var: s for s in selectors} if selectors else {}

    @property
    def description(self) -> str:
        return self._description

    @property
    def salience(self) -> int:
        return self._salience

    # @property
    # def match(self) -> List[Pattern]:
    #     return self._match

    @property
    def result(self) -> List['Selector']:
        return list(self._selectors.values())
