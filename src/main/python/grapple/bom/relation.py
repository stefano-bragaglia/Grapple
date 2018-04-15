import json
from typing import Optional, List

from grapple.bom.entity import Entity


class Relation(Entity):

    def __init__(self, graph: 'Graph', ident: int, tail: 'Node', head: 'Node'):
        super().__init__(graph, ident)
        self._tail = tail
        self._head = head
        self._types = []

    def __repr__(self) -> str:
        content = '#%d' % self._ident
        if self._types:
            content += ' :%s' % ':'.join(self._types)
        if self._properties:
            content += ' {%s}' % ', '.join('%s: %s' % (json.dumps(i[0]), json.dumps(i[1]))
                                           for i in self._properties.items())

        return '-[%s]-' % content

    @property
    def graph(self) -> Optional['Graph']:
        return self._graph

    @property
    def ident(self) -> int:
        return self._ident

    @property
    def tail(self) -> 'Node':
        return self._tail

    @property
    def head(self) -> 'Node':
        return self._head

    @property
    def types(self) -> List[str]:
        return self._types

    def other(self, node: 'Node') -> 'Node':
        if node == self._tail:
            return self._head

        if node == self._head:
            return self._tail

        raise ValueError("'node' is invalid: <%s>" % node)

    def add_types(self, *types: str):
        for type_ in types:
            if str(type_) not in self._types:
                self._types.append(str(type_))

    def remove_types(self, *types: str):
        for type_ in types:
            if str(type_) in self._types:
                self._types.remove(str(type_))

    # noinspection PyProtectedMember
    def delete(self):
        self._tail._relations.pop(self._ident)
        self._head._relations.pop(self._ident)
        self._graph._relations.pop(self._ident)
        self._graph.release_ident(self._ident)
        self._graph = None
