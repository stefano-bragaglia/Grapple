from arpeggio import Optional, RegExMatch, ZeroOrMore


def where():
    return RegExMatch(r"WHERE", ignore_case=True), expression


def expression():
    return or_expression


def or_expression():
    return xor_expression, ZeroOrMore(RegExMatch(r"OR", ignore_case=True), xor_expression)


def xor_expression():
    return and_expression, ZeroOrMore(RegExMatch(r"XOR", ignore_case=True), and_expression)


def and_expression():
    return not_expression, ZeroOrMore(RegExMatch(r"AND", ignore_case=True), not_expression)


def not_expression():
    return ZeroOrMore(RegExMatch(r"NOT", ignore_case=True)), comparison_expression


def comparison_expression():
    return add_or_subtract_expression, ZeroOrMore(partial_comparison_expression)


def partial_comparison_expression():
    pass


def add_or_subtract_expression():
    return multiply_divide_modulo_expression, ZeroOrMore(["+", "-"], multiply_divide_modulo_expression)


def multiply_divide_modulo_expression():
    return power_of_expression, ZeroOrMore(["*", "/", "%"], power_of_expression)


def power_of_expression():
    return unary_add_or_subtract_expression, ZeroOrMore("^", unary_add_or_subtract_expression)


def unary_add_or_subtract_expression():
    return ZeroOrMore(["+", "-"]), string_list_null_operator_expression


def string_list_null_operator_expression():
    return property_or_labels_expression, ZeroOrMore(
        [squared_expression, interval_expression, inline_expression, is_null, is_not_null])


def property_or_labels_expression():
    pass


def squared_expression():
    return "[", expression, "]"


def interval_expression():
    return "[", Optional(expression), "..", Optional(expression), "]"


def inline_expression():
    return [key_in, starts_with, ends_with, key_contains], property_or_labels_expression


def starts_with():
    return key_starts, key_with


def ends_with():
    return key_ends, key_with


def is_null():
    return key_is, key_null


def is_not_null():
    return key_is, key_not, key_null


def key_contains():
    return RegExMatch(r"CONTAINS", ignore_case=True)


def key_ends():
    return RegExMatch(r"ENDS", ignore_case=True)


def key_in():
    return RegExMatch(r"IN", ignore_case=True)


def key_is():
    return RegExMatch(r"IS", ignore_case=True)


def key_not():
    return RegExMatch(r"NOT", ignore_case=True)


def key_null():
    return RegExMatch(r"NULL", ignore_case=True)


def key_starts():
    return RegExMatch(r"STARTS", ignore_case=True)


def key_with():
    return RegExMatch(r"WITH", ignore_case=True)
