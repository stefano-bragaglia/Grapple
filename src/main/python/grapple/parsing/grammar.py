from arpeggio import EOF, Optional, ZeroOrMore, OneOrMore, RegExMatch


def _(name: str):
    return _(name)


def resource(): return ZeroOrMore(statement), EOF


def statement(): return part_rule, Optional(part_match), part_return, ";"


def part_rule(): return description, Optional(salience)


def description(): return key_rule, Optional(json_string)


def salience(): return key_salience, json_number


def part_match(): return OneOrMore(key_match, path)


def path(): return node, ZeroOrMore(relation, node)


def relation(): return [relation_rwd, relation_fwd, relation_any]


def relation_rwd(): return "<-", Optional(relation_def), "-"


def relation_fwd(): return "-", Optional(relation_def), "->"


def relation_any(): return "-", Optional(relation_def), "-"


def relation_def(): return "[", Optional(assignment), Optional(flags), Optional(attributes), "]"


def node(): return "(", Optional(assignment), Optional(flags), Optional(attributes), ")"


def assignment(): return variable


def flags(): return flag, ZeroOrMore(flag)


def attributes(): return json_object


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


def part_return():
    return _(r"RETURN"), Optional(_(r"DISTINCT")), return_body


def return_body():
    return return_items, Optional(order), Optional(skip), Optional(limit)


def return_items():
    return ["*", return_item], ZeroOrMore(",", return_item)


def return_item():
    return expression, Optional(_(r"AS"), variable)


def order():
    return _(r"ORDER"), _(r"BY"), sort_items


def sort_items():
    return sort_item, ZeroOrMore(",", sort_item)


def sort_item():
    return expression, Optional([_(r"ASCENDING"), _(r"ASC"), _(r"DESCENDING"), _(r"DESC")])


def skip():
    return _(r"SKIP"), expression


def limit():
    return _(r"LIMIT"), expression


# ----------------------------------------------------------------------------------------------------------------------

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


def number_literal():
    return [double_literal, integer_literal]


def double_literal():
    return [exponent_decimal_real, regular_decimal_real]


def exponent_decimal_real():
    return [
               OneOrMore(digit),
               (OneOrMore(digit), ".", OneOrMore(digit)),
               (".", OneOrMore(digit))
           ], [
               _(r"E"),
               (_(r"E"), Optional("-"), OneOrMore(digit))
           ]


def regular_decimal_real():
    return [ZeroOrMore(digit), (".", OneOrMore(digit))]


def integer_literal():
    return [hex_integer, octal_integer, decimal_integer]


def hex_integer():
    return "0x", OneOrMore(hex_digit)


def hex_digit():
    return [digit, hex_letter]


def digit():
    return [zero_digit, non_zero_digit]


def zero_digit():
    return "0"


def non_zero_digit():
    return [non_zero_oct_digit, "8", "9"]


def non_zero_oct_digit():
    return ["1", "2", "3", "4", "5", "6", "7"]


def hex_letter():
    return _(r"[A-F]")


def octal_integer():
    return zero_digit, OneOrMore(oct_digit)


def oct_digit():
    return [zero_digit, non_zero_oct_digit]


def decimal_integer():
    return [zero_digit, (non_zero_digit, ZeroOrMore(digit))]


def string_literal():
    return [
        ('"', ZeroOrMore([_(r'[^"]*'), escaped_char]), '"'),
        ("'", ZeroOrMore([_(r"[^']*"), escaped_char]), "'")
    ]


def escaped_char():
    return [
        "\\\\",
        "\\'",
        '\\"',
        _(r"\\b"),
        _(r"\\f"),
        _(r"\\n"),
        _(r"\\t"),
        (_(r"\\U"), (hex_digit, hex_digit, hex_digit, hex_digit)),
        (_(r"\\U"), (hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit, hex_digit))
    ]


def boolean_literal():
    return [_(r"TRUE"), _(r"FALSE")]


def map_literal():
    return "{", Optional(property_key_name, ":", expression, ZeroOrMore(",", property_key_name, ":", expression)), "}"


def property_key_name():
    return schema_name


def schema_name():
    return [symbolic_name, reserved_word]


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
    return _(r"[a-zA-Z_][0-9A-Za-z_$]*")


def escaped_symbolic_name():
    return OneOrMore("`", _(r"[^`]*"), "`")


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


