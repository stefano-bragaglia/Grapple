import json

from valid_model.descriptors import Dict, List

from grapple.bom.container import Value
from grapple.bom.entity import Entity
from grapple.bom.node import Node


class Accessor(object):
    def get_key(self) -> str:
        raise NotImplementedError

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        raise NotImplementedError


class AccessorValue(Accessor):
    def __init__(self, accessor: Dict[str, object]):
        if 'content' not in accessor or not accessor['content']:
            raise ValueError("'accessor' requires some content")
        self._value = str(accessor['content'])
        self._tag = str(accessor['as']) if 'as' in accessor and accessor['as'] else None

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return json.dumps(self._value)

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        return self._value


class AccessorLabels(Accessor):
    def __init__(self, accessor: Dict[str, object]):
        if 'content' not in accessor or not accessor['content']:
            raise ValueError("'accessor' requires some content")
        self._var = str(accessor['content'])
        self._tag = str(accessor['as']) if 'as' in accessor and accessor['as'] else None

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
    def __init__(self, accessor: Dict[str, object]):
        if 'content' not in accessor or not accessor['content']:
            raise ValueError("'accessor' requires some content")
        self._var = str(accessor['content'])
        self._tag = str(accessor['as']) if 'as' in accessor and accessor['as'] else None

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
    def __init__(self, accessor: Dict[str, object]):
        if 'content' not in accessor or not accessor['content']:
            raise ValueError("'accessor' requires some content")
        self._var = str(accessor['content'])
        self._tag = str(accessor['as']) if 'as' in accessor and accessor['as'] else None

    def get_key(self) -> str:
        if self._tag:
            return self._tag

        return 'id(%s)' % self._var

    def get_value(self, payload: Dict[str, Entity]) -> Value:
        if self._var not in payload:
            raise ValueError("'%s' not defined by this rule" % self._var)

        return payload[self._var].ident


class AccessorVariable(Accessor):
    def __init__(self, accessor: Dict[str, object]):
        if 'content' not in accessor or not accessor['content']:
            raise ValueError("'accessor' requires some content")
        self._var = str(accessor['content'])
        self._attr = str(accessor['field']) if 'field' in accessor and accessor['field'] else None
        self._tag = str(accessor['as']) if 'as' in accessor and accessor['as'] else None

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


class AccessorList(object):
    def __init__(self, accessors=List[Dict[str, object]]):
        self._pos = None
        self._accessors = []
        for accessor in accessors:
            if 'type' not in accessor:
                raise ValueError("'accessor' is missing the type: %s" % accessor)

            if accessor['type'] == 'value':
                self._accessors.append(AccessorValue(accessor))
            elif accessor['type'] == 'labels':
                self._accessors.append(AccessorLabels(accessor))
            elif accessor['type'] == 'types':
                self._accessors.append(AccessorTypes(accessor))
            elif accessor['type'] == 'id':
                self._accessors.append(AccessorId(accessor))
            elif accessor['type'] == 'accessor':
                self._accessors.append(AccessorVariable(accessor))
            else:
                raise ValueError("'accessor' has an unknown type: %s" % accessor['type'])

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos is None:
            self._pos = 0

        if self._pos >= len(self._accessors):
            self._pos = None
            raise StopIteration

        else:
            accessor = self._accessors[self._pos]
            self._pos += 1
            return accessor

    @property
    def accessors(self) -> List[Accessor]:
        return self._accessors