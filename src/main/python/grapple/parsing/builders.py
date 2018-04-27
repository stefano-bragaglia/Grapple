import json

from arpeggio import ParserPython, visit_parse_tree

from grapple.parsing.grammar import resource, comment
from grapple.parsing.visitors import GrammarVisitor


class Builder(object):

    @staticmethod
    def load(filename: str) -> 'Base':
        with open(filename, 'r') as file:
            content = file.read()
            return Builder.parse(content)

    @staticmethod
    def parse(content: str) -> 'Base':
        parser = ParserPython(resource, comment)
        parse_tree = parser.parse(content)
        print(parse_tree)
        # print(json.dumps(parse_tree, indent=4))
        # result = visit_parse_tree(parse_tree, GrammarVisitor())
        # print(json.dumps(result['value'], indent=4))


if __name__ == '__main__':
    content = 'RULE "This is an example" ' \
              'SALIENCE 5 ' \
              'MATCH ($v1 :label1 :labels2 {"alpha": "string", "beta": 123})-[$v2]->(:type1:type2) ' \
              'MATCH ({"alpha": "string", "beta": 123})<--($v3:label3:label4)-[$v4{"current": True}]-(:label5{"main": True}) ' \
              'RETURN {"some": "value"} AS dict, labels($v1), types($v2) AS types, id($v3), $v4 AS name, $v5.field; ' \
              'RULE RETURN True AS def; '
    print(content)

    Builder.parse(content)
