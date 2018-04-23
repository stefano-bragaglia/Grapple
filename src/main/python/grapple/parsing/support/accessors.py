import json

from valid_model.descriptors import Dict

from grapple.bom.container import Value
from grapple.bom.entity import Entity
from grapple.bom.node import Node


class Accessor(object):
    def get_key(self) -> str:
        raise NotImplementedError

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        raise NotImplementedError


class AccessorValue(Accessor):
    def __init__(self, value: Value, tag: str = None):
        self._value = value
        self._tag = tag

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return json.dumps(self._value)

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        return self._value


class AccessorLabels(Accessor):
    def __init__(self, var: str, tag: str = None):
        self._var = var
        self._tag = tag

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return 'labels(%s)' % self._var

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        if self._var not in payload:
            raise ValueError("'%s' not defined by this rule" % self._var)

        if not isinstance(payload[self._var], Node):
            raise ValueError("'%s' does not refer to a node" % self._var)

        return payload[self._var].labels


class AccessorTypes(Accessor):
    def __init__(self, var: str, tag: str = None):
        self._var = var
        self._tag = tag

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return 'types(%s)' % self._var

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        if self._var not in payload:
            raise ValueError("'%s' not defined by this rule" % self._var)

        if not isinstance(payload[self._var], Node):
            raise ValueError("'%s' does not refer to a relation" % self._var)

        return payload[self._var].types


class AccessorId(Accessor):
    def __init__(self, var: str, tag: str = None):
        self._var = var
        self._tag = tag

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return 'id(%s)' % self._var

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        if self._var not in payload:
            raise ValueError("'%s' not defined by this rule" % self._var)

        return payload[self._var].ident


class AccessorVariable(Accessor):
    def __init__(self, var: str, attr: str = None, tag: str = None):
        self._var = var
        self._attr = attr
        self._tag = tag

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        if not self._attr:
            return self._var

        return '%s.%s' % (self._var, self._attr)

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        if self._var not in payload:
            raise ValueError("'%s' not defined by this rule" % self._var)

        if self._attr and not payload[self._var].has_property(self._attr):
            raise ValueError("'%s' does not have a '%s' property" % (self._var, self._attr))

        return payload[self._var].get_property(self._attr)
