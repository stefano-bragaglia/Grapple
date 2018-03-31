from typing import Optional

from grapple.bom.container import Container


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
