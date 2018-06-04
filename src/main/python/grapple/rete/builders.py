import os
from typing import Set

from arpeggio import ParserPython, visit_parse_tree

from grapple.parsing.descriptors import RuleBase
from grapple.parsing.grammar import comment, cypher
from grapple.parsing.rete import Agenda, Alfa, IsNone, Leaf, Return, Root
from grapple.parsing.visitor import KnowledgeVisitor


class Session(object):
    def __init__(self, clauses: Set['Clause'], graph: 'Graph'):
        self.agenda = Agenda()
        self._graph = graph
        self._root = Root()

        if clauses:
            table = {}
            for clause in clauses:
                if not clause.match_part:
                    node = table.setdefault(None, Alfa(IsNone()).link(self._root))
                else:
                    continue
                # create_part
                # delete_part
                # remove_part
                # set_part
                for item in clause.return_part.items:
                    table.setdefault(item, Leaf(self.agenda, Return(item)).link(node))

    def close(self):
        self._graph.unregister(self)
        self._graph = None

    def insert(self, something):
        if not something:
            raise ValueError('This something is invalid')

        self._root.insert(something)

    def fire_all(self):
        if not self._graph:
            raise ValueError('This session is closed')

        self._root.insert(None)
        while not self.agenda.is_empty():
            activation = self.agenda.pop()
            activation.execute()


class KnowledgeBase(object):
    def __init__(self, clauses: Set['Clause']):
        if not clauses:
            raise ValueError('No clause given')

        self.clauses = clauses

    def get_session(self, graph: 'Graph') -> Session:
        if not self.clauses:
            raise ValueError('This knowledge base is empty')

        session = Session(self.clauses, graph)
        graph.register(session)

        return session


class Builder(object):
    def __init__(self):
        self.clauses = set()

    def load_from_base(self, base: 'RuleBase') -> 'Builder':
        for rule in base.clauses:
            self.clauses.add(rule)

        return self

    def load_from_str(self, content: str) -> 'Builder':
        parser = ParserPython(cypher, comment_def=comment)
        parsed = parser.parse(content)
        visited = visit_parse_tree(parsed, KnowledgeVisitor())
        base = RuleBase(visited['data'])
        self.load_from_base(base)

        return self

    def load_from_file(self, filename: str) -> 'Builder':
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                self.load_from_str(content)

        return self

    def build(self) -> KnowledgeBase:
        return KnowledgeBase(self.clauses)
