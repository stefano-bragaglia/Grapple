import os
from typing import Set

from arpeggio import ParserPython, visit_parse_tree

from grapple.descriptors import RuleBase, CreatePart
from grapple.grammar import comment, cypher
from grapple.rete import Agenda, Alfa, Create, IsNone, Leaf, Payload, Return, Root
from grapple.visitor import KnowledgeVisitor


class Session(object):
    def __init__(self, clauses: Set['Clause'], graph: 'Graph'):
        self.agenda = Agenda()
        self._graph = graph
        self._root = Root()

        if clauses:
            table = {}
            for clause in clauses:
                # match_part
                if not clause.match_part:
                    node = table.setdefault(None, Alfa(IsNone()).link(self._root))
                else:
                    continue
                # update_part
                for part in clause.update_part:
                    # create_part
                    if type(part) is CreatePart:



                        for pattern in part.patterns:
                            table.setdefault(pattern, Leaf(self.agenda, Create(self._graph, pattern)).link(node))
                    # delete_part
                    # remove_part
                    # set_part
                # return_part
                for item in clause.return_part.items:
                    table.setdefault(item, Leaf(self.agenda, Return(item)).link(node))

    def close(self):
        self._graph.unregister(self)
        self._graph = None

    def insert(self, entity: 'Entity'):
        if not entity:
            raise ValueError('This entity is invalid')

        self._root.insert(entity, Payload.create(entity))

    def fire_all(self):
        if not self._graph:
            raise ValueError('This session is closed')

        self._root.insert(None, None)
        while not self.agenda.is_empty():
            activation = self.agenda.pop()
            activation.execute()


class KnowledgeBase(object):
    def __init__(self, clauses: Set['Clause']):
        if not clauses:
            raise ValueError('No clause given')

        self.clauses = clauses

    def get_session(self, graph: 'Graph') -> Session:
        if not graph:
            raise ValueError('This graph is invalid')

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
