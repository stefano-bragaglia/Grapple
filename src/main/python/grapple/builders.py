import os
from typing import Set

from arpeggio import ParserPython, visit_parse_tree

from grapple.descriptors import RuleBase, CreatePart
from grapple.grammar import comment, cypher
from grapple.rete import Agenda, Alfa, Create, IsNone, Leaf, Payload, Return, Root, HasLabel
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
                    condition = IsNone()
                    if condition.signature not in table:
                        table[condition.signature] = Alfa(condition, self._root)
                    node = table[condition.signature]
                else:
                    continue
                # update_part
                for part in clause.update_part:
                    # create_part
                    node = self._root
                    if type(part) is CreatePart:
                        # for label in part.node.labels:
                        #     condition = HasLabel(label)
                        #     if condition.signature not in table:
                        #         table[condition.signature] = Alfa(condition).link(node)
                        #     # Still neda a Beta
                        for pattern in part.patterns:
                            table.setdefault(pattern, Leaf(Create(self._graph, pattern), self.agenda, node))
                    # delete_part
                    # remove_part
                    # set_part
                # return_part
                for item in clause.return_part.items:
                    table.setdefault(item, Leaf(Return(item), self.agenda, node))

    def close(self):
        self._graph.unregister(self)
        self._graph = None

    def insert(self, entity: 'Entity'):
        if not entity:
            raise ValueError('This entity is invalid')

        self._root.notify(Payload.create(entity), None)

    def fire_all(self):
        if not self._graph:
            raise ValueError('This session is closed')

        self._root.notify(None, None)
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
