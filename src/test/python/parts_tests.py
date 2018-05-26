from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import create_part, delete_part, match_part, remove_part, return_part, rule_part, set_part, \
    updating_part
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_updating_part_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(updating_part, '~other~') \
            .starts_with("Expected key_create or key_remove or key_set or is_detach or key_delete at position")

    def test_updating_part_1(self):
        assert_that(self.process(updating_part, 'CREATE $pp = ($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_updating_part_2(self):
        assert_that(self.process(updating_part, 'CREATE ($p:current{key: "value"})'
                                                '<-[$p:current{key: "value"}]->'
                                                '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_updating_part_3(self):
        assert_that(self.process(updating_part, 'CREATE $pp = ($p:current{key: "value"}), '
                                                '($p:current{key: "value"})'
                                                '<-[$p:current{key: "value"}]->'
                                                '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                        },
                        {
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
                    ]
                }
            }
        })

    def test_updating_part_4(self):
        assert_that(self.process(updating_part, 'REMOVE $node :label, $rel."key"')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'remove_part': {
                    'items': [
                        {
                            'entity': '$node',
                            'flags': ['label']
                        },
                        {
                            'entity': '$rel',
                            'field': 'key'
                        }
                    ]
                }
            }
        })

    def test_updating_part_5(self):
        assert_that(self.process(updating_part, 'SET $node :label, $rel += {key: "value", num: -.123}, '
                                                '$rel = {key: "value", num: -.123}, $node."num" = -.123')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'set_part': {
                    'items': [
                        {
                            'entity': '$node',
                            'flags': ['label']
                        },
                        {
                            'function': 'replace',
                            'entity': '$rel',
                            'properties': {
                                'key': 'value',
                                'num': -0.123
                            }
                        },
                        {
                            'function': 'assign',
                            'entity': '$rel',
                            'properties': {
                                'key': 'value',
                                'num': -0.123
                            }
                        },
                        {
                            'function': 'assign',
                            'entity': '$node',
                            'field': 'num',
                            'value': -0.123
                        }
                    ]
                }
            }
        })

    def test_updating_part_6(self):
        assert_that(self.process(updating_part, 'DETACH DELETE $rel, $node')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'delete_part': {
                    'detach': True,
                    'items': [
                        {
                            'entity': '$rel'
                        },
                        {
                            'entity': '$node'
                        }
                    ]
                }
            }
        })

    def test_rule_part_99(self):
        assert_that(self.process(rule_part, 'RULE "Description"\nSALIENCE 5')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'rule_part': {
                    'description': 'Description',
                    'salience': 5
                }
            }
        })

    def test_create_part_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(create_part, '~other~') \
            .starts_with("Expected key_create at position")

    def test_create_part_1(self):
        assert_that(self.process(create_part, 'CREATE $pp = ($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_create_part_2(self):
        assert_that(self.process(create_part, 'CREATE ($p:current{key: "value"})'
                                              '<-[$p:current{key: "value"}]->'
                                              '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_create_part_3(self):
        assert_that(self.process(create_part, 'CREATE $pp = ($p:current{key: "value"}), '
                                              '($p:current{key: "value"})'
                                              '<-[$p:current{key: "value"}]->'
                                              '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'create_part': {
                    'items': [
                        {
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
                        },
                        {
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
                    ]
                }
            }
        })

    def test_delete_part_99(self):
        assert_that(self.process(delete_part, 'DETACH DELETE $rel, $node')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'delete_part': {
                    'detach': True,
                    'items': [
                        {
                            'entity': '$rel'
                        },
                        {
                            'entity': '$node'
                        }
                    ]
                }
            }
        })

    def test_match_part_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(match_part, '~other~') \
            .starts_with("Expected is_optional or key_match at position")

    def test_match_part_1(self):
        assert_that(self.process(match_part, 'MATCH $pp = ($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'match_part': {
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_match_part_2(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH ($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'match_part': {
                    'optional': True,
                    'items': [
                        {
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
                    ]
                }
            }
        })

    def test_match_part_3(self):
        assert_that(self.process(match_part, 'OPTIONAL MATCH $pp = ($p:current{key: "value"}), '
                                             '($p:current{key: "value"})'
                                             '<-[$p:current{key: "value"}]->'
                                             '($p:current{key: "value"})')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'match_part': {
                    'optional': True,
                    'items': [
                        {
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
                        },
                        {
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
                    ]
                }
            }
        })

    def test_remove_part_99(self):
        assert_that(self.process(remove_part, 'REMOVE $node :label, $rel."key"')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'remove_part': {
                    'items': [
                        {
                            'entity': '$node',
                            'flags': ['label']
                        },
                        {
                            'entity': '$rel',
                            'field': 'key'
                        }
                    ]
                }
            }
        })

    def test_set_part_99(self):
        assert_that(self.process(set_part, 'SET $node :label, $rel += {key: "value", num: -.123}, '
                                           '$rel = {key: "value", num: -.123}, $node."num" = -.123')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'set_part': {
                    'items': [
                        {
                            'entity': '$node',
                            'flags': ['label']
                        },
                        {
                            'function': 'replace',
                            'entity': '$rel',
                            'properties': {
                                'key': 'value',
                                'num': -0.123
                            }
                        },
                        {
                            'function': 'assign',
                            'entity': '$rel',
                            'properties': {
                                'key': 'value',
                                'num': -0.123
                            }
                        },
                        {
                            'function': 'assign',
                            'entity': '$node',
                            'field': 'num',
                            'value': -0.123
                        }
                    ]
                }
            }
        })

    def test_return_part_99(self):
        assert_that(self.process(return_part, 'RETURN DISTINCT *, coalesce($param.prop, 5) AS "synonym" '
                                              'ORDER BY synonym DESC SKIP 5 LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'return_part': {
                    'distinct': True,
                    'items': [
                        {
                            'function': 'all'
                        }, {
                            'function': 'coalesce',
                            'parameter': '$param',
                            'field': 'prop',
                            'value': 5,
                            'synonym': 'synonym'
                        }
                    ],
                    'order_by': [
                        {
                            'ascending': False,
                            'name': 'synonym'
                        }
                    ],
                    'skip': 5,
                    'limit': 3
                }
            }
        })

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
