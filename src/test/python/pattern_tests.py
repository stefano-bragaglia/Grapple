from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import chain, details, dir_back, dir_both, dir_next, dir_none, node, pattern, relation, \
    start, step
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_pattern_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(pattern, '~other~') \
            .starts_with("Expected entity or '(' at position")

    def test_pattern_1(self):
        assert_that(self.process(pattern, '$pp = ($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'pattern': {
                    'entity': '$pp',
                    'node': {
                        'entity': '$p',
                        'labels': ['current'],
                        'properties': {
                            'key': 'value'
                        }
                    }
                }
            }
        })

    def test_pattern_2(self):
        assert_that(self.process(pattern, '($p:current{key: "value"})'
                                          '<-[$p:current{key: "value"}]->'
                                          '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'pattern': {
                    'node': {
                        'entity': '$p',
                        'labels': ['current'],
                        'properties': {
                            'key': 'value'
                        }
                    }, 'chain': [
                        {
                            'relation': {
                                'direction': 'any',
                                'entity': '$p',
                                'types': ['current'],
                                'properties': {
                                    'key': 'value'
                                }
                            },
                            'node': {
                                'entity': '$p',
                                'labels': ['current'],
                                'properties': {
                                    'key': 'value'
                                }
                            }
                        }
                    ]
                }
            }
        })

    def test_pattern_3(self):
        assert_that(self.process(pattern, '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'pattern': {
                    'node': {
                        'entity': '$p',
                        'labels': ['current'],
                        'properties': {
                            'key': 'value'
                        }
                    }
                }
            }
        })

    def test_pattern_4(self):
        assert_that(self.process(pattern, '($p:current{key: "value"})'
                                          '<-[$p:current{key: "value"}]->'
                                          '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'pattern': {
                    'node': {
                        'entity': '$p',
                        'labels': ['current'],
                        'properties': {
                            'key': 'value'
                        }
                    },
                    'chain': [
                        {
                            'relation': {
                                'direction': 'any',
                                'entity': '$p',
                                'types': ['current'],
                                'properties': {
                                    'key': 'value'
                                }
                            },
                            'node': {
                                'entity': '$p',
                                'labels': ['current'],
                                'properties': {
                                    'key': 'value'
                                }
                            }
                        }
                    ]
                }
            }
        })

    def test_pattern_99(self):
        assert_that(
            self.process(pattern, '$path = ($n :main {name: "Stu"})-[]->()-[$r :lives {since: 1995}]-(:city)')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'pattern': {
                    'entity': '$path',
                    'node': {
                        'entity': '$n',
                        'labels': ['main'],
                        'properties': {
                            'name': 'Stu'}
                    },
                    'chain': [
                        {
                            'relation': {
                                'direction': 'outgoing'
                            },
                            'node': {
                            },
                        },
                        {
                            'relation': {
                                'direction': 'any',
                                'entity': '$r',
                                'types': ['lives'],
                                'properties': {'since': 1995}
                            },
                            'node': {
                                'labels': ['city']
                            }
                        }
                    ]
                }
            }
        })

    def test_start_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(start, '~other~') \
            .starts_with("Expected '(' at position")

    def test_start_1(self):
        assert_that(self.process(start, '()')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {}}})

    def test_start_2(self):
        assert_that(self.process(start, '($p)')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'entity': '$p'}}})

    def test_start_3(self):
        assert_that(self.process(start, '(:current)')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'labels': ['current']}}})

    def test_start_4(self):
        assert_that(self.process(start, '({key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'properties': {'key': 'value'}}}})

    def test_start_5(self):
        assert_that(self.process(start, '($p:current)')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'entity': '$p', 'labels': ['current']}}})

    def test_start_6(self):
        assert_that(self.process(start, '($p{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'entity': '$p', 'properties': {'key': 'value'}}}})

    def test_start_7(self):
        assert_that(self.process(start, '(:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'labels': ['current'], 'properties': {'key': 'value'}}}})

    def test_start_8(self):
        assert_that(self.process(start, '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'node': {'entity': '$p', 'labels': ['current'],
                                               'properties': {'key': 'value'}}}})

    def test_chain_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(chain, '~other~') \
            .starts_with("Expected '<-' or '<-' or '-' or '-' at position")

    def test_chain_1(self):
        assert_that(self.process(chain, '<-[$p:current{key: "value"}]->($p:main{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'chain': [
            {
                'relation': {'direction': 'any', 'entity': '$p',
                             'types': ['current'], 'properties': {'key': 'value'}},
                'node': {'entity': '$p', 'labels': ['main'], 'properties': {'key': 'value'}}
            },
        ]}})

    def test_chain_2(self):
        assert_that(self.process(chain, '--()<-[$p:current{key: "value"}]->($p:main{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'chain': [
            {
                'relation': {'direction': 'any'},
                'node': {}
            }, {
                'relation': {'direction': 'any', 'entity': '$p',
                             'types': ['current'], 'properties': {'key': 'value'}},
                'node': {'entity': '$p', 'labels': ['main'], 'properties': {'key': 'value'}}
            }
        ]}})

    def test_step_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(step, '~other~') \
            .starts_with("Expected '<-' or '<-' or '-' or '-' at position")

    def test_step_1(self):
        assert_that(self.process(step, '<-[$p:current{key: "value"}]->($p:main{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'relation': {'direction': 'any', 'entity': '$p', 'types': ['current'],
                                                   'properties': {'key': 'value'}},
                                      'node': {'entity': '$p', 'labels': ['main'],
                                               'properties': {'key': 'value'}}}})

    def test_node_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(node, '~other~') \
            .starts_with("Expected '(' at position")

    def test_node_1(self):
        assert_that(self.process(node, '()')) \
            .contains_only('data') \
            .contains_entry({'data': {}})

    def test_node_2(self):
        assert_that(self.process(node, '($p)')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p'}})

    def test_node_3(self):
        assert_that(self.process(node, '(:current)')) \
            .contains_only('data') \
            .contains_entry({'data': {'labels': ['current']}})

    def test_node_4(self):
        assert_that(self.process(node, '({key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'properties': {'key': 'value'}}})

    def test_node_5(self):
        assert_that(self.process(node, '($p:current)')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'labels': ['current']}})

    def test_node_6(self):
        assert_that(self.process(node, '($p{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'properties': {'key': 'value'}}})

    def test_node_7(self):
        assert_that(self.process(node, '(:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'labels': ['current'], 'properties': {'key': 'value'}}})

    def test_node_8(self):
        assert_that(self.process(node, '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'labels': ['current'],
                                      'properties': {'key': 'value'}}})

    def test_relation_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(relation, '~other~') \
            .starts_with("Expected '<-' or '<-' or '-' or '-' at position")

    def test_relation_1(self):
        assert_that(self.process(relation, '<-[$p:current{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p',
                                      'types': ['current'], 'properties': {'key': 'value'}}})

    def test_relation_2(self):
        assert_that(self.process(relation, '<-[$p:current{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'entity': '$p',
                                      'types': ['current'], 'properties': {'key': 'value'}}})

    def test_relation_3(self):
        assert_that(self.process(relation, '-[$p:current{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'entity': '$p',
                                      'types': ['current'], 'properties': {'key': 'value'}}})

    def test_relation_4(self):
        assert_that(self.process(relation, '-[$p:current{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p',
                                      'types': ['current'], 'properties': {'key': 'value'}}})

    def test_dir_both_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(dir_both, '~other~') \
            .starts_with("Expected '<-' at position")

    def test_dir_both_1(self):
        assert_that(self.process(dir_both, '<-->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any'}})

    def test_dir_both_2(self):
        assert_that(self.process(dir_both, '<-[]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any'}})

    def test_dir_both_3(self):
        assert_that(self.process(dir_both, '<-[$p]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p'}})

    def test_dir_both_4(self):
        assert_that(self.process(dir_both, '<-[:current]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'types': ['current']}})

    def test_dir_both_5(self):
        assert_that(self.process(dir_both, '<-[{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'properties': {'key': 'value'}}})

    def test_dir_both_6(self):
        assert_that(self.process(dir_both, '<-[$p:current]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p', 'types': ['current']}})

    def test_dir_both_7(self):
        assert_that(self.process(dir_both, '<-[$p{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p', 'properties': {'key': 'value'}}})

    def test_dir_both_8(self):
        assert_that(self.process(dir_both, '<-[$p:current{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'direction': 'any', 'entity': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    def test_dir_back_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(dir_back, '~other~') \
            .starts_with("Expected '<-' at position")

    def test_dir_back_1(self):
        assert_that(self.process(dir_back, '<--')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming'}})

    def test_dir_back_2(self):
        assert_that(self.process(dir_back, '<-[]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming'}})

    def test_dir_back_3(self):
        assert_that(self.process(dir_back, '<-[$p]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'entity': '$p'}})

    def test_dir_back_4(self):
        assert_that(self.process(dir_back, '<-[:current]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'types': ['current']}})

    def test_dir_back_5(self):
        assert_that(self.process(dir_back, '<-[{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'properties': {'key': 'value'}}})

    def test_dir_back_6(self):
        assert_that(self.process(dir_back, '<-[$p:current]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'entity': '$p', 'types': ['current']}})

    def test_dir_back_7(self):
        assert_that(self.process(dir_back, '<-[$p{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'incoming', 'entity': '$p', 'properties': {'key': 'value'}}})

    def test_dir_back_8(self):
        assert_that(self.process(dir_back, '<-[$p:current{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'direction': 'incoming', 'entity': '$p', 'types': ['current'],
                      'properties': {'key': 'value'}}})

    def test_dir_next_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(dir_next, '~other~') \
            .starts_with("Expected '-' at position")

    def test_dir_next_1(self):
        assert_that(self.process(dir_next, '-->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing'}})

    def test_dir_next_2(self):
        assert_that(self.process(dir_next, '-[]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing'}})

    def test_dir_next_3(self):
        assert_that(self.process(dir_next, '-[$p]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'entity': '$p'}})

    def test_dir_next_4(self):
        assert_that(self.process(dir_next, '-[:current]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'types': ['current']}})

    def test_dir_next_5(self):
        assert_that(self.process(dir_next, '-[{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'properties': {'key': 'value'}}})

    def test_dir_next_6(self):
        assert_that(self.process(dir_next, '-[$p:current]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'entity': '$p', 'types': ['current']}})

    def test_dir_next_7(self):
        assert_that(self.process(dir_next, '-[$p{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'outgoing', 'entity': '$p', 'properties': {'key': 'value'}}})

    def test_dir_next_8(self):
        assert_that(self.process(dir_next, '-[$p:current{key: "value"}]->')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'direction': 'outgoing', 'entity': '$p', 'types': ['current'],
                      'properties': {'key': 'value'}}})

    def test_dir_none_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(dir_none, '~other~') \
            .starts_with("Expected '-' at position")

    def test_dir_none_1(self):
        assert_that(self.process(dir_none, '--')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any'}})

    def test_dir_none_2(self):
        assert_that(self.process(dir_none, '-[]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any'}})

    def test_dir_none_3(self):
        assert_that(self.process(dir_none, '-[$p]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p'}})

    def test_dir_none_4(self):
        assert_that(self.process(dir_none, '-[:current]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'types': ['current']}})

    def test_dir_none_5(self):
        assert_that(self.process(dir_none, '-[{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'properties': {'key': 'value'}}})

    def test_dir_none_6(self):
        assert_that(self.process(dir_none, '-[$p:current]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p', 'types': ['current']}})

    def test_dir_none_7(self):
        assert_that(self.process(dir_none, '-[$p{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry({'data': {'direction': 'any', 'entity': '$p', 'properties': {'key': 'value'}}})

    def test_dir_none_8(self):
        assert_that(self.process(dir_none, '-[$p:current{key: "value"}]-')) \
            .contains_only('data') \
            .contains_entry(
            {'data': {'direction': 'any', 'entity': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    def test_details_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(details, '~other~') \
            .starts_with("Expected '[' at position")

    def test_details_1(self):
        assert_that(self.process(details, '[]')) \
            .contains_only('data') \
            .contains_entry({'data': {}})

    def test_details_2(self):
        assert_that(self.process(details, '[$p]')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p'}})

    def test_details_3(self):
        assert_that(self.process(details, '[:current]')) \
            .contains_only('data') \
            .contains_entry({'data': {'types': ['current']}})

    def test_details_4(self):
        assert_that(self.process(details, '[{key: "value"}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'properties': {'key': 'value'}}})

    def test_details_5(self):
        assert_that(self.process(details, '[$p:current]')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'types': ['current']}})

    def test_details_6(self):
        assert_that(self.process(details, '[$p{key: "value"}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'properties': {'key': 'value'}}})

    def test_details_7(self):
        assert_that(self.process(details, '[:current{key: "value"}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'types': ['current'], 'properties': {'key': 'value'}}})

    def test_details_8(self):
        assert_that(self.process(details, '[$p:current{key: "value"}]')) \
            .contains_only('data') \
            .contains_entry({'data': {'entity': '$p', 'types': ['current'], 'properties': {'key': 'value'}}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
