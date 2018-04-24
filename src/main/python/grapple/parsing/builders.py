from arpeggio import ParserPython, visit_parse_tree

from grapple.parsing.grammar import base, comment
from grapple.parsing.visitors import GrammarVisitor


class Builder(object):

    def parse(self, filename: str) -> 'Base':
        with open(filename, 'r') as file:
            content = file.read()
            parser = ParserPython(base, comment)
            parse_tree = parser.parse(content)
            resource = visit_parse_tree(parse_tree, GrammarVisitor())

