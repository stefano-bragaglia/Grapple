from typing import List, Optional, Union


class OrderItem(object):
    def __init__(self, entity: str = None, key: str = None, synonym: str = None, ascending: bool = True):
        if not entity and not synonym:
            raise ValueError("entity or synonym required")
        # if not entity and key or key and synonym or entity and synonym:
        #     raise ValueError("inconsistent state")

        self._entity = entity
        self._key = key
        self._synonym = synonym
        self._ascending = ascending

    def __repr__(self) -> str:
        if self._synonym:
            content = self._synonym
        elif self._key:
            content = "%s.%s" % (self._entity, self._key)
        else:
            content = self._entity

        if not self._ascending:
            content += ' DESC'

        return content

    @property
    def entity(self) -> Optional[str]:
        return self._entity

    @property
    def key(self) -> Optional[str]:
        return self._key

    @property
    def synonym(self) -> Optional[str]:
        return self._synonym

    @property
    def ascending(self) -> bool:
        return self._ascending


class OrderItems(object):
    def __init__(self, order_by: List[dict]):
        self._order_items = [OrderItem(**item) for item in order_by]

    def __getitem__(self, given: Union[slice, tuple, int]) -> Union[OrderItem, List[OrderItem]]:
        if isinstance(given, slice):
            return [self._order_items[ii] for ii in range(*given.indices(len(self._order_items)))]

        elif isinstance(given, tuple):
            return [self._order_items[ii] for ii in given if ii in self._order_items]

        elif isinstance(given, int):
            if given < 0:
                given += len(self._order_items)
            if given < 0 or given >= len(self._order_items):
                raise IndexError("The index (%d) is out of range." % given)
            return self._order_items[given]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self) -> str:
        if not self._order_items:
            return ''

        return 'ORDER BY %s' % ', '.join(str(item) for item in self._order_items)


Value = object


class ReturnItem(object):
    def __init__(self,
                 function: str = None, entity: str = None, key: str = None, value: Value = None, synonym: str = None):
        if not function:
            if not entity and not value:
                raise ValueError("entity or value required")
        elif function == 'coalesce':
            if not entity or not key:
                raise ValueError("entity and key required")
        else:
            if function != '*' and not entity:
                raise ValueError("entity required")

        self._function = function
        self._entity = entity
        self._key = key
        self._value = value
        self._synonym = synonym

    def __repr__(self) -> str:
        if not self._function:
            if self._value:
                content = str(self._value)
            elif self._key:
                content = "%s.%s" % (self._entity, self._key)
            else:
                content = self._entity
        elif self._function == '*':
            content = '*'
        elif self._function == 'coalesce':
            content = "coalesce(%s.%s, %s)" % (self._entity, self._key, str(self.value))
        else:
            content = "%s(%s)" % (self._function, self._entity)

        if (not self._function or self._function != '*') and self._synonym:
            content += ' AS %s' % self._synonym

        return content

    @property
    def function(self) -> Optional[str]:
        return self._function

    @property
    def entity(self) -> Optional[str]:
        return self._entity

    @property
    def key(self) -> Optional[str]:
        return self._key

    @property
    def value(self) -> Optional[Value]:
        return self._value

    @property
    def synonym(self) -> Optional[str]:
        return self._synonym


class ReturnItems(object):
    def __init__(self, items: List[dict]):
        self._return_items = [ReturnItem(**item) for item in items]

    def __getitem__(self, given: Union[slice, tuple, int]) -> Union[ReturnItem, List[ReturnItem]]:
        if isinstance(given, slice):
            return [self._return_items[ii] for ii in range(*given.indices(len(self._return_items)))]

        elif isinstance(given, tuple):
            return [self._return_items[ii] for ii in given if ii in self._return_items]

        elif isinstance(given, int):
            if given < 0:
                given += len(self._return_items)
            if given < 0 or given >= len(self._return_items):
                raise IndexError("The index (%d) is out of range." % given)
            return self._return_items[given]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self) -> str:
        if not self._return_items:
            return ''

        return ', '.join(str(item) for item in self._return_items)


class ReturnBody(object):
    def __init__(self, distinct: bool = False, items: List[dict] = None, order_by: List[dict] = None,
                 skip: int = 0, limit: int = -1):
        self._distinct = distinct
        self._return_items = ReturnItems(items if items else [])
        self._order_items = OrderItems(order_by if order_by else [])
        self._skip = skip
        self._limit = limit

    def __repr__(self) -> str:
        content = str(self._return_items)
        if self._distinct:
            content = 'DISTINCT ' + content
        content += ' %s' % str(self._order_items)
        if self._skip > 0:
            content += ' SKIP %d' % self._skip
        if self._limit > 0:
            content += ' LIMIT %d' % self._limit

        return 'RETURN %s' % content

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def return_items(self) -> ReturnItems:
        return self._return_items

    @property
    def order_items(self) -> OrderItems:
        return self._order_items

    @property
    def skip(self) -> int:
        return self._skip

    @property
    def limit(self) -> int:
        return self._limit


if __name__ == '__main__':
    example = {
        'return': {
            'distinct': True,
            'items': [
                {'function': '*', 'synonym': 'a_01'},
                {'function': 'id', 'entity': '$a', 'synonym': 's_02'},
                {'function': 'keys', 'entity': '$a', 'synonym': 's_03'},
                {'function': 'properties', 'entity': '$a', 'synonym': 's_04'},
                {'function': 'labels', 'entity': '$a', 'synonym': 's_05'},
                {'function': 'types', 'entity': '$a', 'synonym': 's_06'},
                {'function': 'tail', 'entity': '$a', 'synonym': 's_07'},
                {'function': 'head', 'entity': '$a', 'synonym': 's_08'},
            ],
            'order_by': [
                {'entity': '$a'},
                {'entity': '$a', 'key': 'key'},
                {'synonym': 'name'},
                {'entity': '$b', 'ascending': False},
                {'entity': '$b', 'key': 'key', 'ascending': False},
                {'synonym': 'surname', 'ascending': False}
            ],
            'skip': 5,
            'limit': 10
        }
    }
    body = ReturnBody(**example['return'])
    print(body)
