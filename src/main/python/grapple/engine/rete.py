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

    def __init__(self, condition: 'Condition', parent: 'Node', variable: str = None):
        self._condition = condition
        self._memory = []
        self._children = []
        self._variable = variable

        parent.register(self)

    @property
    def condition(self) -> Optional['Condition']:
        return self._condition

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    @property
    def children(self) -> List['Node']:
        return self._children

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


class Beta(object):

    def __init__(self, condition: 'Condition', parent_sx: 'Node', parent_dx: 'Node', variable: str = None):
        self._condition = condition
        self._memory = []
        self._children = []
        self._variable = variable
        self._parent_sx = parent_sx
        self._parent_dx = parent_dx

        parent_sx.register(self)
        parent_dx.register(self)

    @property
    def condition(self) -> Optional['Condition']:
        return self._condition

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    @property
    def children(self) -> List['Node']:
        return self._children

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
        # TODO Should probably change Entity to Payload in condition.*
        if source == self._parent_sx:
            for other in self._parent_dx.memory:
                if self._condition and self._condition.passes(payload, other):
                    if other not in payload:
                        temp = payload + other
                    else:
                        temp = payload
                    if temp not in self._memory:
                        self._memory.append(temp)

                    for child in self._children:
                        child.notify(temp, params, self)
        elif source == self._parent_dx:
            for other in self._parent_sx.memory:
                if self._condition and self._condition.passes(other, payload):
                    if payload not in other:
                        temp = other + payload
                    else:
                        temp = other
                    if temp not in self._memory:
                        self._memory.append(temp)

                    for child in self._children:
                        child.notify(temp, params, self)
        else:
            raise ValueError('Unexpected source: <%s>' % source)


class Leaf(object):

    def __init__(self, parent: 'Node', rule: 'Rule', agenda: 'Agenda'):
        self._memory = []
        self._rule = rule
        self._agenda = agenda

        parent.register(self)

    @property
    def memory(self) -> List[Payload]:
        return self._memory

    @property
    def rule(self) -> 'Rule':
        return self._rule

    @property
    def agenda(self) -> 'Agenda':
        return self._agenda

    def purge(self, entity: 'Entity'):
        for payload in self._memory:
            if entity in payload:
                self._memory.remove(payload)

    def notify(self, payload: Payload, params: 'Params' = {}, source: 'Parent' = None):
        if payload not in self._memory:
            self._memory.append(payload)

        activation = Activation(self._rule, params)
        self._agenda.append(activation)
