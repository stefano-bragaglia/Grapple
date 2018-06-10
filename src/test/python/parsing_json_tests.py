from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.grammar import json_array, json_elements, json_false, json_integer, json_key, json_member, \
    json_members, json_null, json_object, json_real, json_string, json_true, json_value
from grapple.visitor import KnowledgeVisitor


class TestJsonParsing(TestCase):
    def test_json_object_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_object, '~other~') \
            .starts_with("Expected '{' at position")

    def test_json_object_1(self):
        assert_that(self.process(json_object, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {}})

    def test_json_object_2(self):
        assert_that(self.process(json_object, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                              '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                      'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}})

    def test_json_members_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_members, '~other~') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_json_members_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_members, '{}') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_json_members_2(self):
        assert_that(self.process(json_members, '\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                               '"k5": true, k6: false, \'k7\': null, "k8": $v')) \
            .contains_only('data') \
            .contains_entry({'data': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                      'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}})

    def test_json_member_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_member, '~other~') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_json_member_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_member, '5: null') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_json_member_2(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_member, '"key" $var') \
            .starts_with("Expected ':' at position")

    def test_json_member_3(self):
        assert_that(self.process(json_member, "'key': 'value'")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_4(self):
        assert_that(self.process(json_member, "'key': \"value\"")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_5(self):
        assert_that(self.process(json_member, "'key': .123")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 0.123}})

    def test_json_member_6(self):
        assert_that(self.process(json_member, "'key': -5")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': -5}})

    def test_json_member_7(self):
        assert_that(self.process(json_member, "'key': {'key': null}")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': {'key': None}}})

    def test_json_member_8(self):
        assert_that(self.process(json_member, "'key': [true, false]")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': [True, False]}})

    def test_json_member_9(self):
        assert_that(self.process(json_member, "'key': true")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': True}})

    def test_json_member_10(self):
        assert_that(self.process(json_member, "'key': false")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': False}})

    def test_json_member_11(self):
        assert_that(self.process(json_member, "'key': null")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': None}})

    def test_json_member_12(self):
        assert_that(self.process(json_member, "'key': $v")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': '$v'}})

    def test_json_member_13(self):
        assert_that(self.process(json_member, "\"key\": 'value'")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_14(self):
        assert_that(self.process(json_member, "\"key\": \"value\"")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_15(self):
        assert_that(self.process(json_member, "\"key\": .123")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 0.123}})

    def test_json_member_16(self):
        assert_that(self.process(json_member, "\"key\": -5")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': -5}})

    def test_json_member_17(self):
        assert_that(self.process(json_member, "\"key\": {'key': null}")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': {'key': None}}})

    def test_json_member_18(self):
        assert_that(self.process(json_member, "\"key\": [true, false]")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': [True, False]}})

    def test_json_member_19(self):
        assert_that(self.process(json_member, "\"key\": true")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': True}})

    def test_json_member_20(self):
        assert_that(self.process(json_member, "\"key\": false")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': False}})

    def test_json_member_21(self):
        assert_that(self.process(json_member, "\"key\": null")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': None}})

    def test_json_member_22(self):
        assert_that(self.process(json_member, "\"key\": $v")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': '$v'}})

    def test_json_member_23(self):
        assert_that(self.process(json_member, "key: 'value'")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_24(self):
        assert_that(self.process(json_member, "key: \"value\"")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 'value'}})

    def test_json_member_25(self):
        assert_that(self.process(json_member, "key: .123")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': 0.123}})

    def test_json_member_26(self):
        assert_that(self.process(json_member, "key: -5")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': -5}})

    def test_json_member_27(self):
        assert_that(self.process(json_member, "key: {'key': null}")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': {'key': None}}})

    def test_json_member_28(self):
        assert_that(self.process(json_member, "key: [true, false]")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': [True, False]}})

    def test_json_member_29(self):
        assert_that(self.process(json_member, "key: true")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': True}})

    def test_json_member_30(self):
        assert_that(self.process(json_member, "key: false")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': False}})

    def test_json_member_31(self):
        assert_that(self.process(json_member, "key: null")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': None}})

    def test_json_member_32(self):
        assert_that(self.process(json_member, "key: $v")) \
            .contains_only('data') \
            .contains_entry({'data': {'key': '$v'}})

    def test_json_value_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_value, '~other~') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_json_value_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_value, '"string') \
            .starts_with("Expected '\"' at position")

    def test_json_value_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_value, "'string") \
            .starts_with("Expected ''' at position")

    def test_json_value_03(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_value, "string'") \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_json_value_04(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_value, 'string"') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_json_value_05(self):
        assert_that(self.process(json_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_value_06(self):
        assert_that(self.process(json_value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_value_07(self):
        assert_that(self.process(json_value, '"string"')) \
            .contains_only('data') \
            .contains_entry({'data': 'string'})

    def test_json_value_08(self):
        assert_that(self.process(json_value, "'string'")) \
            .contains_only('data') \
            .contains_entry({'data': 'string'})

    def test_json_value_09(self):
        assert_that(self.process(json_value, '.123')) \
            .contains_only('data') \
            .contains_entry({'data': 0.123})

    def test_json_value_10(self):
        assert_that(self.process(json_value, '1.0E-2')) \
            .contains_only('data') \
            .contains_entry({'data': 1.0E-2})

    def test_json_value_11(self):
        assert_that(self.process(json_value, '-5.')) \
            .contains_only('data') \
            .contains_entry({'data': -5.0})

    def test_json_value_12(self):
        assert_that(self.process(json_value, '-5.0')) \
            .contains_only('data') \
            .contains_entry({'data': -5.0})

    def test_json_value_13(self):
        assert_that(self.process(json_value, '0')) \
            .contains_only('data') \
            .contains_entry({'data': 0})

    def test_json_value_14(self):
        assert_that(self.process(json_value, '5')) \
            .contains_only('data') \
            .contains_entry({'data': 5})

    def test_json_value_15(self):
        assert_that(self.process(json_value, '-5')) \
            .contains_only('data') \
            .contains_entry({'data': -5})

    def test_json_value_16(self):
        assert_that(self.process(json_value, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {}})

    def test_json_value_17(self):
        assert_that(self.process(json_value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                      'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}})

    def test_json_value_18(self):
        assert_that(self.process(json_value, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': []})

    def test_json_value_19(self):
        assert_that(self.process(json_value, '[\'\', \'string\', "", "string"]')) \
            .contains_only('data') \
            .contains_entry({'data': ['', 'string', '', 'string']})

    def test_json_value_20(self):
        assert_that(self.process(json_value, '[0, 5, -5]')) \
            .contains_only('data') \
            .contains_entry({'data': [0, 5, -5]})

    def test_json_value_21(self):
        assert_that(self.process(json_value, '[.123, 1.0E-2, -5.0]')) \
            .contains_only('data') \
            .contains_entry({'data': [0.123, 1.0E-2, -5.0]})

    def test_json_value_22(self):
        assert_that(self.process(json_value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}]')) \
            .contains_only('data') \
            .contains_entry({'data': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]})

    def test_json_value_23(self):
        assert_that(self.process(json_value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]]')) \
            .contains_only('data') \
            .contains_entry({'data': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]})

    def test_json_value_24(self):
        assert_that(self.process(json_value, '[TRUE, True, true]')) \
            .contains_only('data') \
            .contains_entry({'data': [True, True, True]})

    def test_json_value_25(self):
        assert_that(self.process(json_value, '[FALSE, False, false]')) \
            .contains_only('data') \
            .contains_entry({'data': [False, False, False]})

    def test_json_value_26(self):
        assert_that(self.process(json_value, '[NULL, Null, null]')) \
            .contains_only('data') \
            .contains_entry({'data': [None, None, None]})

    def test_json_value_27(self):
        assert_that(self.process(json_value, '[$1Ab_, $_2Ab, $aB_4]')) \
            .contains_only('data') \
            .contains_entry({'data': ['$1Ab_', '$_2Ab', '$aB_4']})

    def test_json_value_28(self):
        assert_that(self.process(json_value, '["string", -5, .123, {}, [], true, false, null, $1Ab_]')) \
            .contains_only('data') \
            .contains_entry({'data': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']})

    def test_json_value_29(self):
        assert_that(self.process(json_value, 'TRUE')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_value_30(self):
        assert_that(self.process(json_value, 'true')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_value_31(self):
        assert_that(self.process(json_value, 'True')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_value_32(self):
        assert_that(self.process(json_value, 'FALSE')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_value_33(self):
        assert_that(self.process(json_value, 'false')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_value_34(self):
        assert_that(self.process(json_value, 'False')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_value_35(self):
        assert_that(self.process(json_value, 'NULL')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    def test_json_value_36(self):
        assert_that(self.process(json_value, 'null')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    def test_json_value_37(self):
        assert_that(self.process(json_value, 'Null')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    def test_json_key_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_key, '"key') \
            .starts_with("Expected '\"' at position")

    def test_json_key_2(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_key, "'key") \
            .starts_with("Expected ''' at position")

    def test_json_key_3(self):
        assert_that(self.process(json_key, "''")) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_key_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_key, '~other~') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_json_key_4(self):
        assert_that(self.process(json_key, '""')) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_key_5(self):
        assert_that(self.process(json_key, "key'")) \
            .contains_only('data') \
            .contains_entry({'data': 'key'})

    def test_json_key_6(self):
        assert_that(self.process(json_key, 'key"')) \
            .contains_only('data') \
            .contains_entry({'data': 'key'})

    def test_json_key_7(self):
        assert_that(self.process(json_key, "'key'")) \
            .contains_only('data') \
            .contains_entry({'data': 'key'})

    def test_json_key_8(self):
        assert_that(self.process(json_key, '"key"')) \
            .contains_only('data') \
            .contains_entry({'data': 'key'})

    def test_json_key_9(self):
        assert_that(self.process(json_key, 'key')) \
            .contains_only('data') \
            .contains_entry({'data': 'key'})

    def test_json_string_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_string, '~other~') \
            .starts_with("Expected ''' or '\"' at position")

    def test_json_string_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_string, '"string') \
            .starts_with("Expected '\"' at position")

    def test_json_string_2(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_string, "'string") \
            .starts_with("Expected ''' at position")

    def test_json_string_3(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_string, "string'") \
            .starts_with("Expected ''' or '\"' at position")

    def test_json_string_4(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_string, 'string"') \
            .starts_with("Expected ''' or '\"' at position")

    def test_json_string_5(self):
        assert_that(self.process(json_string, '""')) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_string_6(self):
        assert_that(self.process(json_string, '""')) \
            .contains_only('data') \
            .contains_entry({'data': ''})

    def test_json_string_7(self):
        assert_that(self.process(json_string, '"string"')) \
            .contains_only('data') \
            .contains_entry({'data': 'string'})

    def test_json_string_8(self):
        assert_that(self.process(json_string, "'string'")) \
            .contains_only('data') \
            .contains_entry({'data': 'string'})

    def test_json_integer_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_integer, '~other~') \
            .starts_with('Expected json_integer at position')

    def test_json_integer_1(self):
        assert_that(self.process(json_integer, '0')) \
            .contains_only('data') \
            .contains_entry({'data': 0})

    def test_json_integer_2(self):
        assert_that(self.process(json_integer, '5')) \
            .contains_only('data') \
            .contains_entry({'data': 5})

    def test_json_integer_3(self):
        assert_that(self.process(json_integer, '-5')) \
            .contains_only('data') \
            .contains_entry({'data': -5})

    def test_json_real_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_real, '~other~') \
            .starts_with('Expected json_real at position')

    def test_json_real_1(self):
        assert_that(self.process(json_real, '.123')) \
            .contains_only('data') \
            .contains_entry({'data': 0.123})

    def test_json_real_2(self):
        assert_that(self.process(json_real, '1.0E-2')) \
            .contains_only('data') \
            .contains_entry({'data': 1.0E-2})

    def test_json_real_3(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_real, '-5.') \
            .starts_with('Expected json_real at position')

    def test_json_real_4(self):
        assert_that(self.process(json_real, '-5.0')) \
            .contains_only('data') \
            .contains_entry({'data': -5.0})

    def test_json_real_5(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_real, '5') \
            .starts_with("Expected json_real at position")

    def test_json_array_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_array, '~other~') \
            .starts_with("Expected '[' at position")

    def test_json_array_1(self):
        assert_that(self.process(json_array, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': []})

    def test_json_array_2(self):
        assert_that(self.process(json_array, '[\'\', \'string\', "", "string"]')) \
            .contains_only('data') \
            .contains_entry({'data': ['', 'string', '', 'string']})

    def test_json_array_3(self):
        assert_that(self.process(json_array, '[0, 5, -5]')) \
            .contains_only('data') \
            .contains_entry({'data': [0, 5, -5]})

    def test_json_array_4(self):
        assert_that(self.process(json_array, '[.123, 1.0E-2, -5.0]')) \
            .contains_only('data') \
            .contains_entry({'data': [0.123, 1.0E-2, -5.0]})

    def test_json_array_5(self):
        assert_that(self.process(json_array, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}]')) \
            .contains_only('data') \
            .contains_entry({'data': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]})

    def test_json_array_6(self):
        assert_that(self.process(json_array, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]]')) \
            .contains_only('data') \
            .contains_entry({'data': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]})

    def test_json_array_7(self):
        assert_that(self.process(json_array, '[TRUE, True, true]')) \
            .contains_only('data') \
            .contains_entry({'data': [True, True, True]})

    def test_json_array_8(self):
        assert_that(self.process(json_array, '[FALSE, False, false]')) \
            .contains_only('data') \
            .contains_entry({'data': [False, False, False]})

    def test_json_array_9(self):
        assert_that(self.process(json_array, '[NULL, Null, null]')) \
            .contains_only('data') \
            .contains_entry({'data': [None, None, None]})

    def test_json_array_10(self):
        assert_that(self.process(json_array, '[$1Ab_, $_2Ab, $aB_4]')) \
            .contains_only('data') \
            .contains_entry({'data': ['$1Ab_', '$_2Ab', '$aB_4']})

    def test_json_array_11(self):
        assert_that(self.process(json_array, '["string", -5, .123, {}, [], true, false, null, $1Ab_]')) \
            .contains_only('data') \
            .contains_entry({'data': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']})

    def test_json_elements_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_elements, '~other~') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_json_elements_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_elements, '') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_json_elements_2(self):
        assert_that(self.process(json_elements, '\'\', \'string\', "", "string"')) \
            .contains_only('data') \
            .contains_entry({'data': ['', 'string', '', 'string']})

    def test_json_elements_3(self):
        assert_that(self.process(json_elements, '0, 5, -5')) \
            .contains_only('data') \
            .contains_entry({'data': [0, 5, -5]})

    def test_json_elements_4(self):
        assert_that(self.process(json_elements, '.123, 1.0E-2, -5.0')) \
            .contains_only('data') \
            .contains_entry({'data': [0.123, 1.0E-2, -5.0]})

    def test_json_elements_5(self):
        assert_that(self.process(json_elements, '{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}')) \
            .contains_only('data') \
            .contains_entry({'data': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]})

    def test_json_elements_6(self):
        assert_that(self.process(json_elements, '[], [5, .123, {"key": [true, false]}, [true], false, null, $v]')) \
            .contains_only('data') \
            .contains_entry({'data': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]})

    def test_json_elements_7(self):
        assert_that(self.process(json_elements, 'TRUE, True, true')) \
            .contains_only('data') \
            .contains_entry({'data': [True, True, True]})

    def test_json_elements_8(self):
        assert_that(self.process(json_elements, 'FALSE, False, false')) \
            .contains_only('data') \
            .contains_entry({'data': [False, False, False]})

    def test_json_elements_9(self):
        assert_that(self.process(json_elements, 'NULL, Null, null')) \
            .contains_only('data') \
            .contains_entry({'data': [None, None, None]})

    def test_json_elements_10(self):
        assert_that(self.process(json_elements, '$1Ab_, $_2Ab, $aB_4')) \
            .contains_only('data') \
            .contains_entry({'data': ['$1Ab_', '$_2Ab', '$aB_4']})

    def test_json_elements_11(self):
        assert_that(self.process(json_elements, '"string", -5, .123, {}, [], true, false, null, $1Ab_')) \
            .contains_only('data') \
            .contains_entry({'data': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']})

    def test_json_true_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_true, '~other~') \
            .starts_with('Expected json_true at position')

    def test_json_true_1(self):
        assert_that(self.process(json_true, 'TRUE')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_true_2(self):
        assert_that(self.process(json_true, 'true')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_true_3(self):
        assert_that(self.process(json_true, 'True')) \
            .contains_only('data') \
            .contains_entry({'data': True})

    def test_json_false_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_false, '~other~') \
            .starts_with('Expected json_false at position')

    def test_json_false_1(self):
        assert_that(self.process(json_false, 'FALSE')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_false_2(self):
        assert_that(self.process(json_false, 'false')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_false_3(self):
        assert_that(self.process(json_false, 'False')) \
            .contains_only('data') \
            .contains_entry({'data': False})

    def test_json_null_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(json_null, '~other~') \
            .starts_with('Expected json_null at position')

    def test_json_null_1(self):
        assert_that(self.process(json_null, 'NULL')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    def test_json_null_2(self):
        assert_that(self.process(json_null, 'null')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    def test_json_null_3(self):
        assert_that(self.process(json_null, 'Null')) \
            .contains_only('data') \
            .contains_entry({'data': None})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
