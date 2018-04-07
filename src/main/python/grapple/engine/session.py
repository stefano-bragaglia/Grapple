from typing import Optional, List

from grapple.engine.agenda import Agenda


class Session(object):

    def __init__(self, graph: 'Graph'):
        self._agenda = Agenda()
        self._graph = graph

    @property
    def graph(self) -> 'Graph':
        return self._graph

    def insert(self, entity: 'Entity'):
        raise NotImplementedError('To be implemented...')

    def delete(self, entity: 'Entity'):
        raise NotImplementedError('To be implemented...')

    # TODO  def modify(self, entity: 'Entity'):
    # TODO      raise NotImplementedError('To be implemented...')

    def run(self) -> Optional['Record']:
        activation = self._agenda.extract()
        if activation:
            return activation.resolve()

    def run_all(self) -> List['Record']:
        records = []

        while True:
            activation = self._agenda.extract()
            if not activation:
                break

            record = activation.resolve()
            if record:
                records.append(records)

        return records
