from arpeggio import *


def cypher():
    return statement, Optional(";"), EOF


def statement():
    return query


def query():
    return [regular_query, standalone_call]


def regular_query():
    return single_query, ZeroOrMore(union)


def union():
    return [
        (_(r"UNION"), _(r"ALL"), single_query),
        (_(r"UNION"), single_query)
    ]


def single_query():
    return [single_part_query, multi_part_query]


def single_part_query():
    return [
        (ZeroOrMore(reading_clause), return_),
        (ZeroOrMore(reading_clause), updating_clause, ZeroOrMore(updating_clause), Optional(return_))
    ]


def multi_part_query():
    return OneOrMore(ZeroOrMore(reading_clause), ZeroOrMore(updating_clause), with_), single_part_query


def updating_clause():
    return [create, merge, delete, set_, remove]


def reading_clause():
    return [match, unwind, in_query_call]


def match():
    return Optional(_(r"OPTIONAL")), _(r"MATCH"), pattern, Optional(where)


def unwind():
    return _(r"UNWIND"), expression, _(r"AS"), variable


def merge():
    return _(r"MERGE"), pattern_part, ZeroOrMore(merge_action)


def merge_action():
    return [
        (_(r"ON"), _(r"MATCH"), set_),
        (_(r"ON"), _(r"CREATE"), set_)
    ]


def create():
    return _(r"CREATE"), pattern


def set_():
    return _(r"SET"), set_item, ZeroOrMore(",", set_item)


def set_item():
    return [
        (property_expression, "=", expression),
        (variable, "=", expression),
        (variable, "+=", expression),
        (variable, node_labels)
    ]


def delete():
    return Optional(_(r"DETACH")), _(r"DELETE"), expression, ZeroOrMore(",", expression)


def remove():
    return _(r"REMOVE"), remove_item, ZeroOrMore(",", remove_item)


def remove_item():
    return [(variable, node_labels), property_expression]


def in_query_call():
    return _(r"CALL"), explicit_procedure_invocation, Optional(_(r"YIELD"), yield_items)


def standalone_call():
    return _(r"CALL"), [
        explicit_procedure_invocation,
        implicit_procedure_invocation
    ], Optional(_(r"YIELD"), yield_items)


def yield_items():
    return [(yield_item, ZeroOrMore(",", yield_item)), "-"]


def yield_item():
    return Optional(procedure_result_field, _(r"AS")), variable


def with_():
    return _(r"WITH"), Optional(_(r"DISTINCT")), return_body, Optional(where)


def return_():
    return _(r"RETURN"), Optional(_(r"DISTINCT")), return_body


def return_body():
    return return_items, Optional(order), Optional(skip), Optional(limit)


def return_items():
    return [
        ("*", ZeroOrMore(",", return_item)),
        (return_item, ZeroOrMore(",", return_item))
    ]


def return_item():
    return expression, Optional(_(r"AS"), variable)


def order():
    return _(r"ORDER"), _(r"BY"), sort_items


def sort_items():
    return sort_item, ZeroOrMore(",", sort_item)


def skip():
    return _(r"SKIP"), expression


def limit():
    return _(r"LIMIT"), expression


def sort_item():
    return expression, Optional([_(r"ASCENDING"), _(r"ASC"), _(r"DESCENDING"), _(r"DESC")])


def where():
    return _(r"WHERE"), expression


def pattern():
    return pattern_part, ZeroOrMore(",", pattern_part)


def pattern_part():
    return [(variable, "=", anonymous_pattern_part), anonymous_pattern_part]


def anonymous_pattern_part():
    return pattern_element


def pattern_element():
    return [(node_pattern, ZeroOrMore(pattern_element_chain)), ("(", pattern_element, ")")]


def node_pattern():
    return "(", Optional(variable), Optional(node_labels), Optional(properties), ")"


def pattern_element_chain():
    return relationship_pattern, node_pattern


def relationship_pattern():
    return [
        (left_arrow_head, dash, Optional(relationship_detail), dash, right_arrow_head),
        (left_arrow_head, dash, Optional(relationship_detail), dash),
        (dash, Optional(relationship_detail), dash, right_arrow_head),
        (dash, Optional(relationship_detail), dash)
    ]


def relationship_detail():
    return "[", Optional(variable), Optional(relationship_types), Optional(range_literal), Optional(properties), "]"


def properties():
    return [map_literal, parameter]


def relationship_types():
    return ":", rel_type_name, ZeroOrMore("|", Optional(":"), rel_type_name)


def node_labels():
    return node_label, ZeroOrMore(node_label)


def node_label():
    return ":", label_name


def range_literal():
    return "*", Optional(integer_literal), Optional("..", Optional(integer_literal))


def label_name():
    return schema_name


def rel_type_name():
    return schema_name


