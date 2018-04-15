from typing import Optional, List

from grapple.bom.entity import Entity
from grapple.bom.relation import Relation


class Node(Entity):

    def __init__(self, graph: 'Graph', ident: int):
        super().__init__(graph, ident)
        self._labels = []
        self._relations = {}

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        elif self is other:
            return True
        else:
            same_graph = self._graph is other._graph
            same_ident = self._ident == other._ident
            return same_graph and same_ident

    def __hash__(self):
        return self._graph.hash() ^ self._ident

    @property
    def graph(self) -> Optional['Graph']:
        return self._graph

    @property
    def ident(self) -> int:
        return self._ident

    @property
    def labels(self) -> List[str]:
        return self._labels

    @property
    def relations(self) -> List['Relation']:
        return list(self._relations.values())

    def add_labels(self, *labels: str):
        for label in labels:
            if str(label) not in self._labels:
                self._labels.append(str(label))

    def remove_labels(self, *labels: str):
        for label in labels:
            if str(label) in self._labels:
                self._labels.remove(str(label))

    # noinspection PyProtectedMember
    def create_relation_to(self, node: 'Node') -> 'Relation':
        if node.graph != self._graph:
            raise ValueError("'node' is invalid: <%s>" % node)

        ident = self._graph.next_ident()
        relation = Relation(self._graph, ident, self, node)
        self._graph.lock_ident(ident)
        self._graph._relations[ident] = relation
        self._relations[ident] = relation
        node._relations[ident] = relation

        return relation

    # noinspection PyProtectedMember
    def delete(self) -> None:
        if self._relations:
            raise Exception('Node not empty')

        self._graph._nodes.pop(self._ident)
        self._graph.release_ident(self._ident)
        self._graph = None
