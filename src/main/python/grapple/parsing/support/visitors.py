from arpeggio import PTNodeVisitor


# noinspection PyMethodMayBeStatic
class CypherVisitor(PTNodeVisitor):

    def visit_cypher(self, node, children) -> object:
        return None

    def visit_statement(self, node, children) -> object:
        return None

    def visit_query(self, node, children) -> object:
        return None

    def visit_regular_query(self, node, children) -> object:
        return None

    def visit_union(self, node, children) -> object:
        return None

    def visit_single_query(self, node, children) -> object:
        return None

    def visit_single_part_query(self, node, children) -> object:
        return None

    def visit_multi_part_query(self, node, children) -> object:
        return None

    def visit_updating_clause(self, node, children) -> object:
        return None

    def visit_reading_clause(self, node, children) -> object:
        return None

    def visit_match(self, node, children) -> object:
        return None

    def visit_unwind(self, node, children) -> object:
        return None

    def visit_merge(self, node, children) -> object:
        return None

    def visit_merge_action(self, node, children) -> object:
        return None

    def visit_create(self, node, children) -> object:
        return None

    def visit_set_(self, node, children) -> object:
        return None

    def visit_set_item(self, node, children) -> object:
        return None

    def visit_delete(self, node, children) -> object:
        return None

    def visit_remove(self, node, children) -> object:
        return None

    def visit_remove_item(self, node, children) -> object:
        return None

    def visit_in_query_call(self, node, children) -> object:
        return None

    def visit_standalone_call(self, node, children) -> object:
        return None

    def visit_yield_items(self, node, children) -> object:
        return None

    def visit_yield_item(self, node, children) -> object:
        return None

    def visit_with_(self, node, children) -> object:
        return None

    def visit_return_(self, node, children) -> object:
        return None

    def visit_return_body(self, node, children) -> object:
        return None

    def visit_return_items(self, node, children) -> object:
        return None

    def visit_return_item(self, node, children) -> object:
        return None

    def visit_order(self, node, children) -> object:
        return None

    def visit_sort_items(self, node, children) -> object:
        return None

    def visit_skip(self, node, children) -> object:
        return None

    def visit_limit(self, node, children) -> object:
        return None

    def visit_sort_item(self, node, children) -> object:
        return None

    def visit_where(self, node, children) -> object:
        return None

    def visit_pattern(self, node, children) -> object:
        return None

    def visit_pattern_part(self, node, children) -> object:
        return None

    def visit_anonymous_pattern_part(self, node, children) -> object:
        return None

    def visit_pattern_element(self, node, children) -> object:
        return None

    def visit_node_pattern(self, node, children) -> object:
        return None

    def visit_pattern_element_chain(self, node, children) -> object:
        return None

    def visit_relationship_pattern(self, node, children) -> object:
        return None

    def visit_relationship_detail(self, node, children) -> object:
        return None

    def visit_properties(self, node, children) -> object:
        return None

    def visit_relationship_types(self, node, children) -> object:
        return None

    def visit_node_labels(self, node, children) -> object:
        return None

    def visit_node_label(self, node, children) -> object:
        return None

    def visit_range_literal(self, node, children) -> object:
        return None

    def visit_label_name(self, node, children) -> object:
        return None

    def visit_rel_type_name(self, node, children) -> object:
        return None

    def visit_expression(self, node, children) -> object:
        return None

    def visit_or_expression(self, node, children) -> object:
        return None

    def visit_xor_expression(self, node, children) -> object:
        return None

    def visit_and_expression(self, node, children) -> object:
        return None

    def visit_not_expression(self, node, children) -> object:
        return None

    def visit_comparison_expression(self, node, children) -> object:
        return None

    def visit_add_or_subtract_expression(self, node, children) -> object:
        return None

    def visit_multiply_divide_modulo_expression(self, node, children) -> object:
        return None

    def visit_power_of_expression(self, node, children) -> object:
        return None

    def visit_unary_add_or_subtract_expression(self, node, children) -> object:
        return None

    def visit_string_list_null_operator_expression(self, node, children) -> object:
        return None

    def visit_property_or_labels_expression(self, node, children) -> object:
        return None

    def visit_atom(self, node, children) -> object:
        return None

    def visit_literal(self, node, children) -> object:
        return None

    def visit_boolean_literal(self, node, children) -> object:
        return None

    def visit_list_literal(self, node, children) -> object:
        return None

    def visit_partial_comparison_expression(self, node, children) -> object:
        return None

    def visit_parenthesized_expression(self, node, children) -> object:
        return None

    def visit_relationships_pattern(self, node, children) -> object:
        return None

    def visit_filter_expression(self, node, children) -> object:
        return None

    def visit_id_in_coll(self, node, children) -> object:
        return None

    def visit_function_invocation(self, node, children) -> object:
        return None

    def visit_function_name(self, node, children) -> object:
        return None

    def visit_explicit_procedure_invocation(self, node, children) -> object:
        return None

    def visit_implicit_procedure_invocation(self, node, children) -> object:
        return None

    def visit_procedure_result_field(self, node, children) -> object:
        return None

    def visit_procedure_name(self, node, children) -> object:
        return None

    def visit_namespace(self, node, children) -> object:
        return None

    def visit_list_comprehension(self, node, children) -> object:
        return None

    def visit_pattern_comprehension(self, node, children) -> object:
        return None

    def visit_property_lookup(self, node, children) -> object:
        return None

    def visit_case_expression(self, node, children) -> object:
        return None

    def visit_case_alternatives(self, node, children) -> object:
        return None

    def visit_variable(self, node, children) -> object:
        return None

    def visit_string_literal(self, node, children) -> object:
        return None

    def visit_escaped_char(self, node, children) -> object:
        return None

    def visit_number_literal(self, node, children) -> object:
        return None

    def visit_map_literal(self, node, children) -> object:
        return None

    def visit_parameter(self, node, children) -> object:
        return None

    def visit_property_expression(self, node, children) -> object:
        return None

    def visit_property_key_name(self, node, children) -> object:
        return None

    def visit_integer_literal(self, node, children) -> object:
        return None

    def visit_hex_integer(self, node, children) -> object:
        return None

    def visit_decimal_integer(self, node, children) -> object:
        return None

    def visit_octal_integer(self, node, children) -> object:
        return None

    def visit_hex_digit(self, node, children) -> object:
        return None

    def visit_hex_letter(self, node, children) -> object:
        return None

    def visit_oct_digit(self, node, children) -> object:
        return None

    def visit_digit(self, node, children) -> object:
        return None

    def visit_zero_digit(self, node, children) -> object:
        return None

    def visit_non_zero_digit(self, node, children) -> object:
        return None

    def visit_non_zero_oct_digit(self, node, children) -> object:
        return None

    def visit_double_literal(self, node, children) -> object:
        return None

    def visit_exponent_decimal_real(self, node, children) -> object:
        return None

    def visit_regular_decimal_real(self, node, children) -> object:
        return None

    def visit_schema_name(self, node, children) -> object:
        return None

    def visit_reserved_word(self, node, children) -> object:
        return None

    def visit_symbolic_name(self, node, children) -> object:
        return None

    def visit_unescaped_symbolic_name(self, node, children) -> object:
        return None

    def visit_escaped_symbolic_name(self, node, children) -> object:
        return None

    def visit_left_arrow_head(self, node, children) -> object:
        return None

    def visit_right_arrow_head(self, node, children) -> object:
        return None

    def visit_dash(self, node, children) -> object:
        return None

    def visit_comment(self, node, children) -> object:
        return None
