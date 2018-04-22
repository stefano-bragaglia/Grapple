from arpeggio import ParserPython, visit_parse_tree

from grapple.parsing.grammar import base, comment


class Builder(object):

    def parse(self, filename: str) -> 'Base':
        with open(filename, 'r') as file:
            content = file.read()
            parser = ParserPython(base, comment)
            parse_tree = parser.parse(content)
            for query in visit_parse_tree(parse_tree, GrammarVisitor()):
                pass
