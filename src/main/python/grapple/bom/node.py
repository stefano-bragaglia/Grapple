import json
from typing import Optional, List, Dict

from grapple.bom.container import Value
from grapple.bom.entity import Entity
from grapple.bom.relation import Relation
from grapple.engine.descriptors import Direction


class Node(Entity):

    def __init__(self, graph: 'Graph', ident: int):
        super().__init__(graph, ident)
        self._labels = []
        self._relations = {}

    def __repr__(self) -> str:
        content = '#%d' % self._ident
        if self._labels:
            content += ' :%s' % ':'.join(self._labels)
        if self._properties:
            content += ' {%s}' % ', '.join('%s: %s' % (json.dumps(i[0]), json.dumps(i[1]))
                                           for i in self._properties.items())

        return '(%s)' % content

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

    def has_relations(self, *types: str, properties: Dict[str, Value] = None) -> bool:
        pass

    def find_relations(self, *types: str, direction: Direction = Direction.ANY, properties: Dict[str, Value] = None) -> \
            List['Relation']:
        types = [type_ for type_ in types]
        items = (properties if properties else {}).items()

        relations = []
        for relation in self._relations.values():
            if direction == Direction.OUTGOING:
                has_direction = relation.tail == self
            elif direction == Direction.INCOMING:
                has_direction = relation.head == self
            else:
                has_direction = True
            has_types = types <= relation.types
            has_items = items <= relation.get_properties().items()
            is_new = relation not in relations
            if has_direction and has_types and has_items and is_new:
                relations.append(relation)

        return relations
