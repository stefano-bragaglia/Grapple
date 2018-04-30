import json
from enum import Enum
from typing import List, Union, Optional


class Direction(Enum):
    ANY = 0
    OUTGOING = 1
    INCOMING = 2


class Tags(object):
    def __init__(self, tags: List[str]):
        self._tags = list(set(tags))

    def __getitem__(self, given: Union[slice, tuple, int]) -> Union[str, List[str]]:
        if isinstance(given, slice):
            return [self._tags[ii] for ii in range(*given.indices(len(self._tags)))]

        elif isinstance(given, tuple):
            return [self._tags[ii] for ii in given if ii in self._tags]

        elif isinstance(given, int):
            if given < 0:
                given += len(self._tags)
            if given < 0 or given >= len(self._tags):
                raise IndexError("The index (%d) is out of range." % given)
            return self._tags[given]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self) -> str:
        return ''.join(':%s' % tag for tag in self._tags)


class Properties(object):
    def __init__(self, properties: dict = None):
        self._properties = properties

    def __repr__(self) -> str:
        if not self._properties:
            return ''

        return json.dumps(self._properties, sort_keys=True)

    @property
    def properties(self) -> Optional[dict]:
        return self._properties


class NodePattern(object):
    def __init__(self, variable: str = None, tags: List[str] = None, properties: dict = None):
        self._variable = variable
        self._tags = Tags(tags if tags else [])
        self._properties = Properties(properties)

    def __repr__(self) -> str:
        content = ' '.join(part for part in [self._variable, repr(self._tags), repr(self._properties)] if part)
        return '(%s)' % content

    @property
    def variable(self) -> Optional[str]:
        return self._variable

    @property
    def tags(self) -> Tags:
        return self._tags

    @property
    def properties(self) -> Properties:
        return self._properties


class RelationPattern(object):
    def __init__(self, direction: int = 0, variable: str = None, tags: List[str] = None, properties: dict = None):
        self._direction = Direction(direction)
        self._variable = variable
        self._tags = Tags(tags if tags else [])
        self._properties = Properties(properties)

    def __repr__(self) -> str:
        content = ' '.join(part for part in [self._variable, repr(self._tags), repr(self._properties)] if part)
        if content:
            content = '[%s]' % content

        if self._direction == Direction.ANY:
            return '-%s-' % content

        elif self._direction == Direction.OUTGOING:
            return '-%s->' % content

        elif self._direction == Direction.INCOMING:
            return '<-%s-' % content

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def variable(self) -> Optional[str]:
        return self._variable

    @property
    def tags(self) -> Tags:
        return self._tags

    @property
    def properties(self) -> Properties:
        return self._properties


class PatternNext(object):
    def __init__(self, relation_pattern: dict, node_pattern: dict):
        self._relation_pattern = RelationPattern(**relation_pattern)
        self._node_pattern = NodePattern(**node_pattern)

    def __repr__(self) -> str:
        return repr(self._relation_pattern) + repr(self._node_pattern)

    @property
    def relation_pattern(self) -> RelationPattern:
        return self._relation_pattern

    @property
    def node_pattern(self) -> NodePattern:
        return self._node_pattern


class PatternChain(object):
    def __init__(self, pattern_chains: List[dict]):
        self._pattern_chains = [PatternNext(**pattern_chain) for pattern_chain in pattern_chains]

    def __getitem__(self, given: Union[slice, tuple, int]) -> Union[PatternNext, List[PatternNext]]:
        if isinstance(given, slice):
            return [self._pattern_chains[ii] for ii in range(*given.indices(len(self._pattern_chains)))]

        elif isinstance(given, tuple):
            return [self._pattern_chains[ii] for ii in given if ii in self._pattern_chains]

        elif isinstance(given, int):
            if given < 0:
                given += len(self._pattern_chains)
            if given < 0 or given >= len(self._pattern_chains):
                raise IndexError("The index (%d) is out of range." % given)
            return self._pattern_chains[given]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self) -> str:
        if not self._pattern_chains:
            return ''

        return ''.join(repr(pattern_chain) for pattern_chain in self._pattern_chains)


