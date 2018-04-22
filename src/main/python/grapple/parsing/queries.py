from typing import List

from arpeggio import visit_parse_tree

from graphx.grammar import parser
from graphx.visitors import QueryVisitor


class Query(object):

    def __init__(self, statement: str):
        parse_tree = parser.parse(statement)
        descriptor = visit_parse_tree(parse_tree, QueryVisitor())
        self._pattern = descriptor['pattern']
        self._requests = descriptor['requests']

    @property
    def pattern(self) -> dict:
        return self._pattern

    @property
    def requests(self) -> dict:
        return self._requests

    def execute(self, graph: 'GraphX') -> List['Record']:
        records = []
        if self._pattern:
            for match in self._match(graph):
                record = self._extract(match)
                if record and record not in records:
                    records.append(record)

        return records

    def _match(self, graph: 'GraphX') -> List['Match']:
        matches = []
        n = self._pattern[0]
        for node in graph.find_nodes(*n['labels'], props=n['properties']):
            table = {}
            if n['name']:
                table[n['name']] = node

            for result in self._match_next(node, 1, table):
                matches.append(result)

        return matches

    def _match_next(self, node: 'NodeX', index: int, table: 'Match') -> List['Match']:
        if index >= len(self._pattern):
            return [table]

        matches = []
        r, n = self._pattern[index], self._pattern[index + 1]
        for relation in node.find_relations(*r['types'], dir=r['direction'], props=r['properties']):
            current = dict(table)
            if r['name']:
                current[r['name']] = relation

            other = relation.get_other(node)
            if other.match(*n['labels'], props=n['properties'] if 'properties' else {}):
                if n['name']:
                    current[n['name']] = other

                for result in self._match_next(other, index + 2, current):
                    matches.append(result)

        return matches

    def _extract(self, match: 'Match') -> 'Record':
        record = {}

        for request in self._requests:
            var = request['variable']
            if var not in match:
                raise ValueError("'%s' not returned by current pattern" % var)

            entity = match[var]
            if 'field' in request:
                data = entity.get_property(request['field'])
            else:
                data = entity.get_properties()

            if 'name' in request:
                name = request['name']
            else:
                name = var
                if 'field' in request:
                    name += '.' + request['field']

            record[name] = data

        return record
