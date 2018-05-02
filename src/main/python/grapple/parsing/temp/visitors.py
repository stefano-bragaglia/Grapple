from arpeggio import PTNodeVisitor, ParserPython, visit_parse_tree

from grapple.parsing.temp.grammar import comment
from grapple.parsing.temp.grammar import knowledge
from grapple.parsing.temp.support2 import Direction


# noinspection PyMethodMayBeStatic
class GrammarVisitor(PTNodeVisitor):
    def visit_knowledge(self, node, children):
        return {"value": None}

    def visit_clause_list(self, node, children):
        return {"value": None}

    def visit_clause(self, node, children):
        return {"value": None}

    def visit_clause_reading(self, node, children):
        return {"value": None}

    def visit_reading_part(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": result}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_rule_part(self, node, children):
        result = {'description': children[1]['value']}
        for child in children[2:]:
            result.update(child['value'])

        return {"value": result}

    def visit_salience(self, node, children):
        return {"value": {'salience': children[1]['value']}}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_match_part(self, node, children):
        return {"value": None}

    def visit_optional(self, node, children):
        return {'value': {'optional': True}}

    def visit_match(self, node, children):
        return {"value": {'match': children[1]['value']}}

    def visit_pattern_list(self, node, children):
        return {"value": [child['value'] for child in children]}

    def visit_pattern(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": {'pattern': result}}

    def visit_pattern_anonymous(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": {'pattern': result}}

    def visit_pattern_start(self, node, children):
        return {"value": {'start': children[0]['value']}}

    def visit_pattern_chain(self, node, children):
        return {"value": {'chain': [child['value'] for child in children]}}

    def visit_pattern_next(self, node, children):
        return {"value": {'relation': children[0]['value'], 'node': children[1]['value']}}

    def visit_node_pattern(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": result}

    def visit_relation_pattern(self, node, children):
        return {"value": children[0]['value']}

    def visit_relation_pattern_both(self, node, children):
        result = children[0]['value']
        result['direction'] = Direction.ANY.value

        return {"value": result}

    def visit_relation_pattern_back(self, node, children):
        result = children[0]['value']
        result['direction'] = Direction.INCOMING.value

        return {"value": result}

    def visit_relation_pattern_next(self, node, children):
        result = children[0]['value']
        result['direction'] = Direction.OUTGOING.value

        return {"value": result}

    def visit_relation_pattern_none(self, node, children):
        result = children[0]['value']
        result['direction'] = Direction.ANY.value

        return {"value": result}

    def visit_relation_details(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": result}

    def visit_labels(self, node, children):
        return {"value": {'labels': [child['value'] for child in children]}}

    def visit_types(self, node, children):
        return {"value": {'types': [child['value'] for child in children]}}

    def visit_tag_list(self, node, children):
        return {"value": [child['value'] for child in children]}

    def visit_properties(self, node, children):
        return {"value": {'properties': children[0]['value']}}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_return_part(self, node, children):
        return {"value": None}

    def visit_distinct(self, node, children):
        return {"value": None}

    def visit_return_item_list(self, node, children):
        return {"value": None}

    def visit_return_first(self, node, children):
        return {"value": None}

    def visit_return_all(self, node, children):
        return {"value": None}

    def visit_return_item(self, node, children):
        return {"value": None}

    def visit_return_coalesce(self, node, children):
        return {"value": None}

    def visit_return_keys(self, node, children):
        return {"value": None}

    def visit_return_properties(self, node, children):
        return {"value": None}

    def visit_return_id(self, node, children):
        return {"value": None}

    def visit_return_labels(self, node, children):
        return {"value": None}

    def visit_return_types(self, node, children):
        return {"value": None}

    def visit_return_tail(self, node, children):
        return {"value": None}

    def visit_return_head(self, node, children):
        return {"value": None}

    def visit_return_selector(self, node, children):
        return {"value": None}

    def visit_return_value(self, node, children):
        return {"value": None}

    def visit_order(self, node, children):
        return {"value": None}

    def visit_order_item_list(self, node, children):
        return {"value": None}

    def visit_order_item(self, node, children):
        return {"value": None}

    def visit_selector(self, node, children):
        return {"value": None}

    def visit_ordering(self, node, children):
        return {"value": None}

    def visit_limit(self, node, children):
        return {"value": None}

    def visit_skip(self, node, children):
        return {"value": None}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_json_properties(self, node, children):
        return {"value": children[0]['value']}

    def visit_json_member_list(self, node, children):
        result = {}
        for child in children:
            result.update(child['value'])

        return {"value": result}

    def visit_json_member(self, node, children):
        return {"value": {children[0]['value']: children[1]['value']}}

    def visit_json_key(self, node, children):
        return {"value": children[0]['value']}

    def visit_json_value(self, node, children):
        return {"value": children[0]['value']}

    def visit_json_string(self, node, children):
        return {"value": children[0]['value']}

    def visit_json_string_single(self, node, children):
        return {"value": children[0]}

    def visit_json_string_double(self, node, children):
        return {"value": children[0]}

    def visit_json_integer(self, node, children):
        return {"value": int(node.value)}

    def visit_json_real(self, node, children):
        return {"value": float(node.value)}

    def visit_json_array(self, node, children):
        return {"value": None}

    def visit_json_element_list(self, node, children):
        return {"value": None}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_true(self, node, children):
        return {"value": True}

    def visit_false(self, node, children):
        return {"value": False}

    def visit_null(self, node, children):
        return {"value": None}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_identifier(self, node, children):
        return {"value": node.value}

    def visit_tag(self, node, children):
        return {"value": node.value[1:]}

    def visit_variable(self, node, children):
        return {"value": {'variable': node.value[1:]}}

    # ----------------------------------------------------------------------------------------------------------------------
    def visit_comment(self, node, children):
        return {"value": None}


if __name__ == '__main__':
    content = """
        /* Multi-line comment
         * ****************** */
        RULE rule_name
        SALIENCE 5
        OPTIONAL MATCH $a = ($b :main:node {k1: "value", "k2": 5})-[$c :link {key: "value"}]->($d :other {key: null}), 
                       $e = ($f :main:node {"key": -1})-[$g :link {'key': 0.5E-2}]->($h :other {key: True})
        // Single-line comment
        RETURN DISTINCT *, 
                        id($a) AS s_02, 
                        keys($a) AS s_03, 
                        properties($a) AS s_04, 
                        labels($a) AS s_05, 
                        types($a) AS s_06, 
                        tail($a) AS s_07, 
                        head($a) AS s_08 
        ORDER BY $a, $a.key, name, $b DESC, $b.key DESC, surname DESC 
        SKIP 5 
        LIMIT 10;
    """

    parser = ParserPython(knowledge, comment)
    parse_tree = parser.parse(content)
    print(parse_tree)
    # print(json.dumps(parse_tree, indent=4))
    result = visit_parse_tree(parse_tree, GrammarVisitor())
    print(result)
    # print(json.dumps(result['value'], indent=4))
