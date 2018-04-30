from arpeggio import ParserPython

from grapple.parsing.reference.cypher import cypher, comment


class Builder(object):

    @staticmethod
    def load(filename: str) -> 'Base':
        with open(filename, 'r') as file:
            content = file.read()
            return Builder.parse(content)

    @staticmethod
    def parse(content: str) -> 'Base':
        parser = ParserPython(cypher, comment)
        parse_tree = parser.parse(content)
        print(parse_tree)
        # print(json.dumps(parse_tree, indent=4))
        # result = visit_parse_tree(parse_tree, GrammarVisitor())
        # print(json.dumps(result['value'], indent=4))


if __name__ == '__main__':
    content = "MATCH (n) RETURN n;"
    print(content)
    print(
        "------------------------------------------------------------------------------------------------------------------------")

    Builder.parse(content)
    print(
        "========================================================================================================================")
