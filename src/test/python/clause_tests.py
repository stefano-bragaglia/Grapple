from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.grammar import clause, clause_read, clause_update, clauses, cypher
from grapple.visitor import KnowledgeVisitor


class TestClauseParsing(TestCase):
    def test_cypher_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(cypher, '~other~') \
            .starts_with("Expected key_rule or key_rule or ';' or EOF at position")

    def test_cypher_1(self):
        assert_that(self.process(cypher, '')) \
            .contains_only('data') \
            .contains_entry({'data': []})

    def test_cypher_2(self):
        assert_that(self.process(cypher, 'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]
        })

    def test_cypher_3(self):
        assert_that(self.process(cypher, 'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3; '
                                         'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'CREATE ($a)-[:back]->($m) '
                                         'REMOVE $a.num '
                                         'SET $a += {key: 5} '
                                         'DELETE $l '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                },
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'update_part': [
                        {
                            'create_part': {
                                'patterns': [
                                    {
                                        'node': {
                                            'entity': '$a'
                                        },
                                        'chain': [
                                            {
                                                'relation': {
                                                    'direction': 'outgoing',
                                                    'types': ['back']
                                                },
                                                'node': {
                                                    'entity': '$m'
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            'remove_part': {
                                'items': [
                                    {
                                        'entity': '$a',
                                        'field': 'num'
                                    }
                                ]
                            }
                        },
                        {
                            'set_part': {
                                'items': [
                                    {
                                        'operator': '=',
                                        'entity': '$a',
                                        'properties': {
                                            'key': 5
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'delete_part': {
                                'detach': False,
                                'items': [
                                    {
                                        'entity': '$l'
                                    }
                                ]
                            }
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]
        })

    def test_cypher_4(self):
        assert_that(self.process(cypher, 'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3; '
                                         'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'CREATE ($a)-[:back]->($m) '
                                         'REMOVE $a.num '
                                         'SET $a += {key: 5} '
                                         'DELETE $l '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3;')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                },
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'update_part': [
                        {
                            'create_part': {
                                'patterns': [
                                    {
                                        'node': {
                                            'entity': '$a'
                                        },
                                        'chain': [
                                            {
                                                'relation': {
                                                    'direction': 'outgoing',
                                                    'types': ['back']
                                                },
                                                'node': {
                                                    'entity': '$m'
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            'remove_part': {
                                'items': [
                                    {
                                        'entity': '$a',
                                        'field': 'num'
                                    }
                                ]
                            }
                        },
                        {
                            'set_part': {
                                'items': [
                                    {
                                        'operator': '=',
                                        'entity': '$a',
                                        'properties': {
                                            'key': 5
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'delete_part': {
                                'detach': False,
                                'items': [
                                    {
                                        'entity': '$l'
                                    }
                                ]
                            }
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]
        })

    def test_clauses_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(clauses, '~other~') \
            .starts_with("Expected key_rule or key_rule at position")

    def test_clauses_1(self):
        assert_that(self.process(clauses, 'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]}
        )

    def test_clauses_2(self):
        assert_that(self.process(clauses, 'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3; '
                                          'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'CREATE ($a)-[:back]->($m) '
                                          'REMOVE $a.num '
                                          'SET $a += {key: 5} '
                                          'DELETE $l '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                },
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'update_part': [
                        {
                            'create_part': {
                                'patterns': [
                                    {
                                        'node': {
                                            'entity': '$a'
                                        },
                                        'chain': [
                                            {
                                                'relation': {
                                                    'direction': 'outgoing',
                                                    'types': ['back']
                                                },
                                                'node': {
                                                    'entity': '$m'
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            'remove_part': {
                                'items': [
                                    {
                                        'entity': '$a',
                                        'field': 'num'
                                    }
                                ]
                            }
                        },
                        {
                            'set_part': {
                                'items': [
                                    {
                                        'operator': '=',
                                        'entity': '$a',
                                        'properties': {
                                            'key': 5
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'delete_part': {
                                'detach': False,
                                'items': [
                                    {
                                        'entity': '$l'
                                    }
                                ]
                            }
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]
        })

    def test_clauses_3(self):
        assert_that(self.process(clauses, 'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3; '
                                          'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3; '
                                          'RULE "Description" SALIENCE 5 '
                                          'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                          'CREATE ($a)-[:back]->($m) '
                                          'REMOVE $a.num '
                                          'SET $a += {key: 5} '
                                          'DELETE $l '
                                          'RETURN $m.text AS name '
                                          'ORDER BY name DESC '
                                          'SKIP 5'
                                          'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': [
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                },
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                },
                {
                    'rule_part': {
                        'salience': 5,
                        'description': 'Description'
                    },
                    'match_part': [
                        {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$m',
                                        'labels': ['main']
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'entity': '$l',
                                                'types': ['links']
                                            },
                                            'node': {
                                                'entity': '$a',
                                                'properties': {
                                                    'key': 'value',
                                                    'num': -0.123
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'update_part': [
                        {
                            'create_part': {
                                'patterns': [
                                    {
                                        'node': {
                                            'entity': '$a'
                                        },
                                        'chain': [
                                            {
                                                'relation': {
                                                    'direction': 'outgoing',
                                                    'types': ['back']
                                                },
                                                'node': {
                                                    'entity': '$m'
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            'remove_part': {
                                'items': [
                                    {
                                        'entity': '$a',
                                        'field': 'num'
                                    }
                                ]
                            }
                        },
                        {
                            'set_part': {
                                'items': [
                                    {
                                        'operator': '=',
                                        'entity': '$a',
                                        'properties': {
                                            'key': 5
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'delete_part': {
                                'detach': False,
                                'items': [
                                    {
                                        'entity': '$l'
                                    }
                                ]
                            }
                        }
                    ],
                    'return_part': {
                        'items': [
                            {
                                'entity': '$m',
                                'field': 'text',
                                'synonym': 'name'
                            }
                        ],
                        'order_by': [
                            {
                                'ascending': False,
                                'name': 'name'
                            }
                        ],
                        'skip': 5,
                        'limit': 3
                    }
                }
            ]
        })

    def test_clause_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(clause, '~other~') \
            .starts_with("Expected key_rule or key_rule at position")

    def test_clause_1(self):
        assert_that(self.process(clause, 'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'rule_part': {
                    'description': 'Description',
                    'salience': 5,
                },
                'match_part': [
                    {
                        'patterns': [
                            {
                                'node': {
                                    'entity': '$m',
                                    'labels': ['main']
                                },
                                'chain': [
                                    {
                                        'relation': {
                                            'direction': 'outgoing',
                                            'entity': '$l',
                                            'types': ['links']
                                        },
                                        'node': {
                                            'entity': '$a',
                                            'properties': {
                                                'key': 'value',
                                                'num': -0.123
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'return_part': {
                    'items': [
                        {
                            'entity': '$m',
                            'field': 'text',
                            'synonym': 'name'
                        }
                    ],
                    'order_by': [
                        {
                            'ascending': False,
                            'name': 'name'
                        }
                    ],
                    'skip': 5,
                    'limit': 3
                }
            }
        })

    def test_clause_2(self):
        assert_that(self.process(clause, 'RULE "Description" SALIENCE 5 '
                                         'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                         'CREATE ($a)-[:back]->($m) '
                                         'REMOVE $a.num '
                                         'SET $a += {key: 5} '
                                         'DELETE $l '
                                         'RETURN $m.text AS name '
                                         'ORDER BY name DESC '
                                         'SKIP 5'
                                         'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'rule_part': {
                    'salience': 5,
                    'description': 'Description'
                },
                'match_part': [
                    {
                        'patterns': [
                            {
                                'node': {
                                    'entity': '$m',
                                    'labels': ['main']
                                },
                                'chain': [
                                    {
                                        'relation': {
                                            'direction': 'outgoing',
                                            'entity': '$l',
                                            'types': ['links']
                                        },
                                        'node': {
                                            'entity': '$a',
                                            'properties': {
                                                'key': 'value',
                                                'num': -0.123
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'update_part': [
                    {
                        'create_part': {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$a'
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'types': ['back']
                                            },
                                            'node': {
                                                'entity': '$m'
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        'remove_part': {
                            'items': [
                                {
                                    'entity': '$a',
                                    'field': 'num'
                                }
                            ]
                        }
                    },
                    {
                        'set_part': {
                            'items': [
                                {
                                    'operator': '=',
                                    'entity': '$a',
                                    'properties': {
                                        'key': 5
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'delete_part': {
                            'detach': False,
                            'items': [
                                {
                                    'entity': '$l'
                                }
                            ]
                        }
                    }
                ],
                'return_part': {
                    'items': [
                        {
                            'entity': '$m',
                            'field': 'text',
                            'synonym': 'name'
                        }
                    ],
                    'order_by': [
                        {
                            'ascending': False,
                            'name': 'name'
                        }
                    ],
                    'skip': 5,
                    'limit': 3
                }
            }
        })

    def test_clause_reading_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(clause_read, '~other~') \
            .starts_with("Expected key_rule at position")

    def test_clause_reading_99(self):
        assert_that(self.process(clause_read, 'RULE "Description" SALIENCE 5 '
                                              'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                              'RETURN $m.text AS name '
                                              'ORDER BY name DESC '
                                              'SKIP 5'
                                              'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'rule_part': {
                    'salience': 5,
                    'description': 'Description'
                },
                'match_part': [
                    {
                        'patterns': [
                            {
                                'node': {
                                    'entity': '$m',
                                    'labels': ['main']
                                },
                                'chain': [
                                    {
                                        'relation': {
                                            'direction': 'outgoing',
                                            'entity': '$l',
                                            'types': ['links']
                                        },
                                        'node': {
                                            'entity': '$a',
                                            'properties': {
                                                'key': 'value',
                                                'num': -0.123
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'return_part': {
                    'items': [
                        {
                            'entity': '$m',
                            'field': 'text',
                            'synonym': 'name'
                        }
                    ],
                    'order_by': [
                        {
                            'ascending': False,
                            'name': 'name'
                        }
                    ],
                    'skip': 5,
                    'limit': 3
                }
            }
        })

    def test_clause_updating_0(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(clause_update, '~other~') \
            .starts_with("Expected key_rule at position")

    def test_clause_updating_99(self):
        assert_that(self.process(clause_update, 'RULE "Description" SALIENCE 5 '
                                                'MATCH ($m:main)-[$l:links]->($a {key: "value", num: -0.123}) '
                                                'CREATE ($a)-[:back]->($m) '
                                                'REMOVE $a.num '
                                                'SET $a += {key: 5} '
                                                'DELETE $l '
                                                'RETURN $m.text AS name '
                                                'ORDER BY name DESC '
                                                'SKIP 5'
                                                'LIMIT 3')) \
            .contains_only('data') \
            .contains_entry({
            'data': {
                'rule_part': {
                    'salience': 5,
                    'description': 'Description'
                },
                'match_part': [
                    {
                        'patterns': [
                            {
                                'node': {
                                    'entity': '$m',
                                    'labels': ['main']
                                },
                                'chain': [
                                    {
                                        'relation': {
                                            'direction': 'outgoing',
                                            'entity': '$l',
                                            'types': ['links']
                                        },
                                        'node': {
                                            'entity': '$a',
                                            'properties': {
                                                'key': 'value',
                                                'num': -0.123
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'update_part': [
                    {
                        'create_part': {
                            'patterns': [
                                {
                                    'node': {
                                        'entity': '$a'
                                    },
                                    'chain': [
                                        {
                                            'relation': {
                                                'direction': 'outgoing',
                                                'types': ['back']
                                            },
                                            'node': {
                                                'entity': '$m'
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        'remove_part': {
                            'items': [
                                {
                                    'entity': '$a',
                                    'field': 'num'
                                }
                            ]
                        }
                    },
                    {
                        'set_part': {
                            'items': [
                                {
                                    'operator': '=',
                                    'entity': '$a',
                                    'properties': {
                                        'key': 5
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'delete_part': {
                            'detach': False,
                            'items': [
                                {
                                    'entity': '$l'
                                }
                            ]
                        }
                    }
                ],
                'return_part': {
                    'items': [
                        {
                            'entity': '$m',
                            'field': 'text',
                            'synonym': 'name'
                        }
                    ],
                    'order_by': [
                        {
                            'ascending': False,
                            'name': 'name'
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
