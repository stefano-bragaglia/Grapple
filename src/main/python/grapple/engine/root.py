from typing import List, Optional

from grapple.engine.activation import Activation

Payload = List['Entity']


class Root(object):

    def __init__(self):
        self._children = []
        self._memory = []

    @property
    def children(self) -> List['Node']:
        return self._children

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    def purge(self, entity: 'Entity'):
        for payload in self._memory:
            if entity in payload:
                self._memory.remove(payload)

    def register(self, node: 'Node'):
        if node not in self._children:
            self._children.append(node)

    def notify(self, payload: Payload, params: 'Params' = {}, source: 'Parent' = None):
        if payload not in self._memory:
            self._memory.append(payload)

        for child in self._children:
            child.notify(payload, params)


class Alpha(object):

    def __init__(self, condition: 'Condition' = None, variable: str = None):
        self._children = []
        self._condition = condition
        self._memory = []
        self._variable = variable

    @property
    def children(self) -> List['Node']:
        return self._children

    @property
    def condition(self) -> Optional['Condition']:
        return self._condition

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    @property
    def variable(self) -> str:
        return self._variable

    def purge(self, entity: 'Entity'):
        for payload in self._memory:
            if entity in payload:
                self._memory.remove(payload)

    def register(self, node: 'Node'):
        if node not in self._children:
            self._children.append(node)

    def notify(self, payload: Payload, params: 'Params' = {}, source: 'Parent' = None):
        if self._condition and self._condition.passes(payload):
            if payload not in self._memory:
                self._memory.append(payload)

            for child in self._children:
                child.notify(payload, params)

    def hook(self, parent: 'Node'):
        parent.register(self)


class Beta(object):

    def __init__(self):
        self._memory = []

    def purge(self, entity: 'Entity'):
        for payload in self._memory:
            if entity in payload:
                self._memory.remove(payload)


class Leaf(object):

    def __init__(self, agenda: 'Agenda', rule: 'Rule'):
        self._agenda = agenda
        self._rule = rule
        self._memory = []

    @property
    def agenda(self) -> 'Agenda':
        return self._agenda

    @property
    def rule(self) -> 'Rule':
        return self._rule

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    def purge(self, entity: 'Entity'):
        for payload in self._memory:
            if entity in payload:
                self._memory.remove(payload)

    def notify(self, payload: Payload, params: 'Params' = {}, source: 'Parent' = None):
        if payload not in self._memory:
            self._memory.append(payload)

        activation = Activation(self._rule, params)
        self._agenda.append(activation)

    def hook(self, parent: 'Node'):
        parent.register(self)
