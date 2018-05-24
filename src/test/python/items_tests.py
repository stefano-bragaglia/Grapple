from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import item_value, order_by
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):

    def test_value_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, '~other~') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, '"string') \
            .starts_with("Expected '\"' at position")

    def test_value_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, "'string") \
            .starts_with("Expected ''' at position")

    def test_value_03(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, "string'") \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_04(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(item_value, 'string"') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_05(self):
        assert_that(self.process(item_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': ''}]}})

    def test_value_06(self):
        assert_that(self.process(item_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': ''}]}})

    def test_value_07(self):
        assert_that(self.process(item_value, '"string"')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': 'string'}]}})

    def test_value_08(self):
        assert_that(self.process(item_value, "'string'")) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': 'string'}]}})

    def test_value_09(self):
        assert_that(self.process(item_value, '.123')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': 0.123}]}})

    def test_value_10(self):
        assert_that(self.process(item_value, '1.0E-2')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': 0.01}]}})

    def test_value_11(self):
        assert_that(self.process(item_value, '-5.')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': -5}]}})

    def test_value_12(self):
        assert_that(self.process(item_value, '-5.0')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': [{'value': -5.0}]}})

    def test_value_13(self):
        assert_that(self.process(item_value, '0')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 0}})

    def test_value_14(self):
        assert_that(self.process(item_value, '5')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 5}})

    def test_value_15(self):
        assert_that(self.process(item_value, '-5')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5}})

    def test_value_16(self):
        assert_that(self.process(item_value, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {}}})

    def test_value_17(self):
        assert_that(self.process(item_value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}}})

    def test_value_18(self):
        assert_that(self.process(item_value, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': []}})

    def test_value_19(self):
        assert_that(self.process(item_value, '[\'\', \'string\', "", "string"]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['', 'string', '', 'string']}})

    def test_value_20(self):
        assert_that(self.process(item_value, '[0, 5, -5]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0, 5, -5]}})

    def test_value_21(self):
        assert_that(self.process(item_value, '[.123, 1.0E-2, -5.0]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0.123, 1.0E-2, -5.0]}})

    def test_value_22(self):
        assert_that(self.process(item_value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]}})

    def test_value_23(self):
        assert_that(self.process(item_value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]}})

    def test_value_24(self):
        assert_that(self.process(item_value, '[TRUE, True, true]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [True, True, True]}})

    def test_value_25(self):
        assert_that(self.process(item_value, '[FALSE, False, false]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [False, False, False]}})

    def test_value_26(self):
        assert_that(self.process(item_value, '[NULL, Null, null]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [None, None, None]}})

    def test_value_27(self):
        assert_that(self.process(item_value, '[$1Ab_, $_2Ab, $aB_4]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['$1Ab_', '$_2Ab', '$aB_4']}})

    def test_value_28(self):
        assert_that(self.process(item_value, '["string", -5, .123, {}, [], true, false, null, $1Ab_]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']}})

    def test_value_29(self):
        assert_that(self.process(item_value, 'TRUE')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_30(self):
        assert_that(self.process(item_value, 'true')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_31(self):
        assert_that(self.process(item_value, 'True')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_32(self):
        assert_that(self.process(item_value, 'FALSE')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_33(self):
        assert_that(self.process(item_value, 'false')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_34(self):
        assert_that(self.process(item_value, 'False')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_35(self):
        assert_that(self.process(item_value, 'NULL')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

    def test_value_36(self):
        assert_that(self.process(item_value, 'null')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

    def test_value_37(self):
        assert_that(self.process(item_value, 'Null')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

    def test_value_38(self):
        assert_that(self.process(item_value, '"" AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ''}})

    def test_value_39(self):
        assert_that(self.process(item_value, "'' AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ''}})

    def test_value_40(self):
        assert_that(self.process(item_value, '"string" AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 'string'}})

    def test_value_41(self):
        assert_that(self.process(item_value, "'string' AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 'string'}})

    def test_value_42(self):
        assert_that(self.process(item_value, '.123 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 0.123}})

    def test_value_43(self):
        assert_that(self.process(item_value, '1.0E-2 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 1.0E-2}})

    def test_value_44(self):
        assert_that(self.process(item_value, '-5. AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5.0}})

    def test_value_45(self):
        assert_that(self.process(item_value, '-5.0 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5.0}})

    def test_value_46(self):
        assert_that(self.process(item_value, '0 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 0}})

    def test_value_47(self):
        assert_that(self.process(item_value, '5 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 5}})

    def test_value_48(self):
        assert_that(self.process(item_value, '-5 AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5}})

    def test_value_49(self):
        assert_that(self.process(item_value, "{} AS name")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {}}})

    def test_value_50(self):
        assert_that(self.process(item_value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v} AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}}})

    def test_value_51(self):
        assert_that(self.process(item_value, '[] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': []}})

    def test_value_52(self):
        assert_that(self.process(item_value, '[\'\', \'string\', "", "string"] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['', 'string', '', 'string']}})

    def test_value_53(self):
        assert_that(self.process(item_value, '[0, 5, -5] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0, 5, -5]}})

    def test_value_54(self):
        assert_that(self.process(item_value, '[.123, 1.0E-2, -5.0] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0.123, 1.0E-2, -5.0]}})

    def test_value_55(self):
        assert_that(self.process(item_value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]}})

    def test_value_56(self):
        assert_that(
            self.process(item_value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]}})

    def test_value_57(self):
        assert_that(self.process(item_value, '[TRUE, True, true] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [True, True, True]}})

    def test_value_58(self):
        assert_that(self.process(item_value, '[FALSE, False, false] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [False, False, False]}})

    def test_value_59(self):
        assert_that(self.process(item_value, '[NULL, Null, null] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [None, None, None]}})

    def test_value_60(self):
        assert_that(self.process(item_value, '[$1Ab_, $_2Ab, $aB_4] AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['$1Ab_', '$_2Ab', '$aB_4']}})

    def test_value_61(self):
        assert_that(self.process(item_value, '["string", -5, .123, {}, [], true, false, null, $1Ab_] AS name')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'item': {'value': ['string', -5, 0.123, {}, [], True, False, None, '$1Ab_'], 'synonym': 'name'}}})

    def test_value_62(self):
        assert_that(self.process(item_value, 'TRUE AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_value_63(self):
        assert_that(self.process(item_value, 'true AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_value_64(self):
        assert_that(self.process(item_value, 'True AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': True, 'synonym': 'name'}}})

    def test_value_65(self):
        assert_that(self.process(item_value, 'FALSE AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_value_66(self):
        assert_that(self.process(item_value, 'false AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_value_67(self):
        assert_that(self.process(item_value, 'False AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': False, 'synonym': 'name'}}})

    def test_value_68(self):
        assert_that(self.process(item_value, 'NULL AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None, 'synonym': 'name'}}})

    def test_value_69(self):
        assert_that(self.process(item_value, 'null AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'item': {'value': None, 'synonym': 'name'}}})

    def test_value_70(self):
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
        assert_that(self.process(order_by, 'ORDER BY $ent')) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    # All the sortables here

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
