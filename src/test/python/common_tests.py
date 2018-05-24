from unittest import TestCase

from arpeggio import NoMatch, ParserPython, SemanticError, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import asc, desc, description, entity, field, flag, identifier, is_detach, \
    is_distinct, is_optional, labels, limit, name, parameter, properties, salience, skip, synonym, types, \
    value, variable
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_asc_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(asc, '~other~') \
            .starts_with('Expected key_asc or key_ascending at position')

    def test_asc_1(self):
        assert_that(self.process(asc, 'ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_asc_2(self):
        assert_that(self.process(asc, 'asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_asc_3(self):
        assert_that(self.process(asc, 'Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_asc_4(self):
        assert_that(self.process(asc, 'ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_asc_5(self):
        assert_that(self.process(asc, 'ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_asc_6(self):
        assert_that(self.process(asc, 'Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': True}})

    def test_desc_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(desc, '~other~') \
            .starts_with('Expected key_desc or key_descending at position')

    def test_desc_1(self):
        assert_that(self.process(desc, 'DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_desc_2(self):
        assert_that(self.process(desc, 'desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_desc_3(self):
        assert_that(self.process(desc, 'Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_desc_4(self):
        assert_that(self.process(desc, 'DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_desc_5(self):
        assert_that(self.process(desc, 'descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_desc_6(self):
        assert_that(self.process(desc, 'Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'ascending': False}})

    def test_description_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(description, '~other~') \
            .starts_with('Expected key_rule at position')

    def test_description_1(self):
        assert_that(self.process(description, 'RULE')) \
            .contains_only('data') \
            .contains_entry({'data': {'description': None}})

    def test_description_2(self):
        assert_that(self.process(description, 'RULE "desc"')) \
            .contains_only('data') \
            .contains_entry({'data': {'description': 'desc'}})

    def test_description_3(self):
        assert_that(self.process(description, "RULE 'desc'")) \
            .contains_only('data') \
            .contains_entry({'data': {'description': 'desc'}})

    def test_entity_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(entity, '~other~') \
            .starts_with('Expected entity at position')

    def test_entity_1(self):
        assert_that(self.process(entity, '$1Ab_')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$1Ab_'}})

    def test_entity_2(self):
        assert_that(self.process(entity, '$Ab_4')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$Ab_4'}})

    def test_entity_3(self):
        assert_that(self.process(entity, '$aB_4')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$aB_4'}})

    def test_entity_4(self):
        assert_that(self.process(entity, '$_2Ab')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$_2Ab'}})

    def test_field_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(field, '~other~') \
            .starts_with("Expected '.' at position")

    def test_field_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(field, '.') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_field_2(self):
        assert_that(self.process(field, '.field')) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_field_3(self):
        assert_that(self.process(field, '. field')) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_field_4(self):
        assert_that(self.process(field, '."field"')) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_field_5(self):
        assert_that(self.process(field, '. "field"')) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_field_6(self):
        assert_that(self.process(field, ".'field'")) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_field_7(self):
        assert_that(self.process(field, ". 'field'")) \
            .contains_only('data') \
            .contains_entry({'data': {'field': 'field'}})

    def test_flag_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(flag, '~other~') \
            .starts_with("Expected ':' at position")

    def test_flag_1(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(flag, ':') \
            .starts_with("Expected identifier at position")

    def test_flag_2(self):
        assert_that(self.process(flag, ':flag')) \
            .contains_only('data') \
            .contains_entry({'data': {'flag': 'flag'}})

    def test_flag_3(self):
        assert_that(self.process(flag, ': flag')) \
            .contains_only('data') \
            .contains_entry({'data': {'flag': 'flag'}})

    def test_is_detach_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(is_detach, '~other~') \
            .starts_with("Expected is_detach at position")

    def test_is_detach_1(self):
        assert_that(self.process(is_detach, 'DETACH')) \
            .contains_only('data') \
            .contains_entry({'data': {'detach': True}})

    def test_is_detach_2(self):
        assert_that(self.process(is_detach, 'detach')) \
            .contains_only('data') \
            .contains_entry({'data': {'detach': True}})

    def test_is_detach_3(self):
        assert_that(self.process(is_detach, 'Detach')) \
            .contains_only('data') \
            .contains_entry({'data': {'detach': True}})

    def test_is_distinct_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(is_distinct, '~other~') \
            .starts_with("Expected is_distinct at position")

    def test_is_distinct_1(self):
        assert_that(self.process(is_distinct, 'DISTINCT')) \
            .contains_only('data') \
            .contains_entry({'data': {'distinct': True}})

    def test_is_distinct_2(self):
        assert_that(self.process(is_distinct, 'distinct')) \
            .contains_only('data') \
            .contains_entry({'data': {'distinct': True}})

    def test_is_distinct_3(self):
        assert_that(self.process(is_distinct, 'Distinct')) \
            .contains_only('data') \
            .contains_entry({'data': {'distinct': True}})

    def test_is_optional_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(is_optional, '~other~') \
            .starts_with("Expected is_optional at position")

    def test_is_optional_1(self):
        assert_that(self.process(is_optional, 'OPTIONAL')) \
            .contains_only('data') \
            .contains_entry({'data': {'optional': True}})

    def test_is_optional_2(self):
        assert_that(self.process(is_optional, 'optional')) \
            .contains_only('data') \
            .contains_entry({'data': {'optional': True}})

    def test_is_optional_3(self):
        assert_that(self.process(is_optional, 'Optional')) \
            .contains_only('data') \
            .contains_entry({'data': {'optional': True}})

    def test_labels_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(labels, '~other~') \
            .starts_with("Expected ':' at position")

    def test_labels_1(self):
        assert_that(self.process(labels, ':flag1')) \
            .contains_only('data') \
            .contains_entry({'data': {'labels': ['flag1']}})

    def test_labels_2(self):
        assert_that(self.process(labels, ':flag1:flag2')) \
            .contains_only('data') \
            .contains_entry({'data': {'labels': ['flag1', 'flag2']}})

    def test_labels_3(self):
        assert_that(self.process(labels, ':flag1 :flag2 :flag3')) \
            .contains_only('data') \
            .contains_entry({'data': {'labels': ['flag1', 'flag2', 'flag3']}})

    def test_return_limit_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(limit, '~other~') \
            .starts_with('Expected key_limit at position')

    def test_return_limit_1(self):
        assert_that(self.process(limit, 'limit 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 0}})

    def test_return_limit_2(self):
        assert_that(self.process(limit, 'limit 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 5}})

    def test_return_limit_3(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(limit, 'limit -5') \
            .starts_with("\"'limit' expected to be non-negative\"")

    def test_return_limit_4(self):
        assert_that(self.process(limit, 'limit 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 0}})

    def test_return_limit_5(self):
        assert_that(self.process(limit, 'limit 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 5}})

    def test_return_limit_6(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(limit, 'limit -5') \
            .starts_with("\"'limit' expected to be non-negative\"")

    def test_return_limit_7(self):
        assert_that(self.process(limit, 'limit 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 0}})

    def test_return_limit_8(self):
        assert_that(self.process(limit, 'limit 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'limit': 5}})

    def test_return_limit_9(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(limit, 'limit -5') \
            .starts_with("\"'limit' expected to be non-negative\"")

    def test_name_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(name, '~other~') \
            .starts_with("Expected ''' or '\"' or identifier at position")

    def test_name_1(self):
        assert_that(self.process(name, 'value')) \
            .contains_only('data') \
            .contains_entry({'data': {'name': 'value'}})

    def test_name_2(self):
        assert_that(self.process(name, '"value"')) \
            .contains_only('data') \
            .contains_entry({'data': {'name': 'value'}})

    def test_name_3(self):
        assert_that(self.process(name, "'value'")) \
            .contains_only('data') \
            .contains_entry({'data': {'name': 'value'}})

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

    def test_properties_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(properties, '~other~') \
            .starts_with("Expected '{' at position")

    def test_properties_1(self):
        assert_that(self.process(properties, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {'properties': {}}})

    def test_properties_2(self):
        assert_that(self.process(properties, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                             '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'properties': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                     'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}}})

    def test_return_salience_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(salience, '~other~') \
            .starts_with('Expected key_salience at position')

    def test_return_salience_1(self):
        assert_that(self.process(salience, 'salience 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 0}})

    def test_return_salience_2(self):
        assert_that(self.process(salience, 'salience 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 5}})

    def test_return_salience_3(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(salience, 'salience -5') \
            .starts_with("\"'salience' expected to be non-negative\"")

    def test_return_salience_4(self):
        assert_that(self.process(salience, 'salience 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 0}})

    def test_return_salience_5(self):
        assert_that(self.process(salience, 'salience 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 5}})

    def test_return_salience_6(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(salience, 'salience -5') \
            .starts_with("\"'salience' expected to be non-negative\"")

    def test_return_salience_7(self):
        assert_that(self.process(salience, 'salience 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 0}})

    def test_return_salience_8(self):
        assert_that(self.process(salience, 'salience 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'salience': 5}})

    def test_return_salience_9(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(salience, 'salience -5') \
            .starts_with("\"'salience' expected to be non-negative\"")

    def test_return_skip_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(skip, '~other~') \
            .starts_with('Expected key_skip at position')

    def test_return_skip_1(self):
        assert_that(self.process(skip, 'SKIP 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 0}})

    def test_return_skip_2(self):
        assert_that(self.process(skip, 'SKIP 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 5}})

    def test_return_skip_3(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(skip, 'skip -5') \
            .starts_with("\"'skip' expected to be non-negative\"")

    def test_return_skip_4(self):
        assert_that(self.process(skip, 'skip 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 0}})

    def test_return_skip_5(self):
        assert_that(self.process(skip, 'skip 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 5}})

    def test_return_skip_6(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(skip, 'skip -5') \
            .starts_with("\"'skip' expected to be non-negative\"")

    def test_return_skip_7(self):
        assert_that(self.process(skip, 'Skip 0')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 0}})

    def test_return_skip_8(self):
        assert_that(self.process(skip, 'Skip 5')) \
            .contains_only('data') \
            .contains_entry({'data': {'skip': 5}})

    def test_return_skip_9(self):
        assert_that(self.process) \
            .raises(SemanticError) \
            .when_called_with(skip, 'Skip -5') \
            .starts_with("\"'skip' expected to be non-negative\"")

    def test_synonym_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(synonym, '~other~') \
            .starts_with("Expected key_as at position")

    def test_synonym_1(self):
        assert_that(self.process(synonym, 'AS name')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_2(self):
        assert_that(self.process(synonym, 'as name')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_3(self):
        assert_that(self.process(synonym, 'As name')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_4(self):
        assert_that(self.process(synonym, 'AS "name"')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_5(self):
        assert_that(self.process(synonym, 'as "name"')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_6(self):
        assert_that(self.process(synonym, 'As "name"')) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_7(self):
        assert_that(self.process(synonym, "AS 'name'")) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_8(self):
        assert_that(self.process(synonym, "as 'name'")) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_synonym_9(self):
        assert_that(self.process(synonym, "As 'name'")) \
            .contains_only('data') \
            .contains_entry({'data': {'synonym': 'name'}})

    def test_types_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(types, '~other~') \
            .starts_with("Expected ':' at position")

    def test_types_1(self):
        assert_that(self.process(types, ':flag1')) \
            .contains_only('data') \
            .contains_entry({'data': {'types': ['flag1']}})

    def test_types_2(self):
        assert_that(self.process(types, ':flag1:flag2')) \
            .contains_only('data') \
            .contains_entry({'data': {'types': ['flag1', 'flag2']}})

    def test_types_3(self):
        assert_that(self.process(types, ':flag1 :flag2 :flag3')) \
            .contains_only('data') \
            .contains_entry({'data': {'types': ['flag1', 'flag2', 'flag3']}})

    def test_value_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(value, '~other~') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(value, '"string') \
            .starts_with("Expected '\"' at position")

    def test_value_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(value, "'string") \
            .starts_with("Expected ''' at position")

    def test_value_03(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(value, "string'") \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_04(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(value, 'string"') \
            .starts_with("Expected ''' or '\"' or json_real or json_integer or '{' or '[' or json_true or json_false "
                         "or json_null or variable at position")

    def test_value_05(self):
        assert_that(self.process(value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ''}})

    def test_value_06(self):
        assert_that(self.process(value, '""')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ''}})

    def test_value_07(self):
        assert_that(self.process(value, '"string"')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 'string'}})

    def test_value_08(self):
        assert_that(self.process(value, "'string'")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 'string'}})

    def test_value_09(self):
        assert_that(self.process(value, '.123')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 0.123}})

    def test_value_10(self):
        assert_that(self.process(value, '1.0E-2')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 1.0E-2}})

    def test_value_11(self):
        assert_that(self.process(value, '-5.')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5.0}})

    def test_value_12(self):
        assert_that(self.process(value, '-5.0')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5.0}})

    def test_value_13(self):
        assert_that(self.process(value, '0')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 0}})

    def test_value_14(self):
        assert_that(self.process(value, '5')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': 5}})

    def test_value_15(self):
        assert_that(self.process(value, '-5')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': -5}})

    def test_value_16(self):
        assert_that(self.process(value, "{}")) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {}}})

    def test_value_17(self):
        assert_that(self.process(value, '{\'k1\': -5, "k2": .123, k3: {}, \'k4\': ["value"], '
                                        '"k5": true, k6: false, \'k7\': null, "k8": $v}')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': {'k1': -5, 'k2': 0.123, 'k3': {}, 'k4': ['value'],
                                                'k5': True, 'k6': False, 'k7': None, 'k8': '$v'}}})

    def test_value_18(self):
        assert_that(self.process(value, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': []}})

    def test_value_19(self):
        assert_that(self.process(value, '[\'\', \'string\', "", "string"]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['', 'string', '', 'string']}})

    def test_value_20(self):
        assert_that(self.process(value, '[0, 5, -5]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0, 5, -5]}})

    def test_value_21(self):
        assert_that(self.process(value, '[.123, 1.0E-2, -5.0]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [0.123, 1.0E-2, -5.0]}})

    def test_value_22(self):
        assert_that(self.process(value, '[{}, {\'k1\': 0, "k2": [.123, 1.0E-2, -5.0], k3: $v}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [{}, {'k1': 0, 'k2': [0.123, 1.0E-2, -5.0], 'k3': '$v'}]}})

    def test_value_23(self):
        assert_that(self.process(value, '[[], [5, .123, {"key": [true, false]}, [true], false, null, $v]]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [[], [5, 0.123, {"key": [True, False]}, [True], False, None, '$v']]}})

    def test_value_24(self):
        assert_that(self.process(value, '[TRUE, True, true]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [True, True, True]}})

    def test_value_25(self):
        assert_that(self.process(value, '[FALSE, False, false]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [False, False, False]}})

    def test_value_26(self):
        assert_that(self.process(value, '[NULL, Null, null]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': [None, None, None]}})

    def test_value_27(self):
        assert_that(self.process(value, '[$1Ab_, $_2Ab, $aB_4]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ['$1Ab_', '$_2Ab', '$aB_4']}})

    def test_value_28(self):
        assert_that(self.process(value, '["string", -5, .123, {}, [], true, false, null, $1Ab_]')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': ["string", -5, 0.123, {}, [], True, False, None, '$1Ab_']}})

    def test_value_29(self):
        assert_that(self.process(value, 'TRUE')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_30(self):
        assert_that(self.process(value, 'true')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_31(self):
        assert_that(self.process(value, 'True')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': True}})

    def test_value_32(self):
        assert_that(self.process(value, 'FALSE')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_33(self):
        assert_that(self.process(value, 'false')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_34(self):
        assert_that(self.process(value, 'False')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': False}})

    def test_value_35(self):
        assert_that(self.process(value, 'NULL')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

    def test_value_36(self):
        assert_that(self.process(value, 'null')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

    def test_value_37(self):
        assert_that(self.process(value, 'Null')) \
            .contains_only('data') \
            .contains_entry({'data': {'value': None}})

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

    def test_variable_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(variable, '~other~') \
            .starts_with('Expected variable at position')

    def test_variable_1(self):
        assert_that(self.process(variable, '$1Ab_')) \
            .contains_only('data') \
            .contains_entry({'data': '$1Ab_'})

    def test_variable_2(self):
        assert_that(self.process(variable, '$Ab_4')) \
            .contains_only('data') \
            .contains_entry({'data': '$Ab_4'})

    def test_variable_3(self):
        assert_that(self.process(variable, '$aB_4')) \
            .contains_only('data') \
            .contains_entry({'data': '$aB_4'})

    def test_variable_4(self):
        assert_that(self.process(variable, '$_2Ab')) \
            .contains_only('data') \
            .contains_entry({'data': '$_2Ab'})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
