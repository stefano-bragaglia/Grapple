from typing import List

from grapple.bom.node import Node


class Graph(object):

    def __init__(self):
        self._pool = []
        self._nodes = {}
        self._relations = {}

    @property
    def nodes(self) -> List['Node']:
        return list(self._nodes.values())

    @property
    def relations(self) -> List['Relation']:
        return list(self._relations.values())

    def create_node(self) -> 'Node':
        ident = self.next_ident()
        self._nodes[ident] = Node(self, ident)
        self.lock_ident(ident)

        return self._nodes[ident]

    def next_ident(self) -> int:
        if self._pool:
            return self._pool[0]

        return len(self._nodes) + len(self._relations)

    def lock_ident(self, ident: int) -> None:
        if ident in self._pool:
            self._pool.remove(ident)

    def release_ident(self, ident: int) -> None:
        self._pool.append(ident)
