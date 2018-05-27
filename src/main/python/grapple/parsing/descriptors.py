import json
from typing import Dict, List

from grapple.tentative_engine.descriptors import Direction


class RulePart(object):
    def __init__(self, salience: int, description: str = None):
        self.description = description
        self.salience = salience

    def __repr__(self) -> str:
        if not self.description:
            content = 'RULE'
        else:
            content = 'RULE "%s"' % json.dumps(self.description)
        if self.salience > 0:
            content += '\nSALIENCE %d' % self.salience

        return content


class Node(object):
    def __init__(self, entity: str = None, labels: List[str] = None, properties: Dict = None):
        self.parameter = entity
        self.labels = labels if labels else []
        self.properties = properties if properties else {}

    def __repr__(self) -> str:
        types = ''.join(':%s' % repr(item) for item in self.labels)
        properties = json.dumps(self.properties) if self.properties else ''
        content = ' '.join(part for part in [self.parameter, types, properties] if part)

        return '(%s)' % content

    def __getitem__(self, index: int) -> str:
        return self.labels[index]


class Relation(object):
    def __init__(self, direction: str, entity: str = None, types: List[str] = None, properties: Dict = None):
        if direction == 'outgoing':
            self.direction = Direction.OUTGOING
        elif direction == 'incoming':
            self.direction = Direction.INCOMING
        else:
            self.direction = Direction.ANY
        self.parameter = entity
        self.types = types if types else []
        self.properties = properties if properties else {}

    def __repr__(self) -> str:
        types = ''.join(':%s' % repr(item) for item in self.types)
        properties = json.dumps(self.properties) if self.properties else ''
        content = ' '.join(part for part in [self.parameter, types, properties] if part)

        if self.direction == Direction.OUTGOING:
            return '-[%s]->' % content
        elif self.direction == Direction.INCOMING:
            return '<-[%s]-' % content
        else:
            return '-[%s]-' % content

    def __getitem__(self, index: int) -> str:
        return self.types[index]


class Step(object):
    def __init__(self, relation: Dict[str, object], node: Dict[str, object]):
        self.relation = Relation(**relation)
        self.node = Node(**node)

    def __repr__(self) -> str:
        return repr(self.relation) + repr(self.node)


class Pattern(object):
    def __init__(self, node: Dict[str, object], chain: List[Dict[str, object]] = None, parameter: str = None):
        self.parameter = parameter
        self.node = Node(**node)
        self.chain = [Step(**data) for data in chain] if chain else []

    def __repr__(self) -> str:
        content = repr(self.node) + ''.join(repr(item) for item in self.chain)
        if self.parameter:
            content = repr(self.parameter) + ' = ' + content

        return content

    def __getitem__(self, index: int) -> Step:
        return self.chain[index]


class MatchPart(object):
    def __init__(self, patterns: List[Dict[str, object]], optional: bool = False):
        self.optional = optional
        self.patterns = [Pattern(**data) for data in patterns]

    def __repr__(self) -> str:
        content = 'MATCH %s' % ',\n\t'.join(repr(item) for item in self.patterns)
        if self.optional:
            content = 'OPTIONAL ' + content

        return content


class CreatePart(object):
    def __init__(self, patterns: List[Dict[str, object]]):
        self.patterns = [Pattern(**data) for data in patterns]

    def __repr__(self) -> str:
        return 'CREATE ' + ',\n\t'.join(repr(item) for item in self.patterns)


class Removable(object):
    def __init__(self, entity: str, field: str = None, flags: List[str] = None):
        self.entity = entity
        self.field = field
        self.flags = flags if flags else []

    def __repr__(self) -> str:
        if self.field:
            if json.dumps(self.field) == '"%s"' % self.field:
                return self.entity + '.' + self.field

            else:
                return self.entity + '.' + json.dumps(self.field)

        else:
            return self.entity + ''.join(':%s' % repr(item) for item in self.flags)


class RemovePart(object):
    def __init__(self, items: List[Dict[str, object]]):
        self.items = [Removable(**data) for data in items] if items else []

    def __repr__(self) -> str:
        return 'REMOVE ' + ', '.join(repr(item) for item in self.items)


class Settable(object):
    def __init__(self, entity: str, field: str = None, flags: List[str] = None, operator: str = None,
                 parameter: str = None, properties: Dict[str, object] = None, value: object = None):
        self.entity = entity  #
        self.field = field  #
        self.flags = flags if flags else []  #
        self.operator = operator  #
        self.parameter = parameter
        self.properties = properties if properties else {}
        self.value = value

    def __repr__(self) -> str:
        content = repr(self.entity)
        if self.field:
            if json.dumps(self.field) == '"%s"' % self.field:
                content += '.' + self.field
            else:
                content += '.' + json.dumps(self.field)
        if self.flags:
            content += ''.join(':%s' % repr(item) for item in self.flags)

        if self.parameter:
            content += self.parameter
        elif self.value is not None:
            content += self.value
        else:
            content += json.dumps(self.properties)

        return content


class SetPart(object):
    def __init__(self, items: List[Dict[str, object]]):
        self.items = [Settable(**data) for data in items] if items else []

    def __repr__(self) -> str:
        return 'SET ' + ', '.join(repr(item) for item in self.items)


class Deletable(object):
    def __init__(self, entity: str):
        self.entity = entity

    def __repr__(self) -> str:
        return self.entity


class DeletePart(object):
    def __init__(self, items: List[Dict[str, str]], detach: bool = False):
        self.detach = detach
        self.items = [Deletable(**data) for data in items] if items else []

    def __repr__(self) -> str:
        if self.detach:
            return 'DETACH DELETE ' + ', '.join(repr(item) for item in self.entities)

        else:
            return 'DELETE ' + ', '.join(repr(item) for item in self.entities)


class Clause(object):
    def __init__(
            self,
            rule_part: Dict[str, object],
            match_part: List[Dict[str, object]] = None,
            update_part: List[Dict[str, object]] = None,
            return_part: Dict[str, object] = None,
    ):
        self.rule_part = RulePart(**rule_part)
        self.match_part = [MatchPart(**data) for data in match_part] if match_part else []
        self.update_part = []
        for data in update_part:
            if data.get('create_part', False):
                self.update_part.append(CreatePart(**data['create_part']))
            if data.get('remove_part', False):
                self.update_part.append(RemovePart(**data['remove_part']))
            if data.get('set_part', False):
                self.update_part.append(SetPart(**data['set_part']))
            if data.get('delete_part', False):
                self.update_part.append(DeletePart(**data['delete_part']))
        self.return_part = ReturnPart(**return_part) if return_part else None

    def __repr__(self) -> str:
        # TODO to be completed
        return '\n'.join(
            repr(self.rule_part),
            '\n'.join(repr(part) for part in self.match_part),
            '\n'.join(repr(part) for part in self.match_part),
        )


class RuleBase(object):
    def __init__(self, clauses: List[Dict[str, object]]):
        self.clauses = [Clause(**data) for data in clauses]

    def __repr__(self) -> str:
        return '\n\n'.join(repr(rule) for rule in self.clauses)
