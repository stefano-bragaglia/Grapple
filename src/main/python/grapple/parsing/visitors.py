from arpeggio import PTNodeVisitor, ParseTreeNode, visit_parse_tree

from grapple.parsing.grammar import *


# noinspection PyMethodMayBeStatic
class GrammarVisitor(PTNodeVisitor):

    def visit_comment(self, node: ParseTreeNode, children) -> object:
        return "asd"

    def visit_key_as(self, node: ParseTreeNode, children) -> object:
        return "AS"

    def visit_key_false(self, node: ParseTreeNode, children) -> object:
        return False

    def visit_key_id(self, node: ParseTreeNode, children) -> object:
        return "ID"

    def visit_key_labels(self, node: ParseTreeNode, children) -> object:
        return "LABELS"

    def visit_key_null(self, node: ParseTreeNode, children) -> object:
        return None

    def visit_key_return(self, node: ParseTreeNode, children) -> object:
        return "RETURN"

    def visit_key_true(self, node: ParseTreeNode, children) -> object:
        return True

    def visit_key_types(self, node: ParseTreeNode, children) -> object:
        return "TYPES"


if __name__ == '__main__':
    content = '// Testing comments '
    content = '/* Testing \n' \
              '   comments */'
    parser = ParserPython(comment)
    parse_tree = parser.parse(content)
    result = visit_parse_tree(parse_tree, GrammarVisitor())
