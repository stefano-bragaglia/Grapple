from typing import List, Optional, Dict, Union

from grapple.bom.container import Value
from grapple.bom.entity import Entity
from grapple.bom.node import Node


class MatchNode(object):
    pass


class MatchRelation(object):
    pass


class MatchPattern(object):
    pass


class MatchBody(object):
    def __init__(self):
        pass


class ReturnItem(object):
    def __init__(
            self, function: str = None, variable: str = None, key: str = None, value: Value = None,
            literal: str = None):
        self._function = function
        self._variable = variable
        self._key = key
        self._value = value
        self._literal = literal

    @property
    def function(self) -> Optional[str]:
        return self._function

    @property
    def variable(self) -> Optional[str]:
        return self._variable

    @property
    def key(self) -> Optional[str]:
        return self._key

    @property
    def value(self) -> Optional[Value]:
        return self._value

    @property
    def literal(self) -> Optional[str]:
        return self._literal

    def resolve_content(self, payload: Dict[str, Entity]) -> Union[Value, Dict[str, Value]]:
        if not self._function:
            if self._variable:
                if self._variable not in payload:
                    raise ValueError("Variable '%s' not defined" % self._variable)

                if self._key:
                    return payload[self._variable].get_property(self._key)
                return payload[self._variable].get_properties()
            return self._value

        if self._variable not in payload:
            raise ValueError("Variable '%s' not defined" % self._variable)

        if self._function == 'id':
            return payload[self._variable].ident

        elif self._function == 'labels':
            if not isinstance(payload[self._variable], Node):
                raise ValueError("Type mismatch on '%s': expected Node but was Relation" % self._variable)
            return payload[self._variable].labels

        elif self._function == 'types':
            if not isinstance(payload[self._variable], Node):
                raise ValueError("Type mismatch on '%s': expected Relation but was node" % self._variable)
            return payload[self._variable].types

        elif self._function == 'keys':
            return payload[self._variable].keys

        elif self._function == 'keys':
            return payload[self._variable].keys

        elif self._function == 'properties':
            return payload[self._variable].get_properties()

        elif self._function == 'coalesce':
            return payload[self._variable].get_property(self._key, self._value)

        else:
            raise ValueError("Unknown function '%s'" % self._function)

    def resolve_name(self):
        if self._literal:
            return self._literal

        if not self._function:
            if self._variable:
                if self._key:
                    return '%s.%s' % (self._variable, self._key)
                return self._variable
            return str(self._value)

    def resolve(self, payload: Dict[str, Entity]) -> Dict[str, Union[Value, Dict[str, Value]]]:
        if self._function and self._function == '*':
            return {key: entity.get_properties() for key, entity in payload.items()}

        return {self.resolve_name(): self.resolve_content(payload)}


class ReturnBody(object):
    def __init__(self, return_items: List[ReturnItem], skip: int = 0, limit: int = None):
        self._return_items = return_items
        self._skip = skip
        self._limit = limit

    def __getitem__(self, index: int) -> ReturnItem:
        return self._return_items[index]

    @property
    def return_items(self) -> List[ReturnItem]:
        return self._return_items

    @property
    def skip(self) -> int:
        return self._skip

    @property
    def limit(self) -> Optional[int]:
        return self._limit

    def resolve(self, payload: Dict[str, Entity]) -> Dict[str, Union[Value, Dict[str, Value]]]:
        result = {}
        for return_item in self:
            result.update(return_item.resolve(payload))

        return result


class Rule(object):
    def __init__(self, description: str = None, salience: int = 0, match_body: dict = None, return_body: dict = None):
        self._description = description
        self._salience = salience
        self._match_body = MatchBody(**match_body)
        self._return_body = ReturnBody(**return_body)

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def salience(self) -> int:
        return self._salience

    @property
    def match_body(self) -> MatchBody:
        return self._match_body

    @property
    def return_body(self) -> ReturnBody:
        return self._return_body


class Base(object):
    def __init__(self, *rules: dict):
        self._rules = list({Rule(**rule) for rule in rules})

    @property
    def rules(self) -> List[Rule]:
        return self._rules

    def __getitem__(self, index: int) -> Rule:
        return self._rules[index]

    def add(self, rule: Rule) -> 'Base':
        if rule not in self._rules:
            self._rules.append(rule)

        return self

    def remove(self, rule: Rule) -> 'Base':
        if rule in self._rules:
            self._rules.remove(rule)

        return self
