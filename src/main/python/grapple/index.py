from typing import List


class Index(object):

    def __init__(self, graph: 'Graph'):
        self._graph = graph
        self._by_kind = {}
        self._with_keys = {}

    def add(self, entity: 'Entity') -> None:
        if entity.graph != self._graph:
            raise ValueError("'entity' is invalid: <%s>" % entity)

        for kind in entity.kinds:
            if kind not in self._by_kind:
                self._by_kind[kind] = [entity]
            elif entity not in self._by_kind[kind]:
                self._by_kind[kind].append(entity)

            if kind not in self._with_keys:
                self._with_keys[kind] = {}
            for key in entity.keys:
                if key not in self._with_keys[kind]:
                    self._with_keys[kind][key] = {}
                value = entity.get_property(key)
                if value not in self._with_keys[kind][key]:
                    self._with_keys[kind][key][value] = [entity]
                elif entity not in self._with_keys[kind][key][value]:
                    self._with_keys[kind][key][value].append(entity)

    def find(self, *kinds: str, key: str = None, value: 'Value' = None) -> List['Entity']:
        if key is None or value is None:
            entities = None
            for kind in kinds:
                if kind in self._by_kind:
                    if entities is None:
                        entities = set(self._by_kind[kind])
                    else:
                        entities = entities.intersection(self._by_kind[kind])
                    if not entities:
                        return []
            return list(entities)

    def remove(self, entity: 'Entity') -> None:
        if entity.graph != self._graph:
            raise ValueError("'entity' is invalid: <%s>" % entity)

        for kind in entity.kinds:
            if kind in self._by_kind and entity in self._by_kind[kind]:
                self._by_kind[kind].remove(entity)

            if kind in self._with_keys:
                for key in entity.keys:
                    if key in self._with_keys[kind]:
                        value = entity.get_property(key)
                        if value in self._with_keys[kind][key] and entity in self._with_keys[kind][key][value]:
                            self._with_keys[kind][key][value].remove(entity)
