from unittest import TestCase

from arpeggio import NoMatch, ParserPython, SemanticError, visit_parse_tree
from assertpy import assert_that

from grapple.neat.grammar import return_part, return_items, return_first, return_item, return_all, return_coalesce, \
    return_default, return_keys, return_properties, return_id, return_labels, return_types, return_tail, return_head, \
    return_selector, return_value, return_synonym, return_order_by, return_order_by_items, return_order_by_item, \
    return_order_by_selector, return_parameter, return_property, return_order_by_name, return_ordering, \
    return_ordering_ascending, return_ordering_descending, return_skip, return_limit
from grapple.neat.visitor import KnowledgeVisitor


class TestGrammarVisitor(TestCase):
    def test_return_part_1(self):
        assert_that(self.process(return_part, 'RETURN DISTINCT *, coalesce($param.prop, 5) AS "synonym" '
                                              'ORDER BY synonym DESC SKIP 5 LIMIT 3')) \
            .contains_only('value') \
            .contains_entry({'value': {'return': {'distinct': True,
                                                  'items': [{'function': 'all'},
                                                            {'function': 'coalesce', 'parameter': '$param',
                                                             'property': 'prop', 'default': 5, 'as': 'synonym'}],
                                                  'order': [{'ascending': False, 'name': 'synonym'}],
                                                  'skip': 5,
                                                  'limit': 3}}})

    def test_return_items_1(self):
        assert_that(self.process(return_items, 'coalesce($param.prop, 5) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'items': [{'function': 'coalesce', 'parameter': '$param', 'property': 'prop',
                                                  'default': 5, 'as': 'synonym'}]}})

    def test_return_items_2(self):
        assert_that(self.process(return_items, '*, coalesce($param.prop, 5) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'items': [{'function': 'all'},
                                                 {'function': 'coalesce', 'parameter': '$param', 'property': 'prop',
                                                  'default': 5, 'as': 'synonym'}]}})

    def test_return_first_1(self):
        assert_that(self.process(return_first, '*')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'all'}})

    def test_return_first_2(self):
        assert_that(self.process(return_first, 'coalesce($param.prop, 5) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'coalesce', 'parameter': '$param', 'property': 'prop', 'default': 5,
                                       'as': 'synonym'}})

    def test_return_first_3(self):
        assert_that(self.process(return_first, 'keys($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'keys', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_4(self):
        assert_that(self.process(return_first, 'properties($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'properties', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_5(self):
        assert_that(self.process(return_first, 'id($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'id', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_6(self):
        assert_that(self.process(return_first, 'labels($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'labels', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_7(self):
        assert_that(self.process(return_first, 'types($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'types', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_8(self):
        assert_that(self.process(return_first, 'tail($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'tail', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_9(self):
        assert_that(self.process(return_first, 'head($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'head', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_first_10(self):
        assert_that(self.process(return_first, '$param.prop AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': 'prop', 'as': 'synonym'}})

    def test_return_first_11(self):
        assert_that(self.process(return_first, '5 AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'value': 5, 'as': 'synonym'}})

    def test_return_item_1(self):
        assert_that(self.process(return_item, 'coalesce($param.prop, 5) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'coalesce', 'parameter': '$param', 'property': 'prop', 'default': 5,
                                       'as': 'synonym'}})

    def test_return_item_2(self):
        assert_that(self.process(return_item, 'keys($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'keys', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_3(self):
        assert_that(self.process(return_item, 'properties($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'properties', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_4(self):
        assert_that(self.process(return_item, 'id($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'id', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_5(self):
        assert_that(self.process(return_item, 'labels($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'labels', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_6(self):
        assert_that(self.process(return_item, 'types($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'types', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_7(self):
        assert_that(self.process(return_item, 'tail($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'tail', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_8(self):
        assert_that(self.process(return_item, 'head($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'head', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_item_9(self):
        assert_that(self.process(return_item, '$param.prop AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': 'prop', 'as': 'synonym'}})

    def test_return_item_10(self):
        assert_that(self.process(return_item, '5 AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'value': 5, 'as': 'synonym'}})

    def test_return_all_1(self):
        assert_that(self.process(return_all, '*')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'all'}})

    def test_return_coalesce_1(self):
        assert_that(self.process(return_coalesce, 'coalesce($param.prop, 5) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'coalesce', 'parameter': '$param', 'property': 'prop', 'default': 5,
                                       'as': 'synonym'}})

    def test_return_default_1(self):
        assert_that(self.process(return_default, ', 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'default': 5}})

    def test_return_keys_1(self):
        assert_that(self.process(return_keys, 'keys($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'keys', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_properties_1(self):
        assert_that(self.process(return_properties, 'properties($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'properties', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_id_1(self):
        assert_that(self.process(return_id, 'id($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'id', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_labels_1(self):
        assert_that(self.process(return_labels, 'labels($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'labels', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_types_1(self):
        assert_that(self.process(return_types, 'types($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'types', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_tail_1(self):
        assert_that(self.process(return_tail, 'tail($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'tail', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_head_1(self):
        assert_that(self.process(return_head, 'head($param) AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'function': 'head', 'parameter': '$param', 'as': 'synonym'}})

    def test_return_selector_1(self):
        assert_that(self.process(return_selector, '$param.prop AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': 'prop', 'as': 'synonym'}})

    def test_return_value_1(self):
        assert_that(self.process(return_value, '5 AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'value': 5, 'as': 'synonym'}})

    # ------------------------------------------------------------------------------------------------------------------
    def test_return_synonym_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_synonym, '~other~') \
            .starts_with("Expected key_as at position")

    def test_return_synonym_1(self):
        assert_that(self.process(return_synonym, 'AS "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_2(self):
        assert_that(self.process(return_synonym, 'As "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_3(self):
        assert_that(self.process(return_synonym, 'as "synonym"')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_4(self):
        assert_that(self.process(return_synonym, "AS 'synonym'")) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_5(self):
        assert_that(self.process(return_synonym, "As 'synonym'")) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_6(self):
        assert_that(self.process(return_synonym, "as 'synonym'")) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_7(self):
        assert_that(self.process(return_synonym, 'AS synonym')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_8(self):
        assert_that(self.process(return_synonym, 'As synonym')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_synonym_9(self):
        assert_that(self.process(return_synonym, 'as synonym')) \
            .contains_only('value') \
            .contains_entry({'value': {'as': 'synonym'}})

    def test_return_order_by_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_order_by, '~other~') \
            .starts_with("Expected key_order at position")

    def test_return_order_by_1(self):
        assert_that(self.process(return_order_by, 'ORDER BY $param."_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'order': [{'parameter': '$param', 'property': '_string', 'ascending': False}]}})

    def test_return_order_by_2(self):
        assert_that(self.process(return_order_by, 'ORDER BY _name ASC, $param, $param."_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'order': [{'name': '_name', 'ascending': True},
                                                 {'parameter': '$param', 'ascending': True},
                                                 {'parameter': '$param', 'property': '_string', 'ascending': False}]}})

    def test_return_order_by_items_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_order_by_items, '~other~') \
            .starts_with("Expected return_parameter or ''' or '\"' or identifier at position")

    def test_return_order_by_items_1(self):
        assert_that(self.process(return_order_by_items, '$param."_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': [{'parameter': '$param', 'property': '_string', 'ascending': False}]})

    def test_return_order_by_items_2(self):
        assert_that(self.process(return_order_by_items, '_name ASC, $param, $param."_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': [{'name': '_name', 'ascending': True},
                                       {'parameter': '$param', 'ascending': True},
                                       {'parameter': '$param', 'property': '_string', 'ascending': False}]})

    def test_return_order_by_item_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_order_by_item, '~other~') \
            .starts_with("Expected return_parameter or ''' or '\"' or identifier at position")

    def test_return_order_by_item_1(self):
        assert_that(self.process(return_order_by_item, '$param')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'ascending': True}})

    def test_return_order_by_item_2(self):
        assert_that(self.process(return_order_by_item, '$param."_string"')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_3(self):
        assert_that(self.process(return_order_by_item, "$param.'_string'")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_4(self):
        assert_that(self.process(return_order_by_item, "$param._string")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_5(self):
        assert_that(self.process(return_order_by_item, '"_string"')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_6(self):
        assert_that(self.process(return_order_by_item, "'_string'")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_7(self):
        assert_that(self.process(return_order_by_item, '_string')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_8(self):
        assert_that(self.process(return_order_by_item, '$param ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'ascending': True}})

    def test_return_order_by_item_9(self):
        assert_that(self.process(return_order_by_item, '$param."_string" ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_10(self):
        assert_that(self.process(return_order_by_item, "$param.'_string' ASC")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_11(self):
        assert_that(self.process(return_order_by_item, "$param._string ASC")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_12(self):
        assert_that(self.process(return_order_by_item, '"_string" ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_13(self):
        assert_that(self.process(return_order_by_item, "'_string' ASC")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_14(self):
        assert_that(self.process(return_order_by_item, '_string ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_15(self):
        assert_that(self.process(return_order_by_item, '$param ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'ascending': True}})

    def test_return_order_by_item_16(self):
        assert_that(self.process(return_order_by_item, '$param."_string" ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_17(self):
        assert_that(self.process(return_order_by_item, "$param.'_string' ASCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_18(self):
        assert_that(self.process(return_order_by_item, "$param._string ASCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': True}})

    def test_return_order_by_item_19(self):
        assert_that(self.process(return_order_by_item, '"_string" ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_20(self):
        assert_that(self.process(return_order_by_item, "'_string' ASCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_21(self):
        assert_that(self.process(return_order_by_item, '_string ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': True}})

    def test_return_order_by_item_22(self):
        assert_that(self.process(return_order_by_item, '$param DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'ascending': False}})

    def test_return_order_by_item_23(self):
        assert_that(self.process(return_order_by_item, '$param."_string" DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_24(self):
        assert_that(self.process(return_order_by_item, "$param.'_string' DESC")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_25(self):
        assert_that(self.process(return_order_by_item, "$param._string DESC")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_26(self):
        assert_that(self.process(return_order_by_item, '"_string" DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_item_27(self):
        assert_that(self.process(return_order_by_item, "'_string' DESC")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_item_28(self):
        assert_that(self.process(return_order_by_item, '_string DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_item_29(self):
        assert_that(self.process(return_order_by_item, '$param DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'ascending': False}})

    def test_return_order_by_item_30(self):
        assert_that(self.process(return_order_by_item, '$param."_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_31(self):
        assert_that(self.process(return_order_by_item, "$param.'_string' DESCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_32(self):
        assert_that(self.process(return_order_by_item, "$param._string DESCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string', 'ascending': False}})

    def test_return_order_by_item_33(self):
        assert_that(self.process(return_order_by_item, '"_string" DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_item_34(self):
        assert_that(self.process(return_order_by_item, "'_string' DESCENDING")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_item_35(self):
        assert_that(self.process(return_order_by_item, '_string DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string', 'ascending': False}})

    def test_return_order_by_selector_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_order_by_selector, '~other~') \
            .starts_with("Expected return_parameter at position")

    def test_return_order_by_selector_1(self):
        assert_that(self.process(return_order_by_selector, '$param')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param'}})

    def test_return_order_by_selector_2(self):
        assert_that(self.process(return_order_by_selector, '$param."_string"')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string'}})

    def test_return_order_by_selector_3(self):
        assert_that(self.process(return_order_by_selector, "$param.'_string'")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string'}})

    def test_return_order_by_selector_4(self):
        assert_that(self.process(return_order_by_selector, "$param._string")) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param', 'property': '_string'}})

    def test_return_parameter_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_parameter, '~other~') \
            .starts_with("Expected return_parameter at position")

    def test_return_parameter_1(self):
        assert_that(self.process(return_parameter, '$param')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$param'}})

    def test_return_property_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_property, '~other~') \
            .starts_with("Expected '.' at position")

    def test_return_property_1(self):
        assert_that(self.process(return_property, '."_string"')) \
            .contains_only('value') \
            .contains_entry({'value': {'property': '_string'}})

    def test_return_property_2(self):
        assert_that(self.process(return_property, ".'_string'")) \
            .contains_only('value') \
            .contains_entry({'value': {'property': '_string'}})

    def test_return_property_3(self):
        assert_that(self.process(return_property, '._string')) \
            .contains_only('value') \
            .contains_entry({'value': {'property': '_string'}})

    def test_return_order_by_name_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_order_by_name, '~other~') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_return_order_by_name_1(self):
        assert_that(self.process(return_order_by_name, '"_string"')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string'}})

    def test_return_order_by_name_2(self):
        assert_that(self.process(return_order_by_name, "'_string'")) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string'}})

    def test_return_order_by_name_3(self):
        assert_that(self.process(return_order_by_name, '_string')) \
            .contains_only('value') \
            .contains_entry({'value': {'name': '_string'}})

    def test_return_ordering_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_ordering, '~other~') \
            .starts_with('Expected key_asc or key_ascending or key_desc or key_descending at position')

    def test_return_ordering_1(self):
        assert_that(self.process(return_ordering, 'ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_2(self):
        assert_that(self.process(return_ordering, 'Asc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_3(self):
        assert_that(self.process(return_ordering, 'asc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_4(self):
        assert_that(self.process(return_ordering, 'ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_5(self):
        assert_that(self.process(return_ordering, 'Ascending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_6(self):
        assert_that(self.process(return_ordering, 'ascending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_7(self):
        assert_that(self.process(return_ordering, 'DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_8(self):
        assert_that(self.process(return_ordering, 'Desc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_9(self):
        assert_that(self.process(return_ordering, 'desc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_10(self):
        assert_that(self.process(return_ordering, 'DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_11(self):
        assert_that(self.process(return_ordering, 'Descending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_12(self):
        assert_that(self.process(return_ordering, 'descending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_ascending_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_ordering_ascending, '~other~') \
            .starts_with('Expected key_asc or key_ascending at position')

    def test_return_ordering_ascending_1(self):
        assert_that(self.process(return_ordering_ascending, 'ASC')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_ascending_2(self):
        assert_that(self.process(return_ordering_ascending, 'Asc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_ascending_3(self):
        assert_that(self.process(return_ordering_ascending, 'asc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_ascending_4(self):
        assert_that(self.process(return_ordering_ascending, 'ASCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_ascending_5(self):
        assert_that(self.process(return_ordering_ascending, 'Ascending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_ascending_6(self):
        assert_that(self.process(return_ordering_ascending, 'ascending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': True}})

    def test_return_ordering_descending_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_ordering_descending, '~other~') \
            .starts_with('Expected key_desc or key_descending at position')

    def test_return_ordering_descending_1(self):
        assert_that(self.process(return_ordering_descending, 'DESC')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_descending_2(self):
        assert_that(self.process(return_ordering_descending, 'Desc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_descending_3(self):
        assert_that(self.process(return_ordering_descending, 'desc')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_descending_4(self):
        assert_that(self.process(return_ordering_descending, 'DESCENDING')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_descending_5(self):
        assert_that(self.process(return_ordering_descending, 'Descending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_ordering_descending_6(self):
        assert_that(self.process(return_ordering_descending, 'descending')) \
            .contains_only('value') \
            .contains_entry({'value': {'ascending': False}})

    def test_return_skip_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_skip, '~other~') \
            .starts_with('Expected key_skip at position')

    def test_return_skip_1(self):
        assert_that(self.process(return_skip, 'SKIP 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'skip': 0}})

    def test_return_skip_2(self):
        assert_that(self.process(return_skip, 'SKIP 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'skip': 5}})

    def test_return_skip_3(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(return_skip, 'SKIP -5') \
            .starts_with("\"'skip' expected to be non-negative\"")

    def test_return_limit_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(return_limit, '~other~') \
            .starts_with('Expected key_limit at position')

    def test_return_limit_1(self):
        assert_that(self.process(return_limit, 'LIMIT 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'limit': 0}})

    def test_return_limit_2(self):
        assert_that(self.process(return_limit, 'LIMIT 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'limit': 5}})

    def test_return_limit_3(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(return_limit, 'LIMIT -5') \
            .starts_with("\"'limit' expected to be non-negative\"")

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
