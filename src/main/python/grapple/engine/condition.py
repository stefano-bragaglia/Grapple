import json

from grapple.bom.node import Node
from grapple.bom.relation import Relation


class Condition(object):

    @property
    def signature(self) -> str:
        raise NotImplementedError('To be overridden in implementing classes')

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        raise NotImplementedError('To be overridden in implementing classes')


class IsNode(Condition):
    @property
    def signature(self) -> str:
        return '()'

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        return isinstance(entity, Node)


class HasLabel(Condition):
    def __init__(self, label: str):
        self._label = label

    @property
    def signature(self) -> str:
        return '(:%s)' % self._label

    @property
    def label(self) -> str:
        return self._label

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        return self._label in entity.labels


class IsRelation(Condition):
    @property
    def signature(self) -> str:
        return '[]'

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        return isinstance(entity, Relation)


class HasType(Condition):
    def __init__(self, type: str):
        self._type = type

    @property
    def signature(self) -> str:
        return '[:%s]' % self._type

    @property
    def type(self) -> str:
        return self._type

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        return self._type in entity.types


class HasProperty(Condition):
    def __init__(self, key: str, value: 'Value'):
        self._key = key
        self._value = value

    @property
    def signature(self) -> str:
        return '{%s: %s}' % (self._key, json.dumps(self._value))

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> 'Value':
        return self._value

    def is_valid(self, entity: 'Entity', **kwargs) -> bool:
        return entity.get_property(self._key) == self._value
