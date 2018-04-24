from typing import Dict, List, Optional

from grapple.bom.container import Value
from grapple.engine.descriptors import Direction


class Pattern(object):
    pass


class NodePattern(Pattern):
    def __init__(self, element: Dict[str, object]):
        if 'type' not in element:
            raise ValueError("'element' is missing the type")
        if element['type'] != 'node':
            raise ValueError("'element' is not a node")

        self._var = str(element['variable']) if 'variable' in element and element['variable'] else None
        self._labels = element['flags'] if 'flags' in element and element['flags'] else []
        self._attributes = element['attributes'] if 'attributes' in element and element['attributes'] else {}

    @property
    def var(self) -> Optional[str]:
        return self._var

    @property
    def labels(self) -> List[str]:
        return self._labels

    @property
    def properties(self) -> List[str]:
        return list(self._attributes.keys())

    def get_value(self, key: str) -> Optional[Value]:
        if key not in self._attributes:
            return None

        return self._attributes[key]


class RelationPattern(Pattern):
    def __init__(self, element: Dict[str, object]):
        if 'type' not in element:
            raise ValueError("'element' is missing the type")
        if element['type'] != 'relation':
            raise ValueError("'element' is not a relation")

        if 'direction' not in element:
            self._dir = Direction.ANY
        elif element['direction'] == Direction.OUTGOING.value:
            self._dir = Direction.OUTGOING
        elif dir == Direction.INCOMING.value:
            self._dir = Direction.INCOMING
        else:
            self._dir = Direction.ANY
        self._var = str(element['variable']) if 'variable' in element and element['variable'] else None
        self._labels = element['flags'] if 'flags' in element and element['flags'] else []
        self._attributes = element['attributes'] if 'attributes' in element and element['attributes'] else {}

    @property
    def dir(self) -> Direction:
        return self._dir

    @property
    def var(self) -> Optional[str]:
        return self._var

    @property
    def types(self) -> List[str]:
        return self._types

    @property
    def properties(self) -> List[str]:
        return list(self._attributes.keys())

    def get_value(self, key: str) -> Optional[Value]:
        if key not in self._attributes:
            return None

        return self._attributes[key]


class PathPattern(Pattern):
    def __init__(self, elements: List[Dict[str, object]]):
        self._elements = []
        for element in elements:
            if 'type' not in element:
                raise ValueError("'element' is missing the type: %s" % element)

            if element['type'] == 'node':
                self._elements.append(NodePattern(element))
            elif element['type'] == 'relation':
                self._elements.append(RelationPattern(element))
        if len(self._elements) % 2 != 1:
            raise ValueError("'elements' should contain an odd number of alternated nodes and relations: %s" % elements)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos >= len(self._elements):
            raise StopIteration

        elif self._pos == 0:
            node = self._elements[self._pos]
            self._pos += 1
            return node

        else:
            relation = self._elements[self._pos]
            node = self._elements[self._pos + 1]
            self._pos += 2
            return relation, node

    @property
    def elements(self) -> List[Pattern]:
        return self._elements


class MatchPattern(Pattern):
    def __init__(self, paths: List[List[Dict[str, object]]]):
        self._paths = [PathPattern(path) for path in paths]

    @property
    def paths(self) -> List[PathPattern]:
        return self._paths
