from typing import Optional

from grapple.tentative.engine.descriptors import Direction


class Path(object):
    def __init__(self, node: 'Node'):
        self.start = node
        self.chain = []

    def append(self, relation: 'Relation', node: 'Node'):
        self.chain.append((relation, node))


class Payload(object):
    def __init__(self, node: 'Node'):
        self._current = node
        self._path = Path(node)
        self.pattern = [self._path]

    @property
    def current(self) -> 'Entity':
        return self._current

    def append(self, entity: 'Entity'):
        if type(self._current) is Node:
            if type(entity) is Node:
                # noinspection PyTypeChecker
                self._path = Path(entity)

        else:
            if type(entity) is 'Relation':
                raise ValueError('This entity is invalid')

        self._current = entity


class Condition(object):
    @property
    def signature(self) -> str:
        raise NotImplementedError

    @classmethod
    def is_met_by(cls, payload: 'Payload') -> bool:
        raise NotImplementedError


class Tautology(Condition):
    @property
    def signature(self) -> str:
        return 'TRUE'

    @classmethod
    def is_met_by(cls, payload: 'Payload') -> bool:
        return True


class HasLabel(Condition):
    def __init__(self, label: str):
        self.label = label

    @property
    def signature(self) -> str:
        return 'has_label(%s)' % self.label

    def is_met_by(self, payload: 'Payload') -> bool:
        type(payload.current) is Node
        pass


class IsNone(Condition):
    @property
    def signature(self) -> str:
        return 'is_none()'

    @classmethod
    def is_met_by(cls, something) -> bool:
        return bool(something is None)


class Agenda(object):
    def __init__(self):
        self._index = {}

    def add(self, activation: 'Activation'):
        self._index.setdefault(activation.salience, set()).add(activation)

    def is_empty(self) -> bool:
        return not self._index

    def pop(self) -> Optional['Activation']:
        if not self._index:
            return None

        salience = max(self._index.keys())
        activation = self._index[salience].pop()
        if not self._index[salience]:
            self._index.pop(salience)
        return activation


class Activation(object):
    def __init__(self, something, action: 'Action'):
        self.something = something
        self.action = action
        self.salience = 5

    def execute(self):
        self.action.execute(self.something)


class Action(object):
    def activate_with(self, something) -> Activation:
        return Activation(something, self)

    def execute(self, something):
        raise NotImplementedError


class Return(Action):
    def __init__(self, item: 'Returnable'):
        self.item = item

    def execute(self, something):
        content = None
        if self.item.function == '*':
            pass
        elif self.item.function == 'coalesce':
            pass
        elif self.item.function == 'head':
            pass
        elif self.item.function == 'id':
            pass
        elif self.item.function == 'keys':
            pass
        elif self.item.function == 'labels':
            pass
        elif self.item.function == 'length':
            pass
        elif self.item.function == 'nodes':
            pass
        elif self.item.function == 'relations':
            pass
        elif self.item.function == 'properties':
            pass
        elif self.item.function == 'tail':
            pass
        elif self.item.function == 'types':
            pass
        elif self.item.entity:
            if self.item.field:
                pass
            else:
                pass
        else:
            content = self.item.value

        if self.item.synonym:
            print(self.item.synonym, '=', content)
        else:
            print(content)


class Create(Action):
    def __init__(self, graph: 'Graph', pattern: 'Pattern'):
        self.graph = graph
        self.pattern = pattern

    def execute(self, something):
        node = self._create_node(self.graph, self.pattern.node)
        for step in self.pattern.chain:
            temp = self._create_node(self.graph, step.node)
            if step.relation.direction == Direction.INCOMING:
                self._create_relation(temp, node, step.relation)
            else:
                self._create_relation(node, temp, step.relation)
                node = temp

    @staticmethod
    def _create_node(graph, node):
        result = graph.create_node()
        for label in node.labels:
            result.add_labels(label)
        for key in node.properties:
            value = node.properties[key]
            result.set_property(key, value)

        return result

    @staticmethod
    def _create_relation(tail, head, relation):
        result = tail.create_relation_to(head)
        for type_ in relation.types:
            result.add_types(type_)
        for key in relation.properties:
            value = relation.properties[key]
            result.set_property(key, value)

        return result


class Node(object):
    def __init__(self):
        self.condition = Tautology()
        self.memory = set()

    def insert(self, entity: 'Entity', payload: Payload, sender: 'Parent' = None):
        raise NotImplementedError


class Parent(Node):
    def __init__(self):
        super().__init__()
        self.children = set()

    def insert(self, entity: 'Entity', payload: Payload, sender: 'Parent' = None):
        if entity:
            self.memory.add(entity)

        for child in self.children:
            child.insert(entity, payload)

    def register(self, node: Node):
        if not node:
            raise ValueError('This node is invalid')

        self.children.add(node)


class Child(Node):
    def insert(self, entity: 'Entity', payload: Payload, sender: 'Parent' = None):
        raise NotImplementedError

    def link(self, parent: Parent) -> 'Child':
        parent.register(self)
        return self


class Root(Parent):
    def __init__(self):
        super().__init__()


class Alfa(Parent, Child):
    def __init__(self, condition: Condition):
        super().__init__()
        if not condition:
            raise ValueError('This condition is invalid')

        self._condition = condition


class Beta(Node):
    def __init__(self):
        super().__init__()


class Leaf(Child):
    def __init__(self, agenda: Agenda, action: Action):
        super().__init__()
        self.agenda = agenda
        self.action = action

    def insert(self, entity: 'Entity', payload: Payload, sender: 'Parent' = None):
        if entity:
            self.memory.add(entity)

        activation = self.action.activate_with(entity)
        self.agenda.add(activation)
