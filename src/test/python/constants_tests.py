from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.grammar import func_coalesce, func_head, func_id, func_keys, func_labels, func_properties, \
    func_tail, func_types, identifier, key_as, key_asc, key_ascending, key_by, key_desc, key_descending, key_distinct, \
    key_limit, key_match, key_optional, key_order, key_return, key_rule, key_salience, key_skip, parameter
from grapple.visitor import KnowledgeVisitor


class TestConstantParsing(TestCase):
    def test_identifier_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '~other~') \
            .starts_with('Expected identifier at position')

    def test_identifier_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(identifier, '1Ab_') \
            .starts_with('Expected identifier at position')

    def test_identifier_2(self):
        assert_that(self.process(identifier, 'Ab_4')) \
            .contains_only('data') \
            .contains_entry({'data': 'Ab_4'})

    def test_identifier_3(self):
        assert_that(self.process(identifier, 'aB_4')) \
            .contains_only('data') \
            .contains_entry({'data': 'aB_4'})

    def test_identifier_4(self):
        assert_that(self.process(identifier, '_2Ab')) \
            .contains_only('data') \
            .contains_entry({'data': '_2Ab'})

    def test_parameter_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(parameter, '~other~') \
            .starts_with('Expected parameter at position')

    def test_parameter_1(self):
        assert_that(self.process(parameter, '$1Ab_')) \
            .contains_only('data') \
            .contains_entry({'data': {'parameter': '$1Ab_'}})

    def test_parameter_2(self):
        assert_that(self.process(parameter, '$Ab_4')) \
            .contains_only('data') \
            .contains_entry({'data': {'parameter': '$Ab_4'}})

    def test_parameter_3(self):
        assert_that(self.process(parameter, '$aB_4')) \
            .contains_only('data') \
            .contains_entry({'data': {'parameter': '$aB_4'}})

    def test_parameter_4(self):
        assert_that(self.process(parameter, '$_2Ab')) \
            .contains_only('data') \
            .contains_entry({'data': {'parameter': '$_2Ab'}})

    def test_key_as_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_as, '~other~') \
            .starts_with('Expected key_as at position')

    def test_key_as_1(self):
        assert_that(self.process(key_as, 'AS')) \
            .contains_only('data') \
            .contains_entry({'data': 'AS'})

    def test_key_as_2(self):
        assert_that(self.process(key_as, 'as')) \
            .contains_only('data') \
            .contains_entry({'data': 'AS'})

    def test_key_as_3(self):
        assert_that(self.process(key_as, ' as ')) \
            .contains_only('data') \
            .contains_entry({'data': 'AS'})

    def test_key_asc_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_asc, '~other~') \
            .starts_with('Expected key_asc at position')

    def test_key_asc_1(self):
        assert_that(self.process(key_asc, 'ASC')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASC'})

    def test_key_asc_2(self):
        assert_that(self.process(key_asc, 'asc')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASC'})

    def test_key_asc_3(self):
        assert_that(self.process(key_asc, ' asc ')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASC'})

    def test_key_ascending_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_ascending, '~other~') \
            .starts_with('Expected key_ascending at position')

    def test_key_ascending_1(self):
        assert_that(self.process(key_ascending, 'ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASCENDING'})

    def test_key_ascending_2(self):
        assert_that(self.process(key_ascending, 'ascending')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASCENDING'})

    def test_key_ascending_3(self):
        assert_that(self.process(key_ascending, ' ascending ')) \
            .contains_only('data') \
            .contains_entry({'data': 'ASCENDING'})

    def test_key_by_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_by, '~other~') \
            .starts_with('Expected key_by at position')

    def test_key_by_1(self):
        assert_that(self.process(key_by, 'BY')) \
            .contains_only('data') \
            .contains_entry({'data': 'BY'})

    def test_key_by_2(self):
        assert_that(self.process(key_by, 'by')) \
            .contains_only('data') \
            .contains_entry({'data': 'BY'})

    def test_key_by_3(self):
        assert_that(self.process(key_by, ' by ')) \
            .contains_only('data') \
            .contains_entry({'data': 'BY'})

    def test_func_coalesce_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_coalesce, '~other~') \
            .starts_with('Expected func_coalesce at position')

    def test_func_coalesce_1(self):
        assert_that(self.process(func_coalesce, 'COALESCE')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'coalesce'}})

    def test_func_coalesce_2(self):
        assert_that(self.process(func_coalesce, 'coalesce')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'coalesce'}})

    def test_func_coalesce_3(self):
        assert_that(self.process(func_coalesce, ' coalesce ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'coalesce'}})

    def test_key_desc_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_desc, '~other~') \
            .starts_with('Expected key_desc at position')

    def test_key_desc_1(self):
        assert_that(self.process(key_desc, 'DESC')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESC'})

    def test_key_desc_2(self):
        assert_that(self.process(key_desc, 'desc')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESC'})

    def test_key_desc_3(self):
        assert_that(self.process(key_desc, ' desc ')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESC'})

    def test_key_descending_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_descending, '~other~') \
            .starts_with('Expected key_descending at position')

    def test_key_descending_1(self):
        assert_that(self.process(key_descending, 'DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESCENDING'})

    def test_key_descending_2(self):
        assert_that(self.process(key_descending, 'descending')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESCENDING'})

    def test_key_descending_3(self):
        assert_that(self.process(key_descending, ' descending ')) \
            .contains_only('data') \
            .contains_entry({'data': 'DESCENDING'})

    def test_key_distinct_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_distinct, '~other~') \
            .starts_with('Expected key_distinct at position')

    def test_key_distinct_1(self):
        assert_that(self.process(key_distinct, 'DISTINCT')) \
            .contains_only('data') \
            .contains_entry({'data': 'DISTINCT'})

    def test_key_distinct_2(self):
        assert_that(self.process(key_distinct, 'distinct')) \
            .contains_only('data') \
            .contains_entry({'data': 'DISTINCT'})

    def test_key_distinct_3(self):
        assert_that(self.process(key_distinct, ' distinct ')) \
            .contains_only('data') \
            .contains_entry({'data': 'DISTINCT'})

    def test_func_head_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_head, '~other~') \
            .starts_with('Expected func_head at position')

    def test_func_head_1(self):
        assert_that(self.process(func_head, 'HEAD')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'head'}})

    def test_func_head_2(self):
        assert_that(self.process(func_head, 'head')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'head'}})

    def test_func_head_3(self):
        assert_that(self.process(func_head, ' head ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'head'}})

    def test_func_id_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_id, '~other~') \
            .starts_with('Expected func_id at position')

    def test_func_id_1(self):
        assert_that(self.process(func_id, 'ID')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'id'}})

    def test_func_id_2(self):
        assert_that(self.process(func_id, 'id')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'id'}})

    def test_func_id_3(self):
        assert_that(self.process(func_id, ' id ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'id'}})

    def test_func_keys_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_keys, '~other~') \
            .starts_with('Expected func_keys at position')

    def test_func_keys_1(self):
        assert_that(self.process(func_keys, 'KEYS')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'keys'}})

    def test_func_keys_2(self):
        assert_that(self.process(func_keys, 'keys')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'keys'}})

    def test_func_keys_3(self):
        assert_that(self.process(func_keys, ' keys ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'keys'}})

    def test_func_labels_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_labels, '~other~') \
            .starts_with('Expected func_labels at position')

    def test_func_labels_1(self):
        assert_that(self.process(func_labels, 'LABELS')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'labels'}})

    def test_func_labels_2(self):
        assert_that(self.process(func_labels, 'labels')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'labels'}})

    def test_func_labels_3(self):
        assert_that(self.process(func_labels, ' labels ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'labels'}})

    def test_key_limit_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_limit, '~other~') \
            .starts_with('Expected key_limit at position')

    def test_key_limit_1(self):
        assert_that(self.process(key_limit, 'LIMIT')) \
            .contains_only('data') \
            .contains_entry({'data': 'LIMIT'})

    def test_key_limit_2(self):
        assert_that(self.process(key_limit, 'limit')) \
            .contains_only('data') \
            .contains_entry({'data': 'LIMIT'})

    def test_key_limit_3(self):
        assert_that(self.process(key_limit, ' liMIt ')) \
            .contains_only('data') \
            .contains_entry({'data': 'LIMIT'})

    def test_key_match_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_match, '~other~') \
            .starts_with('Expected key_match at position')

    def test_key_match_1(self):
        assert_that(self.process(key_match, 'match')) \
            .contains_only('data') \
            .contains_entry({'data': 'MATCH'})

    def test_key_match_2(self):
        assert_that(self.process(key_match, 'match')) \
            .contains_only('data') \
            .contains_entry({'data': 'MATCH'})

    def test_key_match_3(self):
        assert_that(self.process(key_match, ' match ')) \
            .contains_only('data') \
            .contains_entry({'data': 'MATCH'})

    def test_key_optional_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_optional, '~other~') \
            .starts_with('Expected key_optional at position')

    def test_key_optional_1(self):
        assert_that(self.process(key_optional, 'optional')) \
            .contains_only('data') \
            .contains_entry({'data': 'OPTIONAL'})

    def test_key_optional_2(self):
        assert_that(self.process(key_optional, 'optional')) \
            .contains_only('data') \
            .contains_entry({'data': 'OPTIONAL'})

    def test_key_optional_3(self):
        assert_that(self.process(key_optional, ' optional ')) \
            .contains_only('data') \
            .contains_entry({'data': 'OPTIONAL'})

    def test_key_order_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_order, '~other~') \
            .starts_with('Expected key_order at position')

    def test_key_order_1(self):
        assert_that(self.process(key_order, 'ORDER')) \
            .contains_only('data') \
            .contains_entry({'data': 'ORDER'})

    def test_key_order_2(self):
        assert_that(self.process(key_order, 'order')) \
            .contains_only('data') \
            .contains_entry({'data': 'ORDER'})

    def test_key_order_3(self):
        assert_that(self.process(key_order, ' order ')) \
            .contains_only('data') \
            .contains_entry({'data': 'ORDER'})

    def test_func_properties_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_properties, '~other~') \
            .starts_with('Expected func_properties at position')

    def test_func_properties_1(self):
        assert_that(self.process(func_properties, 'PROPERTIES')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'properties'}})

    def test_func_properties_2(self):
        assert_that(self.process(func_properties, 'properties')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'properties'}})

    def test_func_properties_3(self):
        assert_that(self.process(func_properties, ' properties ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'properties'}})

    def test_key_return_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_return, '~other~') \
            .starts_with('Expected key_return at position')

    def test_key_return_1(self):
        assert_that(self.process(key_return, 'RETURN')) \
            .contains_only('data') \
            .contains_entry({'data': 'RETURN'})

    def test_key_return_2(self):
        result = self.process(key_return, 'return')

        assert_that(result).contains_only('data').contains_entry({'data': 'RETURN'})

    def test_key_return_3(self):
        assert_that(self.process(key_return, ' return ')) \
            .contains_only('data') \
            .contains_entry({'data': 'RETURN'})

    def test_key_rule_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_rule, '~other~') \
            .starts_with('Expected key_rule at position')

    def test_key_rule_1(self):
        assert_that(self.process(key_rule, 'RULE')) \
            .contains_only('data') \
            .contains_entry({'data': 'RULE'})

    def test_key_rule_2(self):
        result = self.process(key_rule, 'rule')

        assert_that(result).contains_only('data').contains_entry({'data': 'RULE'})

    def test_key_rule_3(self):
        assert_that(self.process(key_rule, ' rule ')) \
            .contains_only('data') \
            .contains_entry({'data': 'RULE'})

    def test_key_salience_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_salience, '~other~') \
            .starts_with('Expected key_salience at position')

    def test_key_salience_1(self):
        assert_that(self.process(key_salience, 'SALIENCE')) \
            .contains_only('data') \
            .contains_entry({'data': 'SALIENCE'})

    def test_key_salience_2(self):
        result = self.process(key_salience, 'salience')

        assert_that(result).contains_only('data').contains_entry({'data': 'SALIENCE'})

    def test_key_salience_3(self):
        assert_that(self.process(key_salience, ' salience ')) \
            .contains_only('data') \
            .contains_entry({'data': 'SALIENCE'})

    def test_key_skip_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(key_skip, '~other~') \
            .starts_with('Expected key_skip at position')

    def test_key_skip_1(self):
        assert_that(self.process(key_skip, 'SKIP')) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    def test_key_skip_2(self):
        result = self.process(key_skip, 'skip')

        assert_that(result) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    def test_key_skip_3(self):
        assert_that(self.process(key_skip, ' skip ')) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    def test_func_tail_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_tail, '~other~') \
            .starts_with('Expected func_tail at position')

    def test_func_tail_1(self):
        assert_that(self.process(func_tail, 'TAIL')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'tail'}})

    def test_func_tail_2(self):
        result = self.process(func_tail, 'tail')

        assert_that(result) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'tail'}})

    def test_func_tail_3(self):
        assert_that(self.process(func_tail, ' tail ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'tail'}})

    def test_func_types_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(func_types, '~other~') \
            .starts_with('Expected func_types at position')

    def test_func_types_1(self):
        assert_that(self.process(func_types, 'TYPES')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'types'}})

    def test_func_types_2(self):
        result = self.process(func_types, 'types')

        assert_that(result) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'types'}})

    def test_func_types_3(self):
        assert_that(self.process(func_types, ' types ')) \
            .contains_only('data') \
            .contains_entry({'data': {'function': 'types'}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
