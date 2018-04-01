from typing import Optional, List


class Relation(object):

    def __init__(self, graph: 'Graph', ident: int, tail: 'Node', head: 'Node') -> None:
        self._graph = graph
        self._ident = ident
        self._tail = tail
        self._head = head
        self._types = []

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
        elif node == self._head:
            return self._tail
        else:
            raise ValueError("'node' is invalid: <%s>" % node)

    def add_types(self, *types: str) -> None:
        for type_ in types:
            if str(type_) not in self._types:
                self._types.append(str(type_))

    def remove_types(self, *types: str) -> None:
        for type_ in types:
            if str(type_) in self._types:
                self._types.remove(str(type_))

    # noinspection PyProtectedMember
    def delete(self) -> None:
        self._tail._relations.pop(self._ident)
        self._head._relations.pop(self._ident)
        self._graph._relations.pop(self._ident)
        self._graph.release_ident(self._ident)
        self._graph = None
