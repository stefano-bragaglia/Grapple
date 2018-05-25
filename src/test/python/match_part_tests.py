from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import is_optional, match_part
from grapple.parsing.visitor import KnowledgeVisitor


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

                                                              'node': {'parameter': '$p',
                                                                       'labels': ['current'],
                                                                       'properties': {'key': 'value'}},
                                                              'chain': []}]}}})

    def test_match_part_2(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH ($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'match': {'optional': True,
                                                 'pattern': [{
                                                     'node': {'parameter': '$p',
                                                              'labels': ['current'],
                                                              'properties': {'key': 'value'}},
                                                     'chain': [{'relation': {'direction': 'any',
                                                                             'parameter': '$p',
                                                                             'types': ['current'],
                                                                             'properties': {'key': 'value'}},
                                                                'node': {'parameter': '$p',
                                                                         'labels': ['current'],
                                                                         'properties': {'key': 'value'}}}]}]}}})

    def test_match_part_3(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH $pp = ($p:current{key: "value"}), '
                                             '($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'match': {'optional': True,
                                                 'pattern': [{'parameter': '$pp',
                                                              'node': {'parameter': '$p',
                                                                       'labels': ['current'],
                                                                       'properties': {'key': 'value'}},
                                                              'chain': []},
                                                             {'node': {'parameter': '$p',
                                                                       'labels': ['current'],
                                                                       'properties': {'key': 'value'}},
                                                              'chain': [{'relation': {'direction': 'any',
                                                                                      'parameter': '$p',
                                                                                      'types': ['current'],
                                                                                      'properties': {
                                                                                          'key': 'value'}},
                                                                         'node': {'parameter': '$p',
                                                                                  'labels': ['current'],
                                                                                  'properties': {
                                                                                      'key': 'value'}}}]}]}}})

    def test_match_optional_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(is_optional, '~other~') \
            .starts_with("Expected match_optional at position")

    def test_match_optional_1(self):
        assert_that(self.process(is_optional, 'OPTIONAL')) \
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
                                                    'node': {'parameter': '$p',
                                                             'labels': ['current'],
                                                             'properties': {'key': 'value'}},
                                                    'chain': []}]}})

    def test_match_patterns_2(self):
        assert_that(self.process(match_patterns, 'MATCH ($p:current{key: "value"})'
                                                 '<-[$p:current{key: "value"}]->'
                                                 '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': [{'node': {'parameter': '$p',
                                                             'labels': ['current'],
                                                             'properties': {'key': 'value'}},
                                                    'chain': [{'relation': {'direction': 'any',
                                                                            'parameter': '$p',
                                                                            'types': ['current'],
                                                                            'properties': {'key': 'value'}},
                                                               'node': {'parameter': '$p',
                                                                        'labels': ['current'],
                                                                        'properties': {'key': 'value'}}}]
                                                    }]}})

    def test_match_patterns_3(self):
        assert_that(self.process(match_patterns, 'MATCH $pp = ($p:current{key: "value"}), '
                                                 '($p:current{key: "value"})'
                                                 '<-[$p:current{key: "value"}]->'
                                                 '($p:current{key: "value"})')) \
            .contains_only('value') \
            .contains_entry({'value': {'pattern': [{'parameter': '$pp',
                                                    'node': {'parameter': '$p',
                                                             'labels': ['current'],
                                                             'properties': {
                                                                 'key': 'value'}},
                                                    'chain': []},
                                                   {'node': {'parameter': '$p',
                                                             'labels': ['current'],
                                                             'properties': {'key': 'value'}},
                                                    'chain': [{'relation': {'direction': 'any',
                                                                            'parameter': '$p',
                                                                            'types': ['current'],
                                                                            'properties': {
                                                                                'key': 'value'}},
                                                               'node': {'parameter': '$p',
                                                                        'labels': ['current'],
                                                                        'properties': {
                                                                            'key': 'value'}}}]}]}})

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
