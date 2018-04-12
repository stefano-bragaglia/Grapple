import json
from typing import List, Union

from grapple.bom.entity import Entity
from grapple.bom.node import Node
from grapple.bom.relation import Relation

Payload = List[Union[Entity, Node, Relation]]


class Condition(object):

    @property
    def signature(self) -> str:
        raise NotImplementedError('To be overridden in implementing classes')

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        raise NotImplementedError('To be overridden in implementing classes')


class IsNode(Condition):
    @property
    def signature(self) -> str:
        return '()'

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and isinstance(payload[-1], Node)


class HasLabel(Condition):
    def __init__(self, label: str):
        self._label = label

    @property
    def signature(self) -> str:
        return '(:%s)' % self._label

    @property
    def label(self) -> str:
        return self._label

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and self._label in payload[-1].labels


class IsRelation(Condition):
    @property
    def signature(self) -> str:
        return '[]'

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and isinstance(payload[-1], Relation)


class HasType(Condition):
    def __init__(self, type: str):
        self._type = type

    @property
    def signature(self) -> str:
        return '[:%s]' % self._type

    @property
    def type(self) -> str:
        return self._type

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and self._type in payload[-1].types


class HasKey(Condition):
    def __init__(self, key: str):
        self._key = key

    @property
    def signature(self) -> str:
        return '{%s}' % self._key

    @property
    def key(self) -> str:
        return self._key

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and payload[-1].has_property(self._key)


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

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and payload[-1].get_property(self._key) == self._value


class AreEqual(Condition):
    @property
    def signature(self) -> str:
        return '=='

    def is_valid(self, payload: Payload, other: Payload = None) -> bool:
        return payload and other and payload == other
