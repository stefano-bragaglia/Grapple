from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.neat.grammar import identifier, parameter, key_as, key_asc, key_ascending, key_by, key_coalesce, key_desc, \
    key_descending, key_distinct, key_head, key_id, key_keys, key_labels, key_limit, key_match, key_optional, key_order, \
    key_properties, key_return, key_rule, key_salience, key_skip, key_tail, key_types
from grapple.neat.visitor import KnowledgeVisitor


class TestGrammarVisitor(TestCase):
    def test_identifier_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '~other~') \
            .starts_with('Expected identifier at position')

    def test_identifier_1(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '1Ab_') \
            .starts_with('Expected identifier at position')

    def test_identifier_2(self):
        assert_that(self.process(identifier, 'Ab_4')) \
            .contains_only('value') \
            .contains_entry({'value': 'Ab_4'})

    def test_identifier_3(self):
        assert_that(self.process(identifier, 'aB_4')) \
            .contains_only('value') \
            .contains_entry({'value': 'aB_4'})

    def test_identifier_4(self):
        assert_that(self.process(identifier, '_2Ab')) \
            .contains_only('value') \
            .contains_entry({'value': '_2Ab'})

    def test_parameter_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(parameter, '~other~') \
            .starts_with('Expected parameter at position')

    def test_parameter_1(self):
        assert_that(self.process(parameter, '$1Ab_')) \
            .contains_only('value') \
            .contains_entry({'value': '$1Ab_'})

    def test_parameter_2(self):
        assert_that(self.process(parameter, '$Ab_4')) \
            .contains_only('value') \
            .contains_entry({'value': '$Ab_4'})

    def test_parameter_3(self):
        assert_that(self.process(parameter, '$aB_4')) \
            .contains_only('value') \
            .contains_entry({'value': '$aB_4'})

    def test_parameter_4(self):
        assert_that(self.process(parameter, '$_2Ab')) \
            .contains_only('value') \
            .contains_entry({'value': '$_2Ab'})

    def test_key_as_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_as, '~other~') \
            .starts_with('Expected key_as at position')

    def test_key_as_1(self):
        assert_that(self.process(key_as, 'AS')) \
            .contains_only('value') \
            .contains_entry({'value': 'AS'})

    def test_key_as_2(self):
        assert_that(self.process(key_as, 'as')) \
            .contains_only('value') \
            .contains_entry({'value': 'AS'})

    def test_key_as_3(self):
        assert_that(self.process(key_as, ' as ')) \
            .contains_only('value') \
            .contains_entry({'value': 'AS'})

    def test_key_asc_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_asc, '~other~') \
            .starts_with('Expected key_asc at position')

    def test_key_asc_1(self):
        assert_that(self.process(key_asc, 'ASC')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASC'})

    def test_key_asc_2(self):
        assert_that(self.process(key_asc, 'asc')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASC'})

    def test_key_asc_3(self):
        assert_that(self.process(key_asc, ' asc ')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASC'})

    def test_key_ascending_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_ascending, '~other~') \
            .starts_with('Expected key_ascending at position')

    def test_key_ascending_1(self):
        assert_that(self.process(key_ascending, 'ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASCENDING'})

    def test_key_ascending_2(self):
        assert_that(self.process(key_ascending, 'ascending')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASCENDING'})

    def test_key_ascending_3(self):
        assert_that(self.process(key_ascending, ' ascending ')) \
            .contains_only('value') \
            .contains_entry({'value': 'ASCENDING'})

    def test_key_by_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_by, '~other~') \
            .starts_with('Expected key_by at position')

    def test_key_by_1(self):
        assert_that(self.process(key_by, 'BY')) \
            .contains_only('value') \
            .contains_entry({'value': 'BY'})

    def test_key_by_2(self):
        assert_that(self.process(key_by, 'by')) \
            .contains_only('value') \
            .contains_entry({'value': 'BY'})

    def test_key_by_3(self):
        assert_that(self.process(key_by, ' by ')) \
            .contains_only('value') \
            .contains_entry({'value': 'BY'})

    def test_key_coalesce_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_coalesce, '~other~') \
            .starts_with('Expected key_coalesce at position')

    def test_key_coalesce_1(self):
        assert_that(self.process(key_coalesce, 'COALESCE')) \
            .contains_only('value') \
            .contains_entry({'value': 'coalesce'})

    def test_key_coalesce_2(self):
        assert_that(self.process(key_coalesce, 'coalesce')) \
            .contains_only('value') \
            .contains_entry({'value': 'coalesce'})

    def test_key_coalesce_3(self):
        assert_that(self.process(key_coalesce, ' coalesce ')) \
            .contains_only('value') \
            .contains_entry({'value': 'coalesce'})

    def test_key_desc_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_desc, '~other~') \
            .starts_with('Expected key_desc at position')

    def test_key_desc_1(self):
        assert_that(self.process(key_desc, 'DESC')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESC'})

    def test_key_desc_2(self):
        assert_that(self.process(key_desc, 'desc')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESC'})

    def test_key_desc_3(self):
        assert_that(self.process(key_desc, ' desc ')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESC'})

    def test_key_descending_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_descending, '~other~') \
            .starts_with('Expected key_descending at position')

    def test_key_descending_1(self):
        assert_that(self.process(key_descending, 'DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESCENDING'})

    def test_key_descending_2(self):
        assert_that(self.process(key_descending, 'descending')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESCENDING'})

    def test_key_descending_3(self):
        assert_that(self.process(key_descending, ' descending ')) \
            .contains_only('value') \
            .contains_entry({'value': 'DESCENDING'})

    def test_key_distinct_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_distinct, '~other~') \
            .starts_with('Expected key_distinct at position')

    def test_key_distinct_1(self):
        assert_that(self.process(key_distinct, 'DISTINCT')) \
            .contains_only('value') \
            .contains_entry({'value': 'DISTINCT'})

    def test_key_distinct_2(self):
        assert_that(self.process(key_distinct, 'distinct')) \
            .contains_only('value') \
            .contains_entry({'value': 'DISTINCT'})

    def test_key_distinct_3(self):
        assert_that(self.process(key_distinct, ' distinct ')) \
            .contains_only('value') \
            .contains_entry({'value': 'DISTINCT'})

    def test_key_head_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_head, '~other~') \
            .starts_with('Expected key_head at position')

    def test_key_head_1(self):
        assert_that(self.process(key_head, 'HEAD')) \
            .contains_only('value') \
            .contains_entry({'value': 'head'})

    def test_key_head_2(self):
        assert_that(self.process(key_head, 'head')) \
            .contains_only('value') \
            .contains_entry({'value': 'head'})

    def test_key_head_3(self):
        assert_that(self.process(key_head, ' head ')) \
            .contains_only('value') \
            .contains_entry({'value': 'head'})

    def test_key_id_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_id, '~other~') \
            .starts_with('Expected key_id at position')

    def test_key_id_1(self):
        assert_that(self.process(key_id, 'ID')) \
            .contains_only('value') \
            .contains_entry({'value': 'id'})

    def test_key_id_2(self):
        assert_that(self.process(key_id, 'id')) \
            .contains_only('value') \
            .contains_entry({'value': 'id'})

    def test_key_id_3(self):
        assert_that(self.process(key_id, ' id ')) \
            .contains_only('value') \
            .contains_entry({'value': 'id'})

    def test_key_keys_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_keys, '~other~') \
            .starts_with('Expected key_keys at position')

    def test_key_keys_1(self):
        assert_that(self.process(key_keys, 'KEYS')) \
            .contains_only('value') \
            .contains_entry({'value': 'keys'})

    def test_key_keys_2(self):
        assert_that(self.process(key_keys, 'keys')) \
            .contains_only('value') \
            .contains_entry({'value': 'keys'})

    def test_key_keys_3(self):
        assert_that(self.process(key_keys, ' keys ')) \
            .contains_only('value') \
            .contains_entry({'value': 'keys'})

    def test_key_labels_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_labels, '~other~') \
            .starts_with('Expected key_labels at position')

    def test_key_labels_1(self):
        assert_that(self.process(key_labels, 'LABELS')) \
            .contains_only('value') \
            .contains_entry({'value': 'labels'})

    def test_key_labels_2(self):
        assert_that(self.process(key_labels, 'labels')) \
            .contains_only('value') \
            .contains_entry({'value': 'labels'})

    def test_key_labels_3(self):
        assert_that(self.process(key_labels, ' labels ')) \
            .contains_only('value') \
            .contains_entry({'value': 'labels'})

    def test_key_limit_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_limit, '~other~') \
            .starts_with('Expected key_limit at position')

    def test_key_limit_1(self):
        assert_that(self.process(key_limit, 'LIMIT')) \
            .contains_only('value') \
            .contains_entry({'value': 'LIMIT'})

    def test_key_limit_2(self):
        assert_that(self.process(key_limit, 'limit')) \
            .contains_only('value') \
            .contains_entry({'value': 'LIMIT'})

    def test_key_limit_3(self):
        assert_that(self.process(key_limit, ' liMIt ')) \
            .contains_only('value') \
            .contains_entry({'value': 'LIMIT'})

    def test_key_match_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_match, '~other~') \
            .starts_with('Expected key_match at position')

    def test_key_match_1(self):
        assert_that(self.process(key_match, 'match')) \
            .contains_only('value') \
            .contains_entry({'value': 'MATCH'})

    def test_key_match_2(self):
        assert_that(self.process(key_match, 'match')) \
            .contains_only('value') \
            .contains_entry({'value': 'MATCH'})

    def test_key_match_3(self):
        assert_that(self.process(key_match, ' match ')) \
            .contains_only('value') \
            .contains_entry({'value': 'MATCH'})

    def test_key_optional_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_optional, '~other~') \
            .starts_with('Expected key_optional at position')

    def test_key_optional_1(self):
        assert_that(self.process(key_optional, 'optional')) \
            .contains_only('value') \
            .contains_entry({'value': 'OPTIONAL'})

    def test_key_optional_2(self):
        assert_that(self.process(key_optional, 'optional')) \
            .contains_only('value') \
            .contains_entry({'value': 'OPTIONAL'})

    def test_key_optional_3(self):
        assert_that(self.process(key_optional, ' optional ')) \
            .contains_only('value') \
            .contains_entry({'value': 'OPTIONAL'})

    def test_key_order_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_order, '~other~') \
            .starts_with('Expected key_order at position')

    def test_key_order_1(self):
        assert_that(self.process(key_order, 'ORDER')) \
            .contains_only('value') \
            .contains_entry({'value': 'ORDER'})

    def test_key_order_2(self):
        assert_that(self.process(key_order, 'order')) \
            .contains_only('value') \
            .contains_entry({'value': 'ORDER'})

    def test_key_order_3(self):
        assert_that(self.process(key_order, ' order ')) \
            .contains_only('value') \
            .contains_entry({'value': 'ORDER'})

    def test_key_properties_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_properties, '~other~') \
            .starts_with('Expected key_properties at position')

    def test_key_properties_1(self):
        assert_that(self.process(key_properties, 'PROPERTIES')) \
            .contains_only('value') \
            .contains_entry({'value': 'properties'})

    def test_key_properties_2(self):
        assert_that(self.process(key_properties, 'properties')) \
            .contains_only('value') \
            .contains_entry({'value': 'properties'})

    def test_key_properties_3(self):
        assert_that(self.process(key_properties, ' properties ')) \
            .contains_only('value') \
            .contains_entry({'value': 'properties'})

    def test_key_return_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_return, '~other~') \
            .starts_with('Expected key_return at position')

    def test_key_return_1(self):
        assert_that(self.process(key_return, 'RETURN')) \
            .contains_only('value') \
            .contains_entry({'value': 'RETURN'})

    def test_key_return_2(self):
        result = self.process(key_return, 'return')

        assert_that(result).contains_only('value').contains_entry({'value': 'RETURN'})

    def test_key_return_3(self):
        assert_that(self.process(key_return, ' return ')) \
            .contains_only('value') \
            .contains_entry({'value': 'RETURN'})

    def test_key_rule_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_rule, '~other~') \
            .starts_with('Expected key_rule at position')

    def test_key_rule_1(self):
        assert_that(self.process(key_rule, 'RULE')) \
            .contains_only('value') \
            .contains_entry({'value': 'RULE'})

    def test_key_rule_2(self):
        result = self.process(key_rule, 'rule')

        assert_that(result).contains_only('value').contains_entry({'value': 'RULE'})

    def test_key_rule_3(self):
        assert_that(self.process(key_rule, ' rule ')) \
            .contains_only('value') \
            .contains_entry({'value': 'RULE'})

    def test_key_salience_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_salience, '~other~') \
            .starts_with('Expected key_salience at position')

    def test_key_salience_1(self):
        assert_that(self.process(key_salience, 'SALIENCE')) \
            .contains_only('value') \
            .contains_entry({'value': 'SALIENCE'})

    def test_key_salience_2(self):
        result = self.process(key_salience, 'salience')

        assert_that(result).contains_only('value').contains_entry({'value': 'SALIENCE'})

    def test_key_salience_3(self):
        assert_that(self.process(key_salience, ' salience ')) \
            .contains_only('value') \
            .contains_entry({'value': 'SALIENCE'})

    def test_key_skip_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_skip, '~other~') \
            .starts_with('Expected key_skip at position')

    def test_key_skip_1(self):
        assert_that(self.process(key_skip, 'SKIP')) \
            .contains_only('value') \
            .contains_entry({'value': 'SKIP'})

    def test_key_skip_2(self):
        result = self.process(key_skip, 'skip')

        assert_that(result) \
            .contains_only('value') \
            .contains_entry({'value': 'SKIP'})

    def test_key_skip_3(self):
        assert_that(self.process(key_skip, ' skip ')) \
            .contains_only('value') \
            .contains_entry({'value': 'SKIP'})

    def test_key_tail_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_tail, '~other~') \
            .starts_with('Expected key_tail at position')

    def test_key_tail_1(self):
        assert_that(self.process(key_tail, 'TAIL')) \
            .contains_only('value') \
            .contains_entry({'value': 'tail'})

    def test_key_tail_2(self):
        result = self.process(key_tail, 'tail')

        assert_that(result) \
            .contains_only('value') \
            .contains_entry({'value': 'tail'})

    def test_key_tail_3(self):
        assert_that(self.process(key_tail, ' tail ')) \
            .contains_only('value') \
            .contains_entry({'value': 'tail'})

    def test_key_types_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(key_types, '~other~') \
            .starts_with('Expected key_types at position')

    def test_key_types_1(self):
        assert_that(self.process(key_types, 'TYPES')) \
            .contains_only('value') \
            .contains_entry({'value': 'types'})

    def test_key_types_2(self):
        result = self.process(key_types, 'types')

        assert_that(result) \
            .contains_only('value') \
            .contains_entry({'value': 'types'})

    def test_key_types_3(self):
        assert_that(self.process(key_types, ' types ')) \
            .contains_only('value') \
            .contains_entry({'value': 'types'})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