class AnonymousPattern(object):
    def __init__(self, node_pattern: dict, pattern_chain: List[dict] = None):
        self._node_pattern = NodePattern(**node_pattern)
        self._pattern_chain = PatternChain(pattern_chain if pattern_chain else [])

    def __repr__(self) -> str:
        return repr(self._node_pattern) + repr(self._pattern_chain)

    @property
    def node_pattern(self) -> NodePattern:
        return self._node_pattern

    @property
    def pattern_chain(self) -> Optional[PatternChain]:
        return self._pattern_chain


class Pattern(object):
    def __init__(self, anonymous_pattern: dict, variable: str = None):
        self._variable = variable
        self._anonymous_pattern = AnonymousPattern(**anonymous_pattern)

    def __repr__(self) -> str:
        content = repr(self._anonymous_pattern)
        if self._variable:
            content = '%s = %s' % (self._variable, content)

        return content

    @property
    def variable(self) -> Optional[str]:
        return self._variable

    @property
    def anonymous_pattern(self) -> AnonymousPattern:
        return self._anonymous_pattern


class PatternList(object):
    def __init__(self, pattern_list: List[dict]):
        self._pattern_list = [Pattern(**pattern) for pattern in pattern_list]

    def __getitem__(self, given: Union[slice, tuple, int]) -> Union[Pattern, List[Pattern]]:
        if isinstance(given, slice):
            return [self._pattern_list[ii] for ii in range(*given.indices(len(self._pattern_list)))]

        elif isinstance(given, tuple):
            return [self._pattern_list[ii] for ii in given if ii in self._pattern_list]

        elif isinstance(given, int):
            if given < 0:
                given += len(self._pattern_list)
            if given < 0 or given >= len(self._pattern_list):
                raise IndexError("The index (%d) is out of range." % given)
            return self._pattern_list[given]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self) -> str:
        return ', '.join(repr(pattern) for pattern in self._pattern_list)


class MatchBody(object):
    def __init__(self, pattern_list: List[dict], optional: bool = False):
        self._optional = optional
        self._pattern_list = PatternList(pattern_list)

    def __repr__(self):
        content = "MATCH %s" % repr(self._pattern_list)
        if self._optional:
            content = 'OPTIONAL ' + content

        return content

    @property
    def optional(self) -> bool:
        return self._optional

    @property
    def pattern_list(self) -> PatternList:
        return self._pattern_list


if __name__ == '__main__':
    example = {
        'match': {
            'optional': True,
            'pattern_list': [{
                'variable': 'a',
                'anonymous_pattern': {
                    'node_pattern': {
                        'variable': 'b',
                        'tags': ['main', 'node'],
                        'properties': {
                            'key': 'value'
                        }
                    },
                    'pattern_chain': [{
                        'relation_pattern': {
                            'direction': 1,
                            'variable': 'c',
                            'tags': ['link'],
                            'properties': {
                                'key': 'value'
                            }
                        },
                        'node_pattern': {
                            'variable': 'd',
                            'tags': ['other'],
                            'properties': {
                                'key': 'value'
                            }
                        }
                    }],
                }
            }, {
                'variable': 'e',
                'anonymous_pattern': {
                    'node_pattern': {
                        'variable': 'f',
                        'tags': ['main', 'node'],
                        'properties': {
                            'key': 'value'
                        }
                    },
                    'pattern_chain': [{
                        'relation_pattern': {
                            'direction': 1,
                            'variable': 'g',
                            'tags': ['link'],
                            'properties': {
                                'key': 'value'
                            }
                        },
                        'node_pattern': {
                            'variable': 'h',
                            'tags': ['other'],
                            'properties': {
                                'key': 'value'
                            }
                        }
                    }],
                }
            }]
        }
    }
    body = MatchBody(**example['match'])
    print(body)
