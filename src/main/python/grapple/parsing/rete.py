from typing import Optional, Union


class Condition(object):
    @classmethod
    def is_met_by(cls, something) -> bool:
        raise NotImplementedError


class Tautology(Condition):
    @classmethod
    def is_met_by(cls, something) -> bool:
        return True


class IsNone(Condition):
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


class Path(object):
    def __init__(self, node: 'Node'):
        self.start = node
        self.tail = []

    def append(self, relation: 'Relation', node: 'Node'):
        self.tail.append((relation, node))

    def clone(self) -> 'Path':
        result = Path(self.start)
        for relation, node in self.tail:
            result.append(relation, node)

        return result


class Payload(object):
    @staticmethod
    def create(node: 'Node') -> 'Payload':
        return Payload(Path(node), {})

    def __init__(self, path: Path, table: dict):
        self.path = path
        self.table = table

    def clone(self) -> 'Payload':
        return Payload(self.path.clone(), dict(self.table))

    def append(self, relation: 'Relation', node: 'Node'):
        self.path.append(relation, node)

    def tag(self, key: str, value: Union['Entity', 'Value']):  # Or Path?
        self.table.setdefault(key, value)


class Node(object):
    def __init__(self):
        self.condition = Tautology()
        self.memory = set()

    def insert(self, something):
        raise NotImplementedError


class Parent(Node):
    def __init__(self):
        super().__init__()
        self.children = set()

    def insert(self, something):
        if something:
            self.memory.add(something)

        for child in self.children:
            child.insert(something)

    def register(self, node: Node):
        if not node:
            raise ValueError('This node is invalid')

        self.children.add(node)


class Child(Node):
    def insert(self, something):
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


class Leaf(Child):
    def __init__(self, agenda: Agenda, action: Action):
        super().__init__()
        self.agenda = agenda
        self.action = action

    def insert(self, something):
        if something:
            self.memory.add(something)

        activation = self.action.activate_with(something)
        self.agenda.add(activation)
