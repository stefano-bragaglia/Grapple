import json
from typing import Dict, List

from grapple.bom.container import Value
from grapple.engine.descriptors import Direction

Properties = Dict[str, Value]


class Node(object):
    def __init__(self, parameter: str = None, labels: List[str] = None, properties: Properties = None):
        self.parameter = parameter
        self.labels = labels if labels else []
        self.properties = properties if properties else {}

    def __repr__(self) -> str:
        labels = ':' + ':'.join(self.labels) if self.labels else None
        properties = json.dumps(self.properties, sort_keys=True) if self.properties else None
        content = ' '.join(part for part in [self.parameter, labels, properties] if part)

        return '(%s)' % content

    def __getitem__(self, index: int) -> str:
        return self.labels[index]


class Relation(object):
    def __init__(self, direction: str = None, parameter: str = None, types: List[str] = None,
                 properties: Properties = None):
        if direction == 'outgoing':
            self.direction = Direction.OUTGOING
        elif direction == 'incoming':
            self.direction = Direction.INCOMING
        else:
            self.direction = Direction.ANY
        self.parameter = parameter
        self.types = types if types else []
        self.properties = properties if properties else {}

    def __repr__(self) -> str:
        types = ':' + ':'.join(self.types) if self.types else None
        properties = json.dumps(self.properties, sort_keys=True) if self.properties else None
        content = ' '.join(part for part in [self.parameter, types, properties] if part)

        if self.direction == Direction.OUTGOING:
            return '-[%s]->' % content
        elif self.direction == Direction.INCOMING:
            return '<-[%s]-' % content
        else:
            return '-[%s]-' % content

    def __getitem__(self, index: int) -> str:
        return self.types[index]


class Chain(object):
    def __init__(self, node: dict, relation: dict):
        self.relation = Relation(**relation)
        self.node = Node(**node)

    def __repr__(self) -> str:
        return repr(self.relation) + repr(self.node)


class Pattern(object):
    def __init__(self, parameter: str = None, node: dict = None, chain: List[dict] = None):
        self.parameter = parameter
        self.node = Node(**node if node else {})
        self.chain = [Chain(**data) for data in chain] if chain else []

    def __repr__(self) -> str:
        content = repr(self.node) + ''.join(repr(data) for data in self.chain)
        if self.parameter:
            content = self.parameter + ' = ' + content

        return content

    def __getitem__(self, index: int) -> Chain:
        return self.chain[index]


class Match(object):
    def __init__(self, optional: bool = False, pattern: List[dict] = None):
        self.optional = optional
        self.pattern = [Pattern(**data) for data in pattern] if pattern else []

    def __repr__(self) -> str:
        content = 'MATCH ' + '\n'.join(repr(item) for item in self.pattern)
        if self.optional:
            content = 'OPTIONAL ' + content

        return content

    def __getitem__(self, index: int) -> Pattern:
        return self.pattern[index]


class Item(object):
    def __init__(self, function: str = None, parameter: str = None, property: str = None, value: 'Value' = None,
                 synonym: str = None):
        self.function = function
        self.parameter = parameter
        self.property = property
        self.value = value
        self.synonym = synonym

    def __repr__(self) -> str:
        if self.parameter:
            if self.property:
                selector = '%s.%s' % (self.parameter, self.property)
            else:
                selector = self.parameter
        else:
            selector = None
        data = json.dumps(self.value)

        if self.function is None:
            content = selector if selector else data
        elif self.function == '*':
            return '*'
        elif self.function == 'coalesce' and self.value:
            content = '%s(%s, %s)' % (self.function, selector, data)
        else:
            content = '%s(%s)' % (self.function, selector)

        if self.synonym:
            content += ' AS ' + self.synonym

        return content


class Order(object):
    def __init__(self, ascending: bool = True, parameter: str = None, property: str = None, synonym: str = None):
        self.ascending = ascending
        self.parameter = parameter
        self.property = property
        self.synonym = synonym

    def __repr__(self) -> str:
        if self.parameter:
            if self.property:
                content = '%s.%s' % (self.parameter, self.property)
            else:
                content = self.parameter
        else:
            content = self.synonym
        if not self.ascending:
            content += ' DESC'

        return content


class Ordering(object):
    def __init__(self, *orders: dict):
        self.items = [Order(**data) for data in orders] if orders else []

    def __repr__(self) -> str:
        return ', '.join(repr(item) for item in self.items)

    def __getitem__(self, index: int) -> Order:
        return self.items[index]


class Return(object):
    def __init__(self, distinct: bool = False, items: List[dict] = None, order: List[dict] = None,
                 skip: int = 0, limit: int = 0):
        self.distinct = distinct
        self.items = [Item(**data) for data in items] if items else []
        self.ordering = Ordering(*order if order else [])
        self.skip = skip
        self.limit = limit

    def __repr__(self) -> str:
        content = 'RETURN '
        if self.distinct:
            content += 'DISTINCT '
        content += ',\n\t'.join(repr(item) for item in self.items)
        if self.ordering.items:
            content += '\nORDER BY ' + ',\n\t'.join(repr(order) for order in self.ordering)
        if self.skip and self.skip > 0:
            content += '\nSKIP %d' % self.skip
        if self.limit and self.limit > 0:
            content += '\nLIMIT %d' % self.limit

        return content

    def __getitem__(self, index: int) -> Item:
        return self.items[index]

    def is_empty(self) -> bool:
        if self.items or self.ordering or self.skip and self.skip > 0 or self.limit:
            return False

        return True


class Rule(object):
    def __init__(self, description: str = None, salience: int = 0, match: List[dict] = None, result: dict = None):
        self.description = description
        self.salience = salience
        self.match = [Match(**data) for data in match] if match else []
        self.result = Return(**result if result else {})

    def __repr__(self) -> str:
        content = 'RULE'
        if self.description:
            content += ' ' + json.dumps(self.description)
        if self.salience and self.salience > 0:
            content += '\nSALIENCE %d' % self.salience
        for match in self.match:
            if match.pattern:
                content += '\n' + repr(match)
        if not self.result.is_empty():
            content += '\n' + repr(self.result)
        content += ';'

        return content


class RuleBase(object):
    def __init__(self, rules: dict):
        self.rules = [Rule(**data) for data in rules]

    def __repr__(self) -> str:
        return '\n\n'.join(repr(rule) for rule in self.rules)

    def __getitem__(self, index: int) -> Rule:
        return self.rules[index]


if __name__ == '__main__':
    content = {'value': [{'description': None,
                          'result': {'distinct': False,
                                     'items': [{'value': True, 'synonym': '_bool'}]}},
                         {'description': None,
                          'result': {'distinct': False,
                                     'items': [{'value': True, 'synonym': '_bool'}],
                                     'order': [{'ascending': True, 'synonym': '_bool'}],
                                     'skip': 5,
                                     'limit': 1}},
                         {'description': 'description',
                          'salience': 5,
                          'match': [{'optional': True,
                                     'pattern': [{'node': {'parameter': '$n',
                                                           'labels': ['main', 'person'],
                                                           'properties': {'text': 'Stefano'}},
                                                  'chain': [{'relation': {'direction': 'any',
                                                                          'types': ['knows']},
                                                             'node': {'parameter': '$f',
                                                                      'labels': ['person']}}]}]}],
                          'result': {'distinct': False,
                                     'items': [{'parameter': '$f',
                                                'property': 'text',
                                                'synonym': 'synonym'}],
                                     'order': [{'ascending': True, 'synonym': 'synonym'}],
                                     'skip': 1,
                                     'limit': 5}}]}

    rb = RuleBase(content['value'])
    print(rb)
