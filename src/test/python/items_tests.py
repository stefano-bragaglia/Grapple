from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.grammar import first, item, item_all, item_coalesce, item_head, item_id, item_keys, item_labels, \
    item_length, item_nodes, item_properties, item_relations, item_selector, item_tail, item_types, item_value, items, \
    order_by
from grapple.tentative.visitor import KnowledgeVisitor


class TestItemsParsing(TestCase):
    def test_items_00(self):
        assert_that(self.process(items, '*, coalesce($ent."key", -.123) AS name, keys($ent) AS name, '
                                        'properties($ent) AS name, id($ent) AS name, labels($ent) AS name, '
                                        'types($ent) AS name, tail($ent) AS name, head($ent) AS name, '
                                        'length($ent) AS name, nodes($ent) AS name, relations($ent) AS name, '
                                        '$ent.key AS name, -.123 AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'items': [
                {'function': 'all'},
                {'function': 'coalesce', 'parameter': '$ent', 'field': 'key', 'value': -0.123, 'synonym': 'name'},
                {'function': 'keys', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'properties', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'id', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'labels', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'types', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'tail', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'head', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'length', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'nodes', 'parameter': '$ent', 'synonym': 'name'},
                {'function': 'relations', 'parameter': '$ent', 'synonym': 'name'},
                {'entity': '$ent', 'field': 'key', 'synonym': 'name'},
                {'value': -0.123, 'synonym': 'name'},
            ]}})

    def test_first_00(self):
        assert_that(self.process(first, '*')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'all'}}})

    def test_first_01(self):
        assert_that(self.process(first, 'coalesce($ent."key", -.123) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {
                'function': 'coalesce',
                'parameter': '$ent',
                'field': 'key',
                'value': -0.123,
                'synonym': 'name',
            }}})

    def test_first_02(self):
        assert_that(self.process(first, 'keys($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'keys', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_03(self):
        assert_that(self.process(first, 'properties($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'properties', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_04(self):
        assert_that(self.process(first, 'id($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'id', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_05(self):
        assert_that(self.process(first, 'labels($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'labels', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_06(self):
        assert_that(self.process(first, 'types($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'types', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_07(self):
        assert_that(self.process(first, 'tail($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'tail', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_08(self):
        assert_that(self.process(first, 'head($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'head', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_09(self):
        assert_that(self.process(first, 'length($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'length', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_10(self):
        assert_that(self.process(first, 'nodes($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'nodes', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_11(self):
        assert_that(self.process(first, 'relations($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'relations', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_first_12(self):
        assert_that(self.process(first, '$ent.key AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'entity': '$ent', 'field': 'key', 'synonym': 'name'}}})

    def test_first_13(self):
        assert_that(self.process(first, '-.123 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -0.123, 'synonym': 'name'}}})

    def test_item_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item, '*') \
            .starts_with("Expected func_coalesce or func_keys or func_properties or func_id or func_labels or "
                         "func_types or func_tail or func_head or func_length or func_nodes or func_relations or "
                         "entity or ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or "
                         "json_false or json_null or variable at position")

    def test_item_01(self):
        assert_that(self.process(item, 'coalesce($ent."key", -.123) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {
                'function': 'coalesce',
                'parameter': '$ent',
                'field': 'key',
                'value': -0.123,
                'synonym': 'name',
            }}})

    def test_item_02(self):
        assert_that(self.process(item, 'keys($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'keys', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_03(self):
        assert_that(self.process(item, 'properties($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'properties', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_04(self):
        assert_that(self.process(item, 'id($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'id', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_05(self):
        assert_that(self.process(item, 'labels($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'labels', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_06(self):
        assert_that(self.process(item, 'types($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'types', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_07(self):
        assert_that(self.process(item, 'tail($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'tail', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_08(self):
        assert_that(self.process(item, 'head($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'head', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_09(self):
        assert_that(self.process(item, 'length($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'length', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_10(self):
        assert_that(self.process(item, 'nodes($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'nodes', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_11(self):
        assert_that(self.process(item, 'relations($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'relations', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_12(self):
        assert_that(self.process(item, '$ent.key AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'entity': '$ent', 'field': 'key', 'synonym': 'name'}}})

    def test_item_13(self):
        assert_that(self.process(item, '-.123 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -0.123, 'synonym': 'name'}}})

    def test_item_all_99(self):
        assert_that(self.process(item_all, '*')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'all'}}})

    def test_item_coalesce_99(self):
        assert_that(self.process(item_coalesce, 'coalesce($ent."key", -.123) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {
                'function': 'coalesce',
                'parameter': '$ent',
                'field': 'key',
                'value': -0.123,
                'synonym': 'name',
            }}})

    def test_item_keys_99(self):
        assert_that(self.process(item_keys, 'keys($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'keys', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_properties_99(self):
        assert_that(self.process(item_properties, 'properties($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'properties', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_id_99(self):
        assert_that(self.process(item_id, 'id($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'id', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_labels_99(self):
        assert_that(self.process(item_labels, 'labels($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'labels', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_types_99(self):
        assert_that(self.process(item_types, 'types($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'types', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_tail_99(self):
        assert_that(self.process(item_tail, 'tail($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'tail', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_head_99(self):
        assert_that(self.process(item_head, 'head($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'head', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_length_99(self):
        assert_that(self.process(item_length, 'length($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'length', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_nodes_99(self):
        assert_that(self.process(item_nodes, 'nodes($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'nodes', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_relations_99(self):
        assert_that(self.process(item_relations, 'relations($ent) AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'function': 'relations', 'parameter': '$ent', 'synonym': 'name'}}})

    def test_item_selector_99(self):
        assert_that(self.process(item_selector, '$ent.key AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'entity': '$ent', 'field': 'key', 'synonym': 'name'}}})

    def test_item_value_99(self):
        assert_that(self.process(item_value, '-.123')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -0.123}}})

    def test_item_value_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, '~other~') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_item_value_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, '"string') \
            .starts_with("Expected '\"' at position")

    def test_item_value_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, "'string") \
            .starts_with("Expected ''' at position")

    def test_item_value_03(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, "string'") \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_item_value_04(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, 'string"') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_item_value_05(self):
        assert_that(self.process(item_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ''}}})

    def test_item_value_06(self):
        assert_that(self.process(item_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ''}}})

    def test_item_value_07(self):
        assert_that(self.process(item_value, '"string"')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 'string'}}})

    def test_item_value_08(self):
        assert_that(self.process(item_value, "'string'")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 'string'}}})

    def test_item_value_09(self):
        assert_that(self.process(item_value, '.123')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 0.123}}})

    def test_item_value_10(self):
        assert_that(self.process(item_value, '1.0E-2')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 0.01}}})

    def test_item_value_11(self):
        assert_that(self.process(item_value, '-5.')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5}}})

    def test_item_value_12(self):
        assert_that(self.process(item_value, '-5.0')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5.0}}})

    def test_item_value_13(self):
        assert_that(self.process(item_value, '0')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 0}}})

    def test_item_value_14(self):
        assert_that(self.process(item_value, '5')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 5}}})

    def test_item_value_15(self):
        assert_that(self.process(item_value, '-5')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5}}})

    def test_item_value_16(self):
        assert_that(self.process(item_value, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': {}}}})

    def test_item_value_17(self):
        assert_that(self.process(item_value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                         'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}}}})

    def test_item_value_18(self):
        assert_that(self.process(item_value, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': []}}})

    def test_item_value_19(self):
        assert_that(self.process(item_value, '[\'\', \'string\', "", "string"]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ['', 'string', '', 'string']}}})

    def test_item_value_20(self):
        assert_that(self.process(item_value, '[0, 5, -5]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [0, 5, -5]}}})

    def test_item_value_21(self):
        assert_that(self.process(item_value, '[.123, 1.0E-2, -5.0]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [0.123, 1.0E-2, -5.0]}}})

    def test_item_value_22(self):
        assert_that(self.process(item_value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]}}})

    def test_item_value_23(self):
        assert_that(self.process(item_value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]]')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'value': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]}}})

    def test_item_value_24(self):
        assert_that(self.process(item_value, '[TRUE, True, true]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [True, True, True]}}})

    def test_item_value_25(self):
        assert_that(self.process(item_value, '[FALSE, False, false]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [False, False, False]}}})

    def test_item_value_26(self):
        assert_that(self.process(item_value, '[NULL, Null, null]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [None, None, None]}}})

    def test_item_value_27(self):
        assert_that(self.process(item_value, '[$1Ab_, $_2Ab, $aB_4]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ['$1Ab_', '$_2Ab', '$aB_4']}}})

    def test_item_value_28(self):
        assert_that(self.process(item_value, '["string", -5, .123, {}, [], true, false, null, $1Ab_]')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']}}})

    def test_item_value_29(self):
        assert_that(self.process(item_value, 'TRUE')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True}}})

    def test_item_value_30(self):
        assert_that(self.process(item_value, 'true')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True}}})

    def test_item_value_31(self):
        assert_that(self.process(item_value, 'True')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True}}})

    def test_item_value_32(self):
        assert_that(self.process(item_value, 'FALSE')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False}}})

    def test_item_value_33(self):
        assert_that(self.process(item_value, 'false')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False}}})

    def test_item_value_34(self):
        assert_that(self.process(item_value, 'False')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False}}})

    def test_item_value_35(self):
        assert_that(self.process(item_value, 'NULL')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None}}})

    def test_item_value_36(self):
        assert_that(self.process(item_value, 'null')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None}}})

    def test_item_value_37(self):
        assert_that(self.process(item_value, 'Null')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None}}})

    def test_item_value_38(self):
        assert_that(self.process(item_value, '"" AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': '', 'synonym': 'name'}}})

    def test_item_value_39(self):
        assert_that(self.process(item_value, "'' AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': '', 'synonym': 'name'}}})

    def test_item_value_40(self):
        assert_that(self.process(item_value, '"string" AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 'string', 'synonym': 'name'}}})

    def test_item_value_41(self):
        assert_that(self.process(item_value, "'string' AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 'string', 'synonym': 'name'}}})

    def test_item_value_42(self):
        assert_that(self.process(item_value, '.123 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 0.123, 'synonym': 'name'}}})

    def test_item_value_43(self):
        assert_that(self.process(item_value, '1.0E-2 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 1.0E-2, 'synonym': 'name'}}})

    def test_item_value_44(self):
        assert_that(self.process(item_value, '-5. AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5}}})

    def test_item_value_45(self):
        assert_that(self.process(item_value, '-5.0 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5.0, 'synonym': 'name'}}})

    def test_item_value_46(self):
        assert_that(self.process(item_value, '0 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 0, 'synonym': 'name'}}})

    def test_item_value_47(self):
        assert_that(self.process(item_value, '5 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': 5, 'synonym': 'name'}}})

    def test_item_value_48(self):
        assert_that(self.process(item_value, '-5 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': -5, 'synonym': 'name'}}})

    def test_item_value_49(self):
        assert_that(self.process(item_value, "{} AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': {}, 'synonym': 'name'}}})

    def test_item_value_50(self):
        assert_that(self.process(item_value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v} AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                         'k5': True, 'k6': False, 'k7': None, 'k8': '$v'},
                                               'synonym': 'name'}}})

    def test_item_value_51(self):
        assert_that(self.process(item_value, '[] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [], 'synonym': 'name'}}})

    def test_item_value_52(self):
        assert_that(self.process(item_value, '[\'\', \'string\', "", "string"] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ['', 'string', '', 'string'], 'synonym': 'name'}}})

    def test_item_value_53(self):
        assert_that(self.process(item_value, '[0, 5, -5] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [0, 5, -5], 'synonym': 'name'}}})

    def test_item_value_54(self):
        assert_that(self.process(item_value, '[.123, 1.0E-2, -5.0] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [0.123, 1.0E-2, -5.0], 'synonym': 'name'}}})

    def test_item_value_55(self):
        assert_that(self.process(item_value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}] AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'value': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}], 'synonym': 'name'}}})

    def test_item_value_56(self):
        assert_that(
            self.process(item_value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]] AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'value': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']],
                               'synonym': 'name'}}})

    def test_item_value_57(self):
        assert_that(self.process(item_value, '[TRUE, True, true] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [True, True, True], 'synonym': 'name'}}})

    def test_item_value_58(self):
        assert_that(self.process(item_value, '[FALSE, False, false] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [False, False, False], 'synonym': 'name'}}})

    def test_item_value_59(self):
        assert_that(self.process(item_value, '[NULL, Null, null] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': [None, None, None], 'synonym': 'name'}}})

    def test_item_value_60(self):
        assert_that(self.process(item_value, '[$1Ab_, $_2Ab, $aB_4] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': ['$1Ab_', '$_2Ab', '$aB_4'], 'synonym': 'name'}}})

    def test_item_value_61(self):
        assert_that(self.process(item_value, '["string", -5, .123, {}, [], true, false, null, $1Ab_] AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'value': ['string', -5, 0.123, {}, [], True, False, None, '$1Ab_'], 'synonym': 'name'}}})

    def test_item_value_62(self):
        assert_that(self.process(item_value, 'TRUE AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_item_value_63(self):
        assert_that(self.process(item_value, 'true AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_item_value_64(self):
        assert_that(self.process(item_value, 'True AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_item_value_65(self):
        assert_that(self.process(item_value, 'FALSE AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_item_value_66(self):
        assert_that(self.process(item_value, 'false AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_item_value_67(self):
        assert_that(self.process(item_value, 'False AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_item_value_68(self):
        assert_that(self.process(item_value, 'NULL AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None, 'synonym': 'name'}}})

    def test_item_value_69(self):
        assert_that(self.process(item_value, 'null AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None, 'synonym': 'name'}}})

    def test_item_value_70(self):
        assert_that(self.process(item_value, 'Null AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None, 'synonym': 'name'}}})

    def test_order_by_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, '~other~') \
            .starts_with('Expected key_order at position')

    def test_order_by_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, 'ORDER') \
            .starts_with('Expected key_by at position')

    def test_order_by_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, 'ORDER BY') \
            .starts_with("Expected entity or entity or ''' or '\"' or identifier at position")

    def test_order_by_03(self):
        assert_that(self.process(order_by, 'ORDER BY $ent, $ent.key, "name"')) \
            .contains_only('data') \
            .contains_entry({'data': {'order_by': [
            {'ascending': True, 'entity': '$ent'},
            {'ascending': True, 'entity': '$ent', 'field': 'key'},
            {'ascending': True, 'name': 'name'},
        ]}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
