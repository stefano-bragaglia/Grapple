from typing import Optional


class Relation(object):

    def __init__(self, graph: 'Graph', ident: int, tail: 'Node', head: 'Node') -> None:
        self._graph = graph
        self._ident = ident
        self._tail = tail
        self._head = head

    def __repr__(self) -> str:
        return '%s-[#%d]->%s' % (self.tail, self._ident, self._head)

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

    def other(self, node: 'Node') -> 'Node':
        if node == self._tail:
            return self._head
        elif node == self._head:
            return self._tail
        else:
            raise ValueError("'node' is invalid: <%s>" % node)

    # noinspection PyProtectedMember
    def delete(self) -> None:
        self._tail._relations.pop(self._ident)
        self._head._relations.pop(self._ident)
        self._graph._relations.pop(self._ident)
        self._graph.release_ident(self._ident)
        self._graph = None
