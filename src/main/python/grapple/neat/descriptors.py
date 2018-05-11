import json
from typing import List, Optional

from grapple.bom.container import Value


class Item(object):
    def __init__(self, function: str = None, parameter: str = None, property: str = None, value: 'Value' = None,
                 as_: str = None):
        self._func = function
        self._param = parameter
        self._prop = property
        self._value = value
        self._name = as_

    def __repr__(self) -> str:
        if self._param:
            if self._prop:
                selector = '%s.%s' % (self._param, self._prop)
            else:
                selector = self._param
        else:
            selector = None
        data = json.dumps(self._value)

        if self._func is None:
            content = selector if selector else data
        elif self._func == '*':
            return '*'
        elif self._func == 'coalesce' and self._value:
            content = '%s(%s, %s)' % (self._func, selector, data)
        else:
            content = '%s(%s)' % (self._func, selector)

        if self._name:
            content += ' AS ' + self._name

        return content

    @property
    def func(self) -> Optional[str]:
        return self._func

    @property
    def param(self) -> Optional[str]:
        return self._param

    @property
    def prop(self) -> Optional[str]:
        return self._prop

    @property
    def value(self) -> Optional['Value']:
        return self._value

    @property
    def name(self) -> Optional[str]:
        return self._name


class Order(object):
    def __init__(self, ascending: bool = True, parameter: str = None, property: str = None, name: str = None):
        self._ascending = ascending
        self._param = parameter
        self._prop = property
        self._name = name

    def __repr__(self) -> str:
        if self._param:
            if self._prop:
                content = '%s.%s' % (self._param, self._prop)
            else:
                content = self._param
        else:
            content = self._name
        if not self._ascending:
            content += ' DESC'

        return content

    @property
    def ascending(self) -> bool:
        return self._ascending

    @property
    def param(self) -> Optional[str]:
        return self._param

    @property
    def prop(self) -> Optional[str]:
        return self._prop

    @property
    def name(self) -> Optional[str]:
        return self._name


class Ordering(object):
    def __init__(self, *orders: dict):
        self._orders = [Order(**data) for data in orders] if orders else []

    def __repr__(self) -> str:
        return ', '.join(repr(order) for order in self._orders)

    def __getitem__(self, index: int) -> Order:
        return self._orders[index]

    def is_empty(self) -> bool:
        return not self._orders

    @property
    def orders(self) -> List[Order]:
        return self._orders


class Return(object):
    def __init__(self, distinct: bool = False, items: List[dict] = None, order: List[dict] = None,
                 skip: int = 0, limit: int = 0):
        self._distinct = distinct
        self._items = [Item(**data) for data in items] if items else []
        self._ordering = Ordering(*order if order else [])
        self._skip = skip
        self._limit = limit

    def __repr__(self) -> str:
        content = 'RETURN '
        if self._distinct:
            content += 'DISTINCT '
        content += ',\n\t'.join(repr(item) for item in self._items)
        if not self._ordering.is_empty():
            content += '\nORDER BY ' + ',\n\t'.join(repr(order) for order in self._ordering)
        if self._skip and self._skip > 0:
            content += '\nSKIP %d' % self._skip
        if self._limit and self._limit > 0:
            content += '\nLIMIT %d' % self._limit

        return content

    def __getitem__(self, index: int) -> Item:
        return self._items[index]

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def items(self) -> List[Item]:
        return self._items

    @property
    def ordering(self) -> Ordering:
        return self._ordering

    @property
    def skip(self) -> int:
        return self._skip

    @property
    def limit(self) -> int:
        return self._limit

    def is_empty(self) -> bool:
        if self._items or not self._ordering.is_empty() or self._skip and self._skip > 0 or self._limit:
            return False

        return True


class Rule(object):
    def __init__(self, description: str = None, salience: int = 0, match: dict = None, return_: dict = None):
        self._desc = description
        self._salience = salience
        # match
        self._return = Return(**return_ if return_ else {})

    def __repr__(self) -> str:
        content = 'RULE'
        if self._desc:
            content += ' ' + json.dumps(self._desc)
        if self._salience and self._salience > 0:
            content += '\nSALIENCE %d' % self._salience
        if not self._return.is_empty():
            content += '\n' + repr(self._return)

        return content

    @property
    def desc(self) -> Optional[str]:
        return self._desc

    @property
    def salience(self) -> int:
        return self._salience

    @property
    def return_(self) -> Optional[Return]:
        return self._return


class RuleBase(object):
    def __init__(self, *rules: dict):
        self._rules = [Rule(**data) for data in rules]

    def __repr__(self) -> str:
        return '\n\n'.join(repr(rule) for rule in self._rules)

    def __getitem__(self, index: int) -> Rule:
        return self._rules[index]

    @property
    def rules(self) -> List[Rule]:
        return self._rules


if __name__ == '__main__':
    result = {'value': [{'description': None,
                         'return_': {'distinct': False,
                                     'items': [{'value': True, 'as_': '_bool'}]}},
                        {'description': None,
                         'return_': {'distinct': False,
                                     'items': [{'value': True, 'as_': '_bool'}],
                                     'order': [{'ascending': True, 'name': '_bool'}],
                                     'skip': 5,
                                     'limit': 1}},
                        {'description': 'description',
                         'salience': 5,
                         'match': [{'optional': True,
                                    'pattern': [{'start': {'node': {'parameter': '$n',
                                                                    'labels': ['main', 'person'],
                                                                    'properties': {'text': 'Stefano'}}},
                                                 'chain': [{'relation': {'direction': 'any',
                                                                         'types': ['knows']},
                                                            'node': {'parameter': '$f',
                                                                     'labels': ['person']}}]}]}],
                         'return_': {'distinct': False,
                                     'items': [{'parameter': '$f',
                                                'property': 'text',
                                                'as_': 'name'}],
                                     'order': [{'ascending': True, 'name': 'name'}],
                                     'skip': 1,
                                     'limit': 5}}]}

    rb = RuleBase(*result['value'])
    print(rb)
