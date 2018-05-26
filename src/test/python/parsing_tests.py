import re
from unittest import TestCase

from arpeggio import ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.old_descriptors import RuleBase
from grapple.parsing.grammar import comment, cypher
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_integration_parsing_0(self):
        content = 'RULE RETURN true AS _bool; \n' \
                  '\n' \
                  'RULE RETURN true AS _bool ORDER BY _bool SKIP 5 LIMIT 1;\n' \
                  '\n' \
                  'RULE "description" \n' \
                  'SALIENCE 5 \n' \
                  'OPTIONAL MATCH ($n :main:person {"text": "Stefano"})-[:knows]-($f :person)\n' \
                  'RETURN $f.text AS name \n' \
                  'ORDER BY name \n' \
                  'SKIP 1 \n' \
                  'LIMIT 5;'

        parser = ParserPython(cypher, comment_def=comment)
        parsed = parser.parse(content)
        visited = visit_parse_tree(parsed, KnowledgeVisitor())
        base = RuleBase(visited['value'])
        result = repr(base)

        assert_that(re.sub(r'\s+', ' ', result)) \
            .is_equal_to(re.sub(r'\s+', ' ', content))