def expression():
    return or_expression


def or_expression():
    return xor_expression, ZeroOrMore(_(r"OR"), xor_expression)


def xor_expression():
    return and_expression, ZeroOrMore(_(r"XOR"), and_expression)


def and_expression():
    return not_expression, ZeroOrMore(_(r"AND"), not_expression)


def not_expression():
    return ZeroOrMore(_(r"NOT")), comparison_expression


def comparison_expression():
    return add_or_subtract_expression, ZeroOrMore(partial_comparison_expression)


def add_or_subtract_expression():
    return multiply_divide_modulo_expression, ZeroOrMore([
        ("+", multiply_divide_modulo_expression),
        ("-", multiply_divide_modulo_expression)
    ])


def multiply_divide_modulo_expression():
    return power_of_expression, ZeroOrMore([
        ("*", power_of_expression),
        ("/", power_of_expression),
        ("%", power_of_expression)
    ])


def power_of_expression():
    return unary_add_or_subtract_expression, ZeroOrMore("^", unary_add_or_subtract_expression)


def unary_add_or_subtract_expression():
    return ZeroOrMore(["+", "-"]), string_list_null_operator_expression


def string_list_null_operator_expression():
    return property_or_labels_expression, ZeroOrMore([
        ("[", expression, "]"),
        ("[", Optional(expression), "..", Optional(expression), "]"),
        ([
             (_(r"IN")),
             (_(r"STARTS"), _(r"WITH")),
             (_(r"ENDS"), _(r"WITH")),
             (_(r"CONTAINS"))
         ], property_or_labels_expression),
        (_(r"IS"), _(r"NULL")),
        (_(r"IS"), _(r"NOT"),
         _(r"NULL"))
    ])


def property_or_labels_expression():
    return atom, ZeroOrMore(property_lookup), Optional(node_labels)


def atom():
    return [
        literal,
        parameter,
        case_expression,
        (_(r"COUNT"), "(", "*", ")"),
        list_comprehension,
        pattern_comprehension,
        (_(r"FILTER"), "(", filter_expression, ")"),
        Optional(_(r"EXTRACT"), "(", filter_expression, Optional("|", expression), ")"),
        (_(r"ALL"), "(", filter_expression, ")"),
        (_(r"ANY"), "(", filter_expression, ")"),
        (_(r"NONE"), "(", filter_expression, ")"),
        (_(r"SINGLE"), "(", filter_expression, ")"),
        relationships_pattern,
        parenthesized_expression,
        function_invocation,
        variable
    ]


def literal():
    return [
        number_literal,
        string_literal,
        boolean_literal,
        _(r"NULL"),
        map_literal,
        list_literal
    ]


def boolean_literal():
    return [_(r"TRUE"), _(r"FALSE")]


def list_literal():
    return "[", ZeroOrMore(expression, Optional(",", expression)), "]"


def partial_comparison_expression():
    return [
        ("=", add_or_subtract_expression),
        ("<>", add_or_subtract_expression),
        ("<", add_or_subtract_expression),
        (">", add_or_subtract_expression),
        ("<=", add_or_subtract_expression),
        (">=", add_or_subtract_expression)
    ]


def parenthesized_expression():
    return "(", expression, ")"


def relationships_pattern():
    return node_pattern, OneOrMore(pattern_element_chain)


def filter_expression():
    return id_in_coll, Optional(where)


def id_in_coll():
    return variable, _(r"IN"), expression


def function_invocation():
    return function_name, "(", Optional(_(r"DISTINCT")), Optional(expression, ZeroOrMore(",", expression)), ")"


def function_name():
    return [symbolic_name, _(r"EXISTS")]


def explicit_procedure_invocation():
    return procedure_name, "(", Optional(expression, ZeroOrMore(",", expression)), ")"


def implicit_procedure_invocation():
    return procedure_name


def procedure_result_field():
    return symbolic_name


def procedure_name():
    return namespace, symbolic_name


def namespace():
    return ZeroOrMore(symbolic_name, ".")


def list_comprehension():
    return "[", filter_expression, Optional("|", expression), "]"


def pattern_comprehension():
    return "[", Optional(variable, "="), relationships_pattern, Optional(_(r"WHERE"), expression), "|", expression, "]"


def property_lookup():
    return ".", property_key_name


def case_expression():
    return [
               (_(r"CASE"), OneOrMore(case_alternatives)),
               (_(r"CASE"), expression, OneOrMore(case_alternatives))
           ], Optional(_(r"ELSE"), expression), _(r"END")


def case_alternatives():
    return _(r"WHEN"), expression, _(r"THEN"), expression


def variable():
    return symbolic_name


def string_literal():
    return [
        ('"', ZeroOrMore([RegExMatch(r"[^\"]"), escaped_char]), '"'),
        ("'", ZeroOrMore([RegExMatch(r"[^']*"), escaped_char]), "'")
    ]


