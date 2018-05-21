from unittest import TestCase

from arpeggio import NoMatch, ParserPython, SemanticError, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import clause, cypher, rule_description, rule_part, rule_salience
from grapple.parsing.visitor import KnowledgeVisitor


class TestGrammarVisitor(TestCase):
    """
    def knowledge():
        return Optional(clauses), Optional(';'), EOF
    
    def clauses():
        return clause, ZeroOrMore(';', clause)
    
    def clause():
        return rule_part(), ZeroOrMore(match_part), return_part
    
    """

    def test_knowledge_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(cypher, '~other~') \
            .starts_with("Expected key_rule or ';' or EOF at position")

    def test_knowledge_1(self):
        assert_that(self.process(cypher, '')) \
            .contains_only('value') \
            .contains_entry({'value': []})

    def test_knowledge_2(self):
        assert_that(self.process(cypher, ';')) \
            .contains_only('value') \
            .contains_entry({'value': []})

    def test_knowledge_3(self):
        assert_that(self.process(cypher, 'RULE RETURN True AS _bool')) \
            .contains_only('value') \
            .contains_entry({'value': [{'description': None,
                                        'result': {'distinct': False,
                                                   'items': [{'value': True, 'synonym': '_bool'}]}}]})

    def test_knowledge_4(self):
        assert_that(self.process(cypher, 'RULE RETURN True AS _bool;')) \
            .contains_only('value') \
            .contains_entry({'value': [{'description': None,
                                        'result': {'distinct': False,
                                                   'items': [{'value': True, 'synonym': '_bool'}]}}]})

    def test_knowledge_5(self):
        assert_that(self.process(cypher, 'RULE RETURN True AS _bool; '
                                            'RULE RETURN True AS _bool ORDER BY _bool SKIP 5 LIMIT 1;'
                                            'RULE "description" '
                                            'SALIENCE 5 '
                                            'OPTIONAL MATCH ($n :main:person {text: "Stefano"})-[:knows]-($f :person)'
                                            'RETURN $f.text AS name '
                                            'ORDER BY name '
                                            'SKIP 1 '
                                            'LIMIT 5')) \
            .contains_only('value') \
            .contains_entry({'value': [{'description': None,
                                        'result': {'distinct': False,
                                                   'items': [{'value': True, 'synonym': '_bool'}]}},
                                       {'description': None,
                                        'result': {'distinct': False,
                                                   'items': [{'value': True, 'synonym': '_bool'}],
                                                   'order': [{'ascending': True, 'synonym': '_bool'}],
                                                   'skip': 5,
                                                   'limit': 1}},
                                       {'description': 'description',
                                        'salience': 5,
                                        'match': [{'optional': True,
                                                   'pattern': [{'node': {'parameter': '$n',
                                                                         'labels': ['main', 'person'],
                                                                         'properties': {'text': 'Stefano'}},
                                                                'chain': [{'relation': {'direction': 'any',
                                                                                        'types': ['knows']},
                                                                           'node': {'parameter': '$f',
                                                                                    'labels': ['person']}}]}]}],
                                        'result': {'distinct': False,
                                                   'items': [{'parameter': '$f',
                                                              'property': 'text',
                                                              'synonym': 'name'}],
                                                   'order': [{'ascending': True, 'synonym': 'name'}],
                                                   'skip': 1,
                                                   'limit': 5}}]})

    def test_knowledge_7(self):
        assert_that(self.process(cypher, 'RULE "description" '
                                            'SALIENCE 5 '
                                            'OPTIONAL MATCH ($n :main:person {text: "Stefano"})-[:knows]-($f :person), '
                                            '               ($n)-[:works_at]->($c :company{current: True}) '
                                            'MATCH ($a :avatar)-[:linked_to]-($n) '
                                            'RETURN $f.text AS name, $c.text AS employer '
                                            'ORDER BY name, employer DESC '
                                            'SKIP 1 '
                                            'LIMIT 5')) \
            .contains_only('value') \
            .contains_entry({'value': [{'description': 'description',
                                        'salience': 5,
                                        'match': [{'optional': True,
                                                   'pattern': [{'node': {'parameter': '$n',
                                                                         'labels': ['main', 'person'],
                                                                         'properties': {
                                                                             'text': 'Stefano'}},
                                                                'chain': [{'relation': {'direction': 'any',
                                                                                        'types': ['knows']},
                                                                           'node': {'parameter': '$f',
                                                                                    'labels': ['person']}}]},
                                                               {'node': {'parameter': '$n'},
                                                                'chain': [{'relation': {'direction': 'outgoing',
                                                                                        'types': ['works_at']},
                                                                           'node': {'parameter': '$c',
                                                                                    'labels': ['company'],
                                                                                    'properties': {
                                                                                        'current': True}}}]}]},
                                                  {'optional': False,
                                                   'pattern': [{'node': {'parameter': '$a',
                                                                         'labels': ['avatar']},
                                                                'chain': [{'relation': {'direction': 'any',
                                                                                        'types': ['linked_to']},
                                                                           'node': {'parameter': '$n'}}]}]}],
                                        'result': {'distinct': False,
                                                   'items': [
                                                       {'parameter': '$f', 'property': 'text', 'synonym': 'name'},
                                                       {'parameter': '$c', 'property': 'text', 'synonym': 'employer'}],
                                                   'order': [{'ascending': True, 'synonym': 'name'},
                                                             {'ascending': False, 'synonym': 'employer'}],
                                                   'skip': 1,
                                                   'limit': 5}}]})

    def test_clause_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(clause, '~other~') \
            .starts_with("Expected key_rule at position")

    def test_clause_1(self):
        assert_that(self.process(clause, 'RULE RETURN True AS _bool')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None,
                                       'result': {'distinct': False,
                                                  'items': [{'value': True, 'synonym': '_bool'}]}}})

    def test_clause_2(self):
        assert_that(self.process(clause, 'RULE RETURN True AS _bool ORDER BY _bool SKIP 5 LIMIT 1')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None,
                                       'result': {'distinct': False,
                                                  'items': [{'value': True, 'synonym': '_bool'}],
                                                  'order': [{'synonym': '_bool', 'ascending': True}],
                                                  'skip': 5,
                                                  'limit': 1}}})

    def test_clause_3(self):
        assert_that(self.process(clause, 'RULE "description" '
                                         'SALIENCE 5 '
                                         'OPTIONAL MATCH ($n :main:person {text: "Stefano"})-[:knows]-($f :person)'
                                         'RETURN $f.text AS name '
                                         'ORDER BY name '
                                         'SKIP 1 '
                                         'LIMIT 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'description',
                                       'salience': 5,
                                       'match': [{'optional': True,
                                                  'pattern': [{'node': {'parameter': '$n',
                                                                        'labels': ['main', 'person'],
                                                                        'properties': {'text': 'Stefano'}},
                                                               'chain': [{'relation': {'direction': 'any',
                                                                                       'types': ['knows']},
                                                                          'node': {'parameter': '$f',
                                                                                   'labels': ['person']}}]}]}],
                                       'result': {'distinct': False,
                                                  'items': [{'parameter': '$f',
                                                             'property': 'text',
                                                             'synonym': 'name'}],
                                                  'order': [{'ascending': True,
                                                             'synonym': 'name'}],
                                                  'skip': 1,
                                                  'limit': 5}}})

    def test_rule_part_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(rule_part, '~other~') \
            .starts_with('Expected key_rule at position')

    def test_rule_part_1(self):
        assert_that(self.process(rule_part, 'RULE')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_2(self):
        assert_that(self.process(rule_part, 'Rule')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_3(self):
        assert_that(self.process(rule_part, 'rule')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_4(self):
        assert_that(self.process(rule_part, 'RULE "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_5(self):
        assert_that(self.process(rule_part, 'Rule "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_6(self):
        assert_that(self.process(rule_part, 'rule "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_7(self):
        assert_that(self.process(rule_part, "RULE 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    def test_rule_part_8(self):
        assert_that(self.process(rule_part, "Rule 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    def test_rule_part_9(self):
        assert_that(self.process(rule_part, "rule 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    # def test_rule_part_10(self):
    #     assert_that(self.process(rule_part, 'RULE identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    # def test_rule_part_11(self):
    #     assert_that(self.process(rule_part, 'Rule identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    # def test_rule_part_12(self):
    #     assert_that(self.process(rule_part, 'rule identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    def test_rule_part_13(self):
        assert_that(self.process(rule_part, 'RULE SALIENCE 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_14(self):
        assert_that(self.process(rule_part, 'Rule Salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_15(self):
        assert_that(self.process(rule_part, 'rule salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 0}})

    def test_rule_part_16(self):
        assert_that(self.process(rule_part, 'RULE "double_quote" SALIENCE 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_17(self):
        assert_that(self.process(rule_part, 'Rule "double_quote" Salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_18(self):
        assert_that(self.process(rule_part, 'rule "double_quote" salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 0}})

    def test_rule_part_19(self):
        assert_that(self.process(rule_part, "RULE 'single_quote' SALIENCE 0")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    def test_rule_part_20(self):
        assert_that(self.process(rule_part, "Rule 'single_quote' Salience 0")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    def test_rule_part_21(self):
        assert_that(self.process(rule_part, "rule 'single_quote' salience 0")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 0}})

    # def test_rule_part_22(self):
    #     assert_that(self.process(rule_part, 'RULE identifier SALIENCE 0')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    # def test_rule_part_23(self):
    #     assert_that(self.process(rule_part, 'Rule identifier Salience 0')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    # def test_rule_part_24(self):
    #     assert_that(self.process(rule_part, 'rule identifier salience 0')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 0}})

    def test_rule_part_25(self):
        assert_that(self.process(rule_part, 'RULE SALIENCE 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 5}})

    def test_rule_part_26(self):
        assert_that(self.process(rule_part, 'Rule Salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 5}})

    def test_rule_part_27(self):
        assert_that(self.process(rule_part, 'rule salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None, 'salience': 5}})

    def test_rule_part_28(self):
        assert_that(self.process(rule_part, 'RULE "double_quote" SALIENCE 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 5}})

    def test_rule_part_29(self):
        assert_that(self.process(rule_part, 'Rule "double_quote" Salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 5}})

    def test_rule_part_30(self):
        assert_that(self.process(rule_part, 'rule "double_quote" salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote', 'salience': 5}})

    def test_rule_part_31(self):
        assert_that(self.process(rule_part, "RULE 'single_quote' SALIENCE 5")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 5}})

    def test_rule_part_32(self):
        assert_that(self.process(rule_part, "Rule 'single_quote' Salience 5")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 5}})

    def test_rule_part_33(self):
        assert_that(self.process(rule_part, "rule 'single_quote' salience 5")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote', 'salience': 5}})

    # def test_rule_part_34(self):
    #     assert_that(self.process(rule_part, 'RULE identifier SALIENCE 5')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 5}})

    # def test_rule_part_35(self):
    #     assert_that(self.process(rule_part, 'Rule identifier Salience 5')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 5}})

    # def test_rule_part_36(self):
    #     assert_that(self.process(rule_part, 'rule identifier salience 5')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier', 'salience': 5}})

    def test_rule_part_37(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'RULE SALIENCE -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_38(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'Rule Salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_39(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'rule salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_40(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'RULE "double_quote" SALIENCE -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_41(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'Rule "double_quote" Salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_42(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, 'rule "double_quote" salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_43(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, "RULE 'single_quote' SALIENCE -5") \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_44(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, "Rule 'single_quote' Salience -5") \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_part_45(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_part, "rule 'single_quote' salience -5") \
            .starts_with('"\'salience\' expected to be non-negative"')

    # def test_rule_part_46(self):
    #     assert_that(TestGrammarVisitor.process) \
    #         .raises(SemanticError) \
    #         .when_called_with(rule_part, 'RULE identifier SALIENCE -5') \
    #         .starts_with('"\'salience\' expected to be non-negative"')

    # def test_rule_part_47(self):
    #     assert_that(TestGrammarVisitor.process) \
    #         .raises(SemanticError) \
    #         .when_called_with(rule_part, 'Rule identifier Salience -5') \
    #         .starts_with('"\'salience\' expected to be non-negative"')

    # def test_rule_part_48(self):
    #     assert_that(TestGrammarVisitor.process) \
    #         .raises(SemanticError) \
    #         .when_called_with(rule_part, 'rule identifier salience -5') \
    #         .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_description_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(rule_description, '~other~') \
            .starts_with('Expected key_rule at position')

    def test_rule_description_1(self):
        assert_that(self.process(rule_description, 'RULE')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None}})

    def test_rule_description_2(self):
        assert_that(self.process(rule_description, 'Rule')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None}})

    def test_rule_description_3(self):
        assert_that(self.process(rule_description, 'rule')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': None}})

    def test_rule_description_4(self):
        assert_that(self.process(rule_description, 'RULE "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote'}})

    def test_rule_description_5(self):
        assert_that(self.process(rule_description, 'Rule "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote'}})

    def test_rule_description_6(self):
        assert_that(self.process(rule_description, 'rule "double_quote"')) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'double_quote'}})

    def test_rule_description_7(self):
        assert_that(self.process(rule_description, "RULE 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote'}})

    def test_rule_description_8(self):
        assert_that(self.process(rule_description, "Rule 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote'}})

    def test_rule_description_9(self):
        assert_that(self.process(rule_description, "rule 'single_quote'")) \
            .contains_only('value') \
            .contains_entry({'value': {'description': 'single_quote'}})

    # def test_rule_description_10(self):
    #     assert_that(self.process(rule_description, 'RULE identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier'}})

    # def test_rule_description_11(self):
    #     assert_that(self.process(rule_description, 'Rule identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier'}})

    # def test_rule_description_12(self):
    #     assert_that(self.process(rule_description, 'rule identifier')) \
    #         .contains_only('value') \
    #         .contains_entry({'value': {'description': 'identifier'}})

    def test_rule_salience_0(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(NoMatch) \
            .when_called_with(rule_salience, '~other~') \
            .starts_with('Expected key_salience at position')

    def test_rule_salience_1(self):
        assert_that(self.process(rule_salience, 'SALIENCE 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 0}})

    def test_rule_salience_2(self):
        assert_that(self.process(rule_salience, 'Salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 0}})

    def test_rule_salience_3(self):
        assert_that(self.process(rule_salience, 'salience 0')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 0}})

    def test_rule_salience_4(self):
        assert_that(self.process(rule_salience, 'SALIENCE 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 5}})

    def test_rule_salience_5(self):
        assert_that(self.process(rule_salience, 'Salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 5}})

    def test_rule_salience_6(self):
        assert_that(self.process(rule_salience, 'salience 5')) \
            .contains_only('value') \
            .contains_entry({'value': {'salience': 5}})

    def test_rule_salience_7(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_salience, 'SALIENCE -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_salience_8(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_salience, 'Salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    def test_rule_salience_9(self):
        assert_that(TestGrammarVisitor.process) \
            .raises(SemanticError) \
            .when_called_with(rule_salience, 'salience -5') \
            .starts_with('"\'salience\' expected to be non-negative"')

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