def list_literal():
    return "[", ZeroOrMore(expression, Optional(",", expression)), "]"


def parameter():
    return "$", [symbolic_name, decimal_integer]


def case_expression():
    return [
               (_(r"CASE"), OneOrMore(case_alternatives)),
               (_(r"CASE"), expression, OneOrMore(case_alternatives))
           ], Optional(_(r"ELSE"), expression), _(r"END")


def case_alternatives():
    return _(r"WHEN"), expression, _(r"THEN"), expression


def list_comprehension():
    return "[", filter_expression, Optional("|", expression), "]"


def filter_expression():
    return id_in_coll, Optional(where)


def id_in_coll():
    return variable, _(r"IN"), expression


def variable():
    return symbolic_name


def where():
    return _(r"WHERE"), expression


def pattern_comprehension():
    return "[", Optional(variable, "="), relationships_pattern, Optional(_(r"WHERE"), expression), "|", expression, "]"


def relationships_pattern():
    return node_pattern, OneOrMore(pattern_element_chain)


def node_pattern():
    return "(", Optional(variable), Optional(node_labels), Optional(properties), ")"


def node_labels():
    return node_label, ZeroOrMore(node_label)


def node_label():
    return ":", label_name


def label_name():
    return schema_name


def properties():
    return [map_literal, parameter]


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


def relationship_types():
    return ":", rel_type_name, ZeroOrMore("|", Optional(":"), rel_type_name)


def rel_type_name():
    return schema_name


def range_literal():
    return "*", Optional(integer_literal), Optional("..", Optional(integer_literal))


def parenthesized_expression():
    return "(", expression, ")"


def function_invocation():
    return function_name, "(", Optional(_(r"DISTINCT")), Optional(expression, ZeroOrMore(",", expression)), ")"


def function_name():
    return [symbolic_name, _(r"EXISTS")]


def property_lookup():
    return ".", property_key_name


def partial_comparison_expression():
    return [
        ("=", add_or_subtract_expression),
        ("<>", add_or_subtract_expression),
        ("<", add_or_subtract_expression),
        (">", add_or_subtract_expression),
        ("<=", add_or_subtract_expression),
        (">=", add_or_subtract_expression)
    ]


def left_arrow_head():
    return ["<", "⟨", "〈", "﹤", "＜"]


def right_arrow_head():
    return [">", "⟩", "〉", "﹥", "＞"]


def dash():
    return ["-", "­", "‐", "‑", "‒", "–", "—", "―", "−", "﹘", "﹣", "－"]


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------


def return_item(): return content, synonym


def content(): return [value, labels, types, ident, accessor]


def value(): return json_value()


def labels(): return key_labels, "(", variable, ")"


def types(): return key_types, "(", variable, ")"


def ident(): return key_id, "(", variable, ")"


def accessor(): return variable, Optional(".", identifier)


def synonym(): return Optional(key_as, identifier)


def skip_body(): return key_skip,


def flag(): return _(r":[a-zA-Z]\w*")


def identifier(): return _(r"[a-zA-Z]\w*")


def variable(): return _(r"\$[a-zA-Z]\w*")


def json_object(): return "{", Optional(json_members), "}"


def json_members(): return json_member, ZeroOrMore(",", json_member)


def json_member(): return json_string, ":", json_value


def json_value(): return [json_string, json_number, json_object, json_array, key_true, key_false, key_null]


def json_string(): return '"', _('[^"]*'), '"'


def json_number(): return _('-?\d+((\.\d*)?((e|E)(\+|-)?\d+)?)?')


def json_array(): return "[", Optional(json_elements), "]"


def json_elements(): return json_value, ZeroOrMore(",", json_value)


def key_as(): return _(r"AS")


def key_distinct(): return _(r"AS")


def key_false(): return _(r"FALSE")


def key_id(): return _(r"ID")


def key_labels(): return _(r"LABELS")


def key_limit(): return _(r"LIMIT")


def key_match(): return _(r"MATCH")


def key_null(): return _(r"NULL")


def key_return(): return _(r"RETURN")


def key_rule(): return _(r"RULE")


def key_salience(): return _(r"SALIENCE")


def key_skip(): return _(r"SKIP")


def key_true(): return _(r"TRUE")


def key_types(): return _(r"TYPES")


def comment(): return [RegExMatch(r"/\*.*\*/"), RegExMatch(r"//.*")]
