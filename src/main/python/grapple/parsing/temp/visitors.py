from arpeggio import PTNodeVisitor, ParserPython

# noinspection PyMethodMayBeStatic
from grapple.parsing.temp.grammar import comment, resource


class GrammarVisitor(PTNodeVisitor):
    def visit_resource(self, node, children):
        return {"value": None}

    def visit_statement(self, node, children):
        return {"value": None}

    def visit_query(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_match_body(self, node, children):
        return {"value": None}

    def visit_pattern_list(self, node, children):
        return {"value": None}

    def visit_pattern(self, node, children):
        return {"value": None}

    def visit_anonymous_pattern(self, node, children):
        return {"value": None}

    def visit_pattern_chain(self, node, children):
        return {"value": None}

    def visit_pattern_next(self, node, children):
        return {"value": None}

    def visit_node_pattern(self, node, children):
        return {"value": None}

    def visit_relation_pattern(self, node, children):
        return {"value": None}

    def visit_relation_both_pattern(self, node, children):
        return {"value": None}

    def visit_relation_back_pattern(self, node, children):
        return {"value": None}

    def visit_relation_next_pattern(self, node, children):
        return {"value": None}

    def visit_relation_none_pattern(self, node, children):
        return {"value": None}

    def visit_relation_details(self, node, children):
        return {"value": None}

    def visit_tags(self, node, children):
        return {"value": None}

    def visit_tag(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_return_body(self, node, children):
        return {"value": None}

    def visit_distinct(self, node, children):
        return {"value": None}

    def visit_limit(self, node, children):
        return {"value": None}

    def visit_skip(self, node, children):
        return {"value": None}

    def visit_order(self, node, children):
        return {"value": None}

    def visit_order_items(self, node, children):
        return {"value": None}

    def visit_order_item(self, node, children):
        return {"value": None}

    def visit_order_selector(self, node, children):
        return {"value": None}

    def visit_order_ordering(self, node, children):
        return {"value": None}

    def visit_return_items(self, node, children):
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

    # ------------------------------------------------------------------------------------------------------------------
    def visit_properties(self, node, children):
        return {"value": None}

    def visit_members(self, node, children):
        return {"value": None}

    def visit_member(self, node, children):
        return {"value": None}

    def visit_key(self, node, children):
        return {"value": None}

    def visit_value(self, node, children):
        return {"value": None}

    def visit_string(self, node, children):
        return {"value": None}

    def visit_single(self, node, children):
        return {"value": None}

    def visit_double(self, node, children):
        return {"value": None}

    def visit_integer(self, node, children):
        return {"value": None}

    def visit_real(self, node, children):
        return {"value": None}

    def visit_array(self, node, children):
        return {"value": None}

    def visit_elements(self, node, children):
        return {"value": None}

    def visit_true(self, node, children):
        return {"value": None}

    def visit_false(self, node, children):
        return {"value": None}

    def visit_null(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_identifier(self, node, children):
        return {"value": None}

    def visit_parameter(self, node, children):
        return {"value": None}

    def visit_variable(self, node, children):
        return {"value": None}

    # ------------------------------------------------------------------------------------------------------------------
    def comment(self, node, children):
        return {"value": None}


if __name__ == '__main__':
    content = """
        /* Multi-line comment
         * ****************** */
        OPTIONAL MATCH $a = ($b :main:node {"key": "value"})-[$c :link {"key": "value"}]->($d :other {"key": "value"}), 
                       $e = ($f :main:node {"key": "value"})-[$g :link {"key": "value"}]->($h :other {"key": "value"})
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

    parser = ParserPython(resource, comment)
    parse_tree = parser.parse(content)
    print(parse_tree)
    # print(json.dumps(parse_tree, indent=4))
    # result = visit_parse_tree(parse_tree, GrammarVisitor())
    # print(json.dumps(result['value'], indent=4))
