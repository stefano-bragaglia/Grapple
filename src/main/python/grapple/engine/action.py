from typing import Dict, List, Union

from grapple.bom.container import Value


class Action(object):

    def __init__(self, pattern: 'Pattern') -> None:
        self._pattern = pattern

    @property
    def pattern(self) -> 'Pattern':
        return self._pattern

    def apply(self, rule: 'Rule', params: Dict[str, 'Entity']) -> List[Dict[str, Union[None, Value, 'Entity']]]:
        raise NotImplementedError()