from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grammar import match_anonymous, match_back, match_both, match_chain, match_details, match_labels, match_next, \
    match_node, match_none, match_optional, match_part, match_pattern, match_patterns, match_properties, match_relation, \
    match_start, match_types
from visitor import KnowledgeVisitor


class TestGrammarVisitor(TestCase):
    def test_match_part_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_part, '~other~') \
            .starts_with("Expected match_optional or key_match at position")

    def test_match_part_1(self):
        assert_that(self.process(match_part, 'MATCH $pp = ($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'match': {'optional': False,
                                                 'pattern': [{'parameter': '$pp',
                                                              'pattern': {
                                                                  'start': {'node': {'parameter': '$p',
                                                                                     'labels': ['current'],
                                                                                     'properties': {'key': 'value'}}},
                                                                  'chain': []}}]}}})

    def test_match_part_2(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH ($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'match': {'optional': True,
                                                 'pattern': [{'pattern': {
                                                     'start': {'node': {'parameter': '$p',
                                                                        'labels': ['current'],
                                                                        'properties': {'key': 'value'}}},
                                                     'chain': [{'relation': {'direction': 'any',
                                                                             'parameter': '$p',
                                                                             'types': ['current'],
                                                                             'properties': {'key': 'value'}},
                                                                'node': {'parameter': '$p',
                                                                         'labels': ['current'],
                                                                         'properties': {'key': 'value'}}}]}}]}}})

    def test_match_part_3(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH $pp = ($p:current{key: "value"}), '
                                             '($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'match': {'optional': True,
                                                 'pattern': [{'parameter': '$pp',
                                                              'pattern': {
                                                                  'start': {'node': {'parameter': '$p',
                                                                                     'labels': ['current'],
                                                                                     'properties': {'key': 'value'}}},
                                                                  'chain': []}},
                                                             {'pattern': {
                                                                 'start': {'node': {'parameter': '$p',
                                                                                    'labels': ['current'],
                                                                                    'properties': {'key': 'value'}}},
                                                                 'chain': [{'relation': {'direction': 'any',
                                                                                         'parameter': '$p',
                                                                                         'types': ['current'],
                                                                                         'properties': {
                                                                                             'key': 'value'}},
                                                                            'node': {'parameter': '$p',
                                                                                     'labels': ['current'],
                                                                                     'properties': {
                                                                                         'key': 'value'}}}]}}]}}})

    def test_match_optional_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_optional, '~other~') \
            .starts_with("Expected match_optional at position")

    def test_match_optional_1(self):
        assert_that(self.process(match_optional, 'OPTIONAL')) \
            .contains_only('value') \
            .contains_entry({'value': {'optional': True}})

    def test_match_patterns_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_patterns, '~other~') \
            .starts_with("Expected key_match at position")

    def test_match_patterns_1(self):
        assert_that(self.process(match_patterns, 'MATCH $pp = ($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': [{'parameter': '$pp',
                                                    'pattern': {'start': {'node': {'parameter': '$p',
                                                                                   'labels': ['current'],
                                                                                   'properties': {'key': 'value'}}},
                                                                'chain': []}}]}})

    def test_match_patterns_2(self):
        assert_that(self.process(match_patterns, 'MATCH ($p:current{key: "value"})'
                                                 '<-[$p:current{key: "value"}]->'
                                                 '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': [{'pattern': {'start': {'node': {'parameter': '$p',
                                                                                   'labels': ['current'],
                                                                                   'properties': {'key': 'value'}}},
                                                                'chain': [{'relation': {'direction': 'any',
                                                                                        'parameter': '$p',
                                                                                        'types': ['current'],
                                                                                        'properties': {'key': 'value'}},
                                                                           'node': {'parameter': '$p',
                                                                                    'labels': ['current'],
                                                                                    'properties': {'key': 'value'}}}]
                                                                }}]}})

    def test_match_patterns_3(self):
        assert_that(self.process(match_patterns, 'MATCH $pp = ($p:current{key: "value"}), '
                                                 '($p:current{key: "value"})'
                                                 '<-[$p:current{key: "value"}]->'
                                                 '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': [{'parameter': '$pp',
                                                    'pattern': {'start': {'node': {'parameter': '$p',
                                                                                   'labels': ['current'],
                                                                                   'properties': {'key': 'value'}}},
                                                                'chain': []}},
                                                   {'pattern': {'start': {'node': {'parameter': '$p',
                                                                                   'labels': ['current'],
                                                                                   'properties': {'key': 'value'}}},
                                                                'chain': [{'relation': {'direction': 'any',
                                                                                        'parameter': '$p',
                                                                                        'types': ['current'],
                                                                                        'properties': {'key': 'value'}},
                                                                           'node': {'parameter': '$p',
                                                                                    'labels': ['current'],
                                                                                    'properties': {'key': 'value'}}}]}}]
                                       }})

    def test_match_pattern_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_pattern, '~other~') \
            .starts_with("Expected return_parameter or '(' at position")

    def test_match_pattern_1(self):
        assert_that(self.process(match_pattern, '$pp = ($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$pp',
                                       'pattern': {'start': {'node': {'parameter': '$p', 'labels': ['current'],
                                                                      'properties': {'key': 'value'}}},
                                                   'chain': []}}})

    def test_match_pattern_2(self):
        assert_that(self.process(match_pattern, '($p:current{key: "value"})'
                                                '<-[$p:current{key: "value"}]->'
                                                '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': {'start': {'node': {'parameter': '$p', 'labels': ['current'],
                                                                      'properties': {'key': 'value'}}},
                                                   'chain': [
                                                       {'relation': {'direction': 'any',
                                                                     'parameter': '$p',
                                                                     'types': ['current'],
                                                                     'properties': {'key': 'value'}},
                                                        'node': {'parameter': '$p',
                                                                 'labels': ['current'],
                                                                 'properties': {'key': 'value'}}}
                                                   ]}}})

    def test_match_anonymous_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_anonymous, '~other~') \
            .starts_with("Expected '(' at position")

    def test_match_anonymous_1(self):
        assert_that(self.process(match_anonymous, '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': {'start': {'node': {'parameter': '$p', 'labels': ['current'],
                                                                      'properties': {'key': 'value'}}},
                                                   'chain': []}}})

    def test_match_anonymous_2(self):
        assert_that(self.process(match_anonymous, '($p:current{key: "value"})'
                                                  '<-[$p:current{key: "value"}]->'
                                                  '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': {'start': {'node': {'parameter': '$p', 'labels': ['current'],
                                                                      'properties': {'key': 'value'}}},
                                                   'chain': [
                                                       {'relation': {'direction': 'any',
                                                                     'parameter': '$p',
                                                                     'types': ['current'],
                                                                     'properties': {'key': 'value'}},
                                                        'node': {'parameter': '$p',
                                                                 'labels': ['current'],
                                                                 'properties': {'key': 'value'}}}
                                                   ]}}})

    def test_match_start_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_start, '~other~') \
            .starts_with("Expected '(' at position")

    def test_return_start_1(self):
        assert_that(self.process(match_start, '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'parameter': '$p', 'labels': ['current'],
                                                'properties': {'key': 'value'}}}})

    def test_match_chain_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_chain, '~other~') \
            .starts_with("Expected '<-' or '<-' or '-' or '-' at position")

    def test_return_chain_1(self):
        assert_that(self.process(match_chain, '<-[$p:current{key: "value"}]->($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'relation': {'direction': 'any', 'parameter': '$p', 'types': ['current'],
                                                    'properties': {'key': 'value'}},
                                       'node': {'parameter': '$p', 'labels': ['current'],
                                                'properties': {'key': 'value'}}}})

    def test_match_node_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_node, '~other~') \
            .starts_with("Expected '(' at position")

    def test_return_node_1(self):
        assert_that(self.process(match_node, '()')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {}}})

    def test_return_node_2(self):
        assert_that(self.process(match_node, '($p)')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'parameter': '$p'}}})

    def test_return_node_3(self):
        assert_that(self.process(match_node, '(:current)')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'labels': ['current']}}})

    def test_return_node_4(self):
        assert_that(self.process(match_node, '({key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'properties': {'key': 'value'}}}})

    def test_return_node_5(self):
        assert_that(self.process(match_node, '($p:current)')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'parameter': '$p', 'labels': ['current']}}})

    def test_return_node_6(self):
        assert_that(self.process(match_node, '($p{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'parameter': '$p', 'properties': {'key': 'value'}}}})

    def test_return_node_7(self):
        assert_that(self.process(match_node, '(:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'labels': ['current'], 'properties': {'key': 'value'}}}})

    def test_return_node_8(self):
        assert_that(self.process(match_node, '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'node': {'parameter': '$p', 'labels': ['current'],
                                                'properties': {'key': 'value'}}}})

    def test_match_relation_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_relation, '~other~') \
            .starts_with("Expected '<-' or '<-' or '-' or '-' at position")

    def test_return_relation_1(self):
        assert_that(self.process(match_relation, '<-[$p:current{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'relation': {'direction': 'any', 'parameter': '$p', 'types': ['current'],
                                                    'properties': {'key': 'value'}}}})

    def test_return_relation_2(self):
        assert_that(self.process(match_relation, '<-[$p:current{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'relation': {'direction': 'incoming', 'parameter': '$p', 'types': ['current'],
                                                    'properties': {'key': 'value'}}}})

    def test_return_relation_3(self):
        assert_that(self.process(match_relation, '-[$p:current{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'relation': {'direction': 'outgoing', 'parameter': '$p', 'types': ['current'],
                                                    'properties': {'key': 'value'}}}})

    def test_return_relation_4(self):
        assert_that(self.process(match_relation, '-[$p:current{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'relation': {'direction': 'any', 'parameter': '$p', 'types': ['current'],
                                                    'properties': {'key': 'value'}}}})

    def test_match_both_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_both, '~other~') \
            .starts_with("Expected '<-' at position")

    def test_return_both_1(self):
        assert_that(self.process(match_both, '<-->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any'}})

    def test_return_both_2(self):
        assert_that(self.process(match_both, '<-[]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any'}})

    def test_return_both_3(self):
        assert_that(self.process(match_both, '<-[$p]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p'}})

    def test_return_both_4(self):
        assert_that(self.process(match_both, '<-[:current]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'types': ['current']}})

    def test_return_both_5(self):
        assert_that(self.process(match_both, '<-[{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'properties': {'key': 'value'}}})

    def test_return_both_6(self):
        assert_that(self.process(match_both, '<-[$p:current]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p', 'types': ['current']}})

    def test_return_both_7(self):
        assert_that(self.process(match_both, '<-[$p{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p', 'properties': {'key': 'value'}}})

    def test_return_both_8(self):
        assert_that(self.process(match_both, '<-[$p:current{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry(
            {'value': {'direction': 'any', 'parameter': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    def test_match_back_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_back, '~other~') \
            .starts_with("Expected '<-' at position")

    def test_return_back_1(self):
        assert_that(self.process(match_back, '<--')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming'}})

    def test_return_back_2(self):
        assert_that(self.process(match_back, '<-[]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming'}})

    def test_return_back_3(self):
        assert_that(self.process(match_back, '<-[$p]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming', 'parameter': '$p'}})

    def test_return_back_4(self):
        assert_that(self.process(match_back, '<-[:current]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming', 'types': ['current']}})

    def test_return_back_5(self):
        assert_that(self.process(match_back, '<-[{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming', 'properties': {'key': 'value'}}})

    def test_return_back_6(self):
        assert_that(self.process(match_back, '<-[$p:current]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming', 'parameter': '$p', 'types': ['current']}})

    def test_return_back_7(self):
        assert_that(self.process(match_back, '<-[$p{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'incoming', 'parameter': '$p', 'properties': {'key': 'value'}}})

    def test_return_back_8(self):
        assert_that(self.process(match_back, '<-[$p:current{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry(
            {'value': {'direction': 'incoming', 'parameter': '$p', 'types': ['current'],
                       'properties': {'key': 'value'}}})

    def test_match_next_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_next, '~other~') \
            .starts_with("Expected '-' at position")

    def test_return_next_1(self):
        assert_that(self.process(match_next, '-->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing'}})

    def test_return_next_2(self):
        assert_that(self.process(match_next, '-[]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing'}})

    def test_return_next_3(self):
        assert_that(self.process(match_next, '-[$p]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing', 'parameter': '$p'}})

    def test_return_next_4(self):
        assert_that(self.process(match_next, '-[:current]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing', 'types': ['current']}})

    def test_return_next_5(self):
        assert_that(self.process(match_next, '-[{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing', 'properties': {'key': 'value'}}})

    def test_return_next_6(self):
        assert_that(self.process(match_next, '-[$p:current]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing', 'parameter': '$p', 'types': ['current']}})

    def test_return_next_7(self):
        assert_that(self.process(match_next, '-[$p{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'outgoing', 'parameter': '$p', 'properties': {'key': 'value'}}})

    def test_return_next_8(self):
        assert_that(self.process(match_next, '-[$p:current{key: "value"}]->')) \
            .contains_only('value') \
            .contains_entry(
            {'value': {'direction': 'outgoing', 'parameter': '$p', 'types': ['current'],
                       'properties': {'key': 'value'}}})

    def test_match_none_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_none, '~other~') \
            .starts_with("Expected '-' at position")

    def test_return_none_1(self):
        assert_that(self.process(match_none, '--')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any'}})

    def test_return_none_2(self):
        assert_that(self.process(match_none, '-[]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any'}})

    def test_return_none_3(self):
        assert_that(self.process(match_none, '-[$p]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p'}})

    def test_return_none_4(self):
        assert_that(self.process(match_none, '-[:current]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'types': ['current']}})

    def test_return_none_5(self):
        assert_that(self.process(match_none, '-[{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'properties': {'key': 'value'}}})

    def test_return_none_6(self):
        assert_that(self.process(match_none, '-[$p:current]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p', 'types': ['current']}})

    def test_return_none_7(self):
        assert_that(self.process(match_none, '-[$p{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry({'value': {'direction': 'any', 'parameter': '$p', 'properties': {'key': 'value'}}})

    def test_return_none_8(self):
        assert_that(self.process(match_none, '-[$p:current{key: "value"}]-')) \
            .contains_only('value') \
            .contains_entry(
            {'value': {'direction': 'any', 'parameter': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    def test_match_details_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_details, '~other~') \
            .starts_with("Expected '[' at position")

    def test_return_details_1(self):
        assert_that(self.process(match_details, '[]')) \
            .contains_only('value') \
            .contains_entry({'value': {}})

    def test_return_details_2(self):
        assert_that(self.process(match_details, '[$p]')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$p'}})

    def test_return_details_3(self):
        assert_that(self.process(match_details, '[:current]')) \
            .contains_only('value') \
            .contains_entry({'value': {'types': ['current']}})

    def test_return_details_4(self):
        assert_that(self.process(match_details, '[{key: "value"}]')) \
            .contains_only('value') \
            .contains_entry({'value': {'properties': {'key': 'value'}}})

    def test_return_details_5(self):
        assert_that(self.process(match_details, '[$p:current]')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$p', 'types': ['current']}})

    def test_return_details_6(self):
        assert_that(self.process(match_details, '[$p{key: "value"}]')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$p', 'properties': {'key': 'value'}}})

    def test_return_details_7(self):
        assert_that(self.process(match_details, '[:current{key: "value"}]')) \
            .contains_only('value') \
            .contains_entry({'value': {'types': ['current'], 'properties': {'key': 'value'}}})

    def test_return_details_8(self):
        assert_that(self.process(match_details, '[$p:current{key: "value"}]')) \
            .contains_only('value') \
            .contains_entry({'value': {'parameter': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    def test_match_properties_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_properties, '~other~') \
            .starts_with("Expected '{' at position")

    def test_return_properties_1(self):
        assert_that(self.process(match_properties, '{}')) \
            .contains_only('value') \
            .contains_entry({'value': {'properties': {}}})

    def test_match_labels_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_labels, '~other~') \
            .starts_with("Expected ':' at position")

    def test_match_labels_1(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_labels, '') \
            .starts_with("Expected ':' at position")

    def test_return_labels_2(self):
        assert_that(self.process(match_labels, ':main:person')) \
            .contains_only('value') \
            .contains_entry({'value': {'labels': ['main', 'person']}})

    def test_return_labels_3(self):
        assert_that(self.process(match_labels, ':main')) \
            .contains_only('value') \
            .contains_entry({'value': {'labels': ['main']}})

    def test_match_types_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_types, '~other~') \
            .starts_with("Expected ':' at position")

    def test_match_types_1(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(match_types, '') \
            .starts_with("Expected ':' at position")

    def test_return_types_2(self):
        assert_that(self.process(match_types, ':main:person')) \
            .contains_only('value') \
            .contains_entry({'value': {'types': ['main', 'person']}})

    def test_return_types_3(self):
        assert_that(self.process(match_types, ':main')) \
            .contains_only('value') \
            .contains_entry({'value': {'types': ['main']}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
