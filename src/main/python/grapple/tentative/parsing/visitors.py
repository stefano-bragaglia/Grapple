from arpeggio import PTNodeVisitor, ParserPython, visit_parse_tree

from grapple.tentative.parsing.grammar import comment
from grapple.tentative.parsing.grammar import knowledge
from grapple.tentative.parsing.support2 import Direction


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
            result.update(child["value"])

        return {"value": result}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_rule_part(self, node, children):
        result = {"description": children[1]["value"]}
        for child in children[2:]:
            result.update(child["value"])

        return {"value": result}

    def visit_salience(self, node, children):
        return {"value": {"salience": children[1]["value"]}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_match_part(self, node, children):
        return {"value": None}

    def visit_optional(self, node, children):
        return {"value": {"optional": True}}

    def visit_match(self, node, children):
        return {"value": {"match": children[1]["value"]}}

    def visit_pattern_list(self, node, children):
        return {"value": [child["value"] for child in children]}

    def visit_pattern(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": {"pattern": result}}

    def visit_pattern_anonymous(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": {"pattern": result}}

    def visit_pattern_start(self, node, children):
        return {"value": {"start": children[0]["value"]}}

    def visit_pattern_chain(self, node, children):
        return {"value": {"chain": [child["value"] for child in children]}}

    def visit_pattern_next(self, node, children):
        return {"value": {"relation": children[0]["value"], "node": children[1]["value"]}}

    def visit_node_pattern(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_relation_pattern(self, node, children):
        return {"value": children[0]["value"]}

    def visit_relation_pattern_both(self, node, children):
        result = children[0]["value"]
        result["direction"] = Direction.ANY.value

        return {"value": result}

    def visit_relation_pattern_back(self, node, children):
        result = children[0]["value"]
        result["direction"] = Direction.INCOMING.value

        return {"value": result}

    def visit_relation_pattern_next(self, node, children):
        result = children[0]["value"]
        result["direction"] = Direction.OUTGOING.value

        return {"value": result}

    def visit_relation_pattern_none(self, node, children):
        result = children[0]["value"]
        result["direction"] = Direction.ANY.value

        return {"value": result}

    def visit_relation_details(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_labels(self, node, children):
        return {"value": {"labels": [child["value"] for child in children]}}

    def visit_types(self, node, children):
        return {"value": {"types": [child["value"] for child in children]}}

    def visit_tag_list(self, node, children):
        return {"value": [child["value"] for child in children]}

    def visit_properties(self, node, children):
        return {"value": {"properties": children[0]["value"]}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_return_part(self, node, children):
        return {"value": None}

    def visit_distinct(self, node, children):
        return {"value": {"distinct": True}}

    def visit_return_item_list(self, node, children):
        return {"value": [child["value"] for child in children]}

    def visit_return_first(self, node, children):
        return {"value": children[0]["value"]}

    def visit_return_all(self, node, children):
        return {"value": {"function": "*"}}

    def visit_return_item(self, node, children):
        return {"value": children[0]["value"]}

    def visit_return_coalesce(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_coalesce(self, node, children):
        return {"value": {"function": "coalesce"}}

    def visit_return_keys(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_keys(self, node, children):
        return {"value": {"function": "keys"}}

    def visit_return_properties(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_properties(self, node, children):
        return {"value": {"function": "properties"}}

    def visit_return_id(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_id(self, node, children):
        return {"value": {"function": "id"}}

    def visit_return_labels(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_labels(self, node, children):
        return {"value": {"function": "labels"}}

    def visit_return_types(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_types(self, node, children):
        return {"value": {"function": "types"}}

    def visit_return_tail(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_tail(self, node, children):
        return {"value": {"function": "tail"}}

    def visit_return_head(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_function_head(self, node, children):
        return {"value": {"function": "head"}}

    def visit_return_selector(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_field(self, node, children):
        return {"value": {"key": children[0]["value"]}}

    def visit_return_value(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_value(self, node, children):
        return {"value": {"value": children[0]["value"]}}

    def visit_synonym(self, node, children):
        return {"value": {"as": children[1]["value"]}}

    def visit_order(self, node, children):
        return {"value": None}

    def visit_order_item_list(self, node, children):
        return {"value": None}

    def visit_order_item(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_selector(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_ordering(self, node, children):
        return {"value": None}

    def visit_limit(self, node, children):
        return {"value": None}

    def visit_skip(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_json_properties(self, node, children):
        return {"value": children[0]["value"]}

    def visit_json_member_list(self, node, children):
        result = {}
        for child in children:
            result.update(child["value"])

        return {"value": result}

    def visit_json_member(self, node, children):
        return {"value": {children[0]["value"]: children[1]["value"]}}

    def visit_json_key(self, node, children):
        return {"value": children[0]["value"]}

    def visit_json_value(self, node, children):
        return {"value": children[0]["value"]}

    def visit_json_string(self, node, children):
        return {"value": children[0]["value"]}

    def visit_json_string_single(self, node, children):
        return {"value": children[0]}

    def visit_json_string_double(self, node, children):
        return {"value": children[0]}

    def visit_json_integer(self, node, children):
        return {"value": int(node.value)}

    def visit_json_real(self, node, children):
        return {"value": float(node.value)}

    def visit_json_array(self, node, children):
        return {"value": children[0]["value"]}

    def visit_json_element_list(self, node, children):
        return {"value": [child["value"] for child in children]}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_true(self, node, children):
        return {"value": True}

    def visit_false(self, node, children):
        return {"value": False}

    def visit_null(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_identifier(self, node, children):
        return {"value": node.value}

    def visit_tag(self, node, children):
        return {"value": node.value[1:]}

    def visit_variable(self, node, children):
        return {"value": node.value[1:]}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_comment(self, node, children):
        return {"value": None}


if __name__ == "__main__":
    content = '/* Multi-line comment\n' \
              ' * ****************** */\n' \
              'RULE rule_name\n' \
              'SALIENCE 5\n' \
              'OPTIONAL MATCH $a = ($b :main:node {k1: "value", "k2": 5})' \
              '-[$c :link {key: "value"}]->($d :other {key: null}),\n' \
              '               $e = ($f :main:node {"key": -1})' \
              '-[$g :link {"key": 0.5E-2}]->($h :other {key: True})\n' \
              '// Single-line comment\n' \
              'RETURN DISTINCT *,\n' \
              '                coalesce($a.key, ["v1", "v2"]) AS s_01,\n' \
              '                id($a) AS s_02,\n' \
              '                keys($a) AS s_03,\n' \
              '                properties($a) AS s_04,\n' \
              '                labels($a) AS s_05,\n' \
              '                types($a) AS s_06,\n' \
              '                tail($a) AS s_07,\n' \
              '                head($a) AS s_08,\n' \
              '                $a AS s_09,\n' \
              '                $a.key AS s_10,\n' \
              '                True AS s_11\n' \
              'ORDER BY $a, $a.key, name, $b DESC, $b.key DESC, surname DESC\n' \
              'SKIP 5\n' \
              'LIMIT 10;\n'

    parser = ParserPython(knowledge, comment)
    parse_tree = parser.parse(content)
    print(parse_tree)
    # print(json.dumps(parse_tree, indent=4))
    result = visit_parse_tree(parse_tree, GrammarVisitor())
    print(result)
    # print(json.dumps(result["value"], indent=4))
