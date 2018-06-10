import json
from typing import Dict, List, Optional, Union

from grapple.tentative.engine.descriptors import Direction

Value = Union[bool, int, float, str, List[bool], List[int], List[float], List[str]]
Properties = Dict[str, Value]


class Container(object):

    def __init__(self):
        self._properties = {}

    @property
    def keys(self) -> List[str]:
        return list(self._properties.keys())

    def get_properties(self, keys: List[str] = None) -> Properties:
        if keys is None:
            keys = list(self._properties.keys())

        return {key: self._properties[key] for key in keys if key in self._properties}

    def get_property(self, key: str, default: Value = None) -> Optional[Value]:
        if key not in self._properties:
            return default

        return self._properties[key]

    def has_property(self, key: str) -> bool:
        return key in self._properties

    def remove_property(self, key: str) -> Optional[Value]:
        if key in self._properties:
            return self._properties.pop(key)

    def set_property(self, key: str, value: Value):
        if value:
            self._properties[key] = value
        elif key in self._properties:
            self._properties.pop(key)


class Entity(Container):

    def __init__(self, graph: 'Graph', ident: int) -> None:
        super().__init__()
        self._graph = graph
        self._ident = ident

    @property
    def graph(self) -> Optional['Graph']:
        return self._graph

    @property
    def ident(self) -> int:
        return self._ident


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

    def find_relations(
            self, *types: str, direction: Direction = Direction.ANY, properties: Dict[str, Value] = None) -> \
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


class Graph(object):

    def __init__(self):
        self._pool = []
        self._nodes = {}
        self._sessions = set()
        self._relations = {}

    @property
    def nodes(self) -> List['Node']:
        return list(self._nodes.values())

    @property
    def relations(self) -> List['Relation']:
        return list(self._relations.values())

    def register(self, session: 'Session'):
        if not session:
            raise ValueError('Session is invalid')

        self._sessions.add(session)

    def unregister(self, session: 'Session'):
        self._sessions.discard(session)

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

    def find_nodes(self, *labels: str, properties: Dict[str, Value] = None) -> List['Node']:
        labels = [label for label in labels]
        items = (properties if properties else {}).items()

        nodes = []
        for node in self.nodes:
            has_labels = labels <= node.labels
            has_items = items <= node.get_properties().items()
            is_new = node not in nodes
            if has_labels and has_items and is_new:
                nodes.append(node)

        return nodes
