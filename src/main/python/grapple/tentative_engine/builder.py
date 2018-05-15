from typing import List, Dict

from arpeggio import visit_parse_tree

from grapple.parsing.temp.grammar import parser
from grapple.parsing.temp.visitors import GrammarVisitor


class Builder(object):

    def parse(self, filename: str) -> List[Dict]:
        with open(filename, 'r') as file:
            content = file.read()
            parse_tree = parser.parse(content)
            return visit_parse_tree(parse_tree, GrammarVisitor())
