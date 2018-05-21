import os
from typing import Set

from arpeggio import ParserPython, visit_parse_tree

from grapple.parsing.descriptors import Rule, RuleBase
from grapple.parsing.grammar import comment, cypher
from grapple.parsing.visitor import KnowledgeVisitor


class Session(object):

    def insert(self):
        pass

    def fire_all(self):


class Base(object):
    def __init__(self, rules: Set[Rule]):
        pass

    def get_session(self, graph: 'Graph') -> Session:
        return None


class Builder(object):

    def __init__(self):
        self._rules = set()

    def load_from_base(self, base: 'RuleBase') -> 'Builder':
        for rule in base:
            self._rules.add(rule)

        return self

    def load_from_str(self, content: str) -> 'Builder':
        parser = ParserPython(cypher, comment_def=comment)
        parsed = parser.parse(content)
        visited = visit_parse_tree(parsed, KnowledgeVisitor())
        base = RuleBase(visited['value'])
        self.load_from_base(base)

        return self

    def load_from_file(self, filename: str) -> 'Builder':
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                self.load_from_str(content)

        return self

    def build(self) -> Base:
        return Base(self._rules)