def escaped_char():
    return [
        "\\\\",
        "\\'",
        '\\"',
        _(r"\\b"),
        _(r"\\f"),
        _(r"\\n"),
        _(r"\\r"),
        _(r"\\t"),
        (_(r"\\u"), (hex_digit, hex_digit, hex_digit, hex_digit)),
        (_(r"\\u"), (hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit))
    ]


def number_literal():
    return [double_literal, integer_literal]


def map_literal():
    return "{", Optional(property_key_name, ":", expression, ZeroOrMore(",", property_key_name, ":", expression)), "}"


def parameter():
    return "$", [symbolic_name, decimal_integer]


def property_expression():
    return atom, OneOrMore(property_lookup)


def property_key_name():
    return schema_name


def integer_literal():
    return [hex_integer, octal_integer, decimal_integer]


def hex_integer():
    return "0x", OneOrMore(hex_digit)


def decimal_integer():
    return [zero_digit, (non_zero_digit, ZeroOrMore(digit))]


def octal_integer():
    return zero_digit, OneOrMore(oct_digit)


def hex_digit():
    return [digit, hex_letter]


def hex_letter():
    return _(r"[A-F]")


def oct_digit():
    return [zero_digit, non_zero_oct_digit]


def digit():
    return [zero_digit, non_zero_digit]


def zero_digit():
    return "0"


def non_zero_digit():
    return [non_zero_oct_digit, "8", "9"]


def non_zero_oct_digit():
    return ["1", "2", "3", "4", "5", "6", "7"]


def double_literal():
    return [exponent_decimal_real, regular_decimal_real]


def exponent_decimal_real():
    return [
               OneOrMore(digit),
               (OneOrMore(digit), ".", OneOrMore(digit)),
               (".", OneOrMore(digit))
           ], [_(r"e"), (_(r"e"), Optional("-"), OneOrMore(digit))]


def regular_decimal_real():
    return [ZeroOrMore(digit), (".", OneOrMore(digit))]


def schema_name():
    return [symbolic_name, reserved_word]


def reserved_word():
    return [
        _(r"ALL"),
        _(r"ASC"),
        _(r"ASCENDING"),
        _(r"BY"),
        _(r"CREATE"),
        _(r"DELETE"),
        _(r"DESC"),
        _(r"DESCENDING"),
        _(r"DETACH"),
        _(r"EXISTS"),
        _(r"LIMIT"),
        _(r"MATCH"),
        _(r"MERGE"),
        _(r"ON"),
        _(r"OPTIONAL"),
        _(r"ORDER"),
        _(r"REMOVE"),
        _(r"RETURN"),
        _(r"SET"),
        _(r"SKIP"),
        _(r"WHERE"),
        _(r"WITH"),
        _(r"UNION"),
        _(r"UNWIND"),
        _(r"AND"),
        _(r"AS"),
        _(r"CONTAINS"),
        _(r"DISTINCT"),
        _(r"ENDS"),
        _(r"IN"),
        _(r"IS"),
        _(r"NOT"),
        _(r"OR"),
        _(r"STARTS"),
        _(r"XOR"),
        _(r"FALSE"),
        _(r"TRUE"),
        _(r"NULL"),
        _(r"CONSTRAINT"),
        _(r"DO"),
        _(r"FOR"),
        _(r"REQUIRE"),
        _(r"UNIQUE"),
        _(r"CASE"),
        _(r"WHEN"),
        _(r"THEN"),
        _(r"ELSE"),
        _(r"END"),
        _(r"MANDATORY"),
        _(r"SCALAR"),
        _(r"OF"),
        _(r"ADD"),
        _(r"DROP")
    ]


def symbolic_name():
    return [
        unescaped_symbolic_name,
        escaped_symbolic_name,
        hex_letter,
        _(r"COUNT"),
        _(r"FILTER"),
        _(r"EXTRACT"),
        _(r"ANY"),
        _(r"NONE"),
        _(r"SINGLE")
    ]


def unescaped_symbolic_name():
    return RegExMatch(r"[a-zA-Z_][0-9A-Za-z_$]*")


def escaped_symbolic_name():
    return OneOrMore("`", RegExMatch(r"[^`]*"), "`")


def left_arrow_head():
    return ["<", "⟨", "〈", "﹤", "＜"]


def right_arrow_head():
    return [">", "⟩", "〉", "﹥", "＞"]


def dash():
    return ["-", "­", "‐", "‑", "‒", "–", "—", "―", "−", "﹘", "﹣", "－"]


def comment():
    return [RegExMatch(r"/\*.*\*/"), RegExMatch(r"//.*")]


def _(name: str):
    return RegExMatch(name, ignore_case=True)
