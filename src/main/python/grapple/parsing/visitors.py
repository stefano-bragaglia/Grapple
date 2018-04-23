import json

from arpeggio import PTNodeVisitor, visit_parse_tree

from grapple.parsing.grammar import *


# noinspection PyMethodMayBeStatic
class GrammarVisitor(PTNodeVisitor):

    def visit_part_return(self, node, children) -> object:
        return {'value': {'return': children[1]['value']}}

    def visit_selectors(self, node, children) -> object:
        return {'value': [child for child in children]}

    def visit_selector(self, node, children) -> object:
        value = children[0]['value']
        value['as'] = children[1]['value']['as'] if len(children) > 1 else None
        return value

    def visit_content(self, node, children) -> object:
        return {'value': children[0]['value']}

    def visit_value(self, node, children) -> object:
        return {'value': {'type': 'value', 'content': children[0]['value']}}

    def visit_labels(self, node, children) -> object:
        return {'value': {'type': 'labels', 'content': children[1]['value']}}

    def visit_types(self, node, children) -> object:
        return {'value': {'type': 'types', 'content': children[1]['value']}}

    def visit_ident(self, node, children) -> object:
        return {'value': {'type': 'id', 'content': children[1]['value']}}

    def visit_accessor(self, node, children) -> object:
        return {'value': {
            'type': 'accessor',
            'content': children[0]['value'],
            'field': children[1]['value'] if len(children) > 1 else None,
        }}

    def visit_synonym(self, node, children) -> object:
        return {'value': {'as': children[1]['value']}}

    def visit_identifier(self, node, children) -> object:
        return {'value': node.value}

    def visit_variable(self, node, children) -> object:
        return {'value': node.value}

    def visit_json_object(self, node, children) -> object:
        return {"value": children[0]['value']}

    def visit_json_members(self, node, children) -> object:
        return {"value": {child['value']['key']: child['value']['value'] for child in children}}

    def visit_json_member(self, node, children) -> object:
        return {"value": {'key': children[0]['value'], 'value': children[1]['value']}}

    def visit_json_value(self, node, children) -> object:
        return {"value": children[0]['value']}

    def visit_json_string(self, node, children) -> object:
        return {"value": children[0]}

    def visit_json_number(self, node, children) -> object:
        try:
            return {"value": int(node.value)}
        except ValueError:
            return {"value": float(node.value)}

    def visit_json_array(self, node, children) -> object:
        return {"value": children[0]['value']}

    def visit_json_elements(self, node, children) -> object:
        return {"value": [child['value'] for child in children]}

    def visit_key_as(self, node, children) -> object:
        return {"value": "AS"}

    def visit_key_false(self, node, children) -> object:
        return {"value": False}

    def visit_key_id(self, node, children) -> object:
        return {"value": "ID"}

    def visit_key_labels(self, node, children) -> object:
        return {"value": "LABELS"}

    def visit_key_null(self, node, children) -> object:
        return {"value": None}

    def visit_key_return(self, node, children) -> object:
        return {"value": "RETURN"}

    def visit_key_true(self, node, children) -> object:
        return {"value": True}

    def visit_key_types(self, node, children) -> object:
        return {"value": "TYPES"}

    def visit_comment(self, node, children) -> object:
        return {'value': node.value}


if __name__ == '__main__':
    content = 'RETURN {"some": "value"} AS dict, labels($v1), types($v2) AS types, id($v3), $v4 AS name, $v5.field'
    print(content)

    parser = ParserPython(part_return, comment)
    parse_tree = parser.parse(content)
    result = visit_parse_tree(parse_tree, GrammarVisitor())
    print(json.dumps(result['value'], indent=4))
