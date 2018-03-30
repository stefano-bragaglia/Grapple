from typing import List

from grapes.bom.node import Node


class Graph(object):

    def __init__(self):
        self._pool = []
        self._nodes = {}
        self._relations = {}

    def __repr__(self) -> str:
        return '<N: %d, R: %d>' % (len(self._nodes), len(self._relations))

    @property
    def nodes(self) -> List['Node']:
        return list(self._nodes)

    def create_node(self) -> 'Node':
        ident = self._next_ident()
        self._nodes[ident] = Node(self, ident)
        return self._nodes[ident]

    def _next_ident(self) -> int:
        if self._pool:
            return self._pool.pop(0)
        return len(self._nodes) + len(self._relations)


if __name__ == '__main__':
    g = Graph()
    n1 = g.create_node()
    n2 = g.create_node()
    n3 = g.create_node()
    r4 = n1.create_relation_to(n2)
    r5 = n2.create_relation_to(n3)
    print(g)

    try:
        n2.delete()
    except Exception as e:
        r4.delete()
        r5.delete()
        n2.delete()
    finally:
        n6 = g.create_node()
        r7 = n1.create_relation_to(n6)
        r8 = n6.create_relation_to(n3)
    print(g)

    print('n1:', n1, 'n2:', n2, 'n3:', n3, 'r4:', r4, 'r5:', r5, 'n6:', n6, 'r7:', r7, 'r8:', r8)
