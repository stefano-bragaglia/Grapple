from typing import Dict, Union

from grapple.bom.container import Value
from grapple.bom.entity import Entity

Params = Dict[str, Union[None, Value, Entity]]


class Activation(object):
    # TODO Replace Rule with just Action?

    def __init__(self, rule: 'Rule', params: 'Params'):
        self._rule = rule
        self._params = params

    @property
    def params(self) -> 'Params':
        return self._params

    @property
    def rule(self) -> 'Rule':
        return self._rule

    @property
    def salience(self) -> int:
        return self._rule.salience

    def resolve(self) -> 'Record':
        return self._rule.apply(self._params)
