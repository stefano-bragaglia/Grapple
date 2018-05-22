import random
import sys
from unittest import TestCase

from arpeggio import ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import func_coalesce, func_head, func_id, func_keys, func_labels, func_length, func_nodes, \
    func_properties, func_relations, func_tail, func_types, json_false, json_integer, json_null, json_real, json_true, \
    key_as, key_asc, key_ascending, key_by, key_create, key_delete, key_desc, key_descending, key_detach, key_distinct, \
    key_limit, key_match, key_optional, key_order, key_remove, key_return, key_rule, key_salience, key_set, key_skip
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_func_coalesce(self):
        assert_that(self.process(func_coalesce, 'coalesce')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'coalesce'}})

    def test_func_head(self):
        assert_that(self.process(func_head, 'head')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'head'}})

    def test_func_id(self):
        assert_that(self.process(func_id, 'id')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'id'}})

    def test_func_keys(self):
        assert_that(self.process(func_keys, 'keys')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'keys'}})

    def test_func_labels(self):
        assert_that(self.process(func_labels, 'labels')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'labels'}})

    def test_func_length(self):
        assert_that(self.process(func_length, 'length')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'length'}})

    def test_func_nodes(self):
        assert_that(self.process(func_nodes, 'nodes')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'nodes'}})

    def test_func_relations(self):
        assert_that(self.process(func_relations, 'relations')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'relations'}})

    def test_func_properties(self):
        assert_that(self.process(func_properties, 'properties')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'properties'}})

    def test_func_tail(self):
        assert_that(self.process(func_tail, 'tail')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'tail'}})

    def test_func_types(self):
        assert_that(self.process(func_types, 'types')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'types'}})

    def test_key_as(self):
        assert_that(self.process(key_as, 'AS')) \
            .contains_only('data') \
            .contains_entry({'data': 'AS'})

    def test_key_asc(self):
        assert_that(self.process(key_asc, 'ASC')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASC'})

    def test_key_ascending(self):
        assert_that(self.process(key_ascending, 'ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASCENDING'})

    def test_key_by(self):
        assert_that(self.process(key_by, 'BY')) \
            .contains_only('data') \
            .contains_entry({'data': 'BY'})

    def test_key_create(self):
        assert_that(self.process(key_create, 'CREATE')) \
            .contains_only('data') \
            .contains_entry({'data': 'CREATE'})

    def test_key_delete(self):
        assert_that(self.process(key_delete, 'DELETE')) \
            .contains_only('data') \
            .contains_entry({'data': 'DELETE'})

    def test_key_detach(self):
        assert_that(self.process(key_detach, 'DETACH')) \
            .contains_only('data') \
            .contains_entry({'data': 'DETACH'})

    def test_key_desc(self):
        assert_that(self.process(key_desc, 'DESC')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESC'})

    def test_key_descending(self):
        assert_that(self.process(key_descending, 'DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESCENDING'})

    def test_key_distinct(self):
        assert_that(self.process(key_distinct, 'DISTINCT')) \
            .contains_only('data') \
            .contains_entry({'data': 'DISTINCT'})

    def test_key_limit(self):
        assert_that(self.process(key_limit, 'LIMIT')) \
            .contains_only('data') \
            .contains_entry({'data': 'LIMIT'})

    def test_key_match(self):
        assert_that(self.process(key_match, 'MATCH')) \
            .contains_only('data') \
            .contains_entry({'data': 'MATCH'})

    def test_key_optional(self):
        assert_that(self.process(key_optional, 'OPTIONAL')) \
            .contains_only('data') \
            .contains_entry({'data': 'OPTIONAL'})

    def test_key_order(self):
        assert_that(self.process(key_order, 'ORDER')) \
            .contains_only('data') \
            .contains_entry({'data': 'ORDER'})

    def test_key_remove(self):
        assert_that(self.process(key_remove, 'REMOVE')) \
            .contains_only('data') \
            .contains_entry({'data': 'REMOVE'})

    def test_key_return(self):
        assert_that(self.process(key_return, 'RETURN')) \
            .contains_only('data') \
            .contains_entry({'data': 'RETURN'})

    def test_key_rule(self):
        assert_that(self.process(key_rule, 'RULE')) \
            .contains_only('data') \
            .contains_entry({'data': 'RULE'})

    def test_key_salience(self):
        assert_that(self.process(key_salience, 'SALIENCE')) \
            .contains_only('data') \
            .contains_entry({'data': 'SALIENCE'})

    def test_key_set(self):
        assert_that(self.process(key_set, 'SET')) \
            .contains_only('data') \
            .contains_entry({'data': 'SET'})

    def test_key_skip(self):
        assert_that(self.process(key_skip, 'SKIP')) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
