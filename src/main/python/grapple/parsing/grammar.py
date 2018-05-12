from arpeggio import EOF, OneOrMore, Optional, RegExMatch, ZeroOrMore

"""
// clause <- clause_reading / clause updating ;
// clause_reading <- rule_part reading_part* return_part ;
// clause_updating <- rule_part reading_part* updating_part+ return_part? ;
// reading_part <- match_part / unwind_part / in_query_call_part ;
// updating_part <- create_part / merge_part / delete_part / set_part / remove_part ;
"""


def comment():
    return [RegExMatch("//.*"), RegExMatch("/\*.*\*/", multiline=True)]


def knowledge():
    return Optional(clauses), Optional(';'), EOF


def clauses():
    return clause, ZeroOrMore(';', clause)


def clause():
    return rule_part(), Optional(match_parts), return_part


def rule_part():
    return rule_description, Optional(rule_salience)


def rule_description():
    return key_rule, Optional(json_string)


def rule_salience():
    return key_salience, json_integer


def match_parts():
    return OneOrMore(match_part)


def match_part():
    return Optional(match_optional), match_patterns


def match_optional():
    return key_optional


def match_patterns():
    return key_match, match_pattern, ZeroOrMore(',', match_pattern)


def match_pattern():
    return Optional(return_parameter, '='), match_anonymous


def match_anonymous():
    return match_start, ZeroOrMore(match_chain)


def match_start():
    return match_node


def match_chain():
    return match_relation, match_node


def match_node():
    return '(', Optional(return_parameter), Optional(match_labels), Optional(match_properties), ')'


def match_relation():
    return [match_both, match_back, match_next, match_none]


def match_both():
    return '<-', Optional(match_details), '->'


def match_back():
    return '<-', Optional(match_details), '-'


def match_next():
    return '-', Optional(match_details), '->'


def match_none():
    return '-', Optional(match_details), '-'


def match_details():
    return '[', Optional(return_parameter), Optional(match_types), Optional(match_properties), ']'


def match_properties():
    return json_object()


def match_labels():
    return OneOrMore(':', identifier)


def match_types():
    return OneOrMore(':', identifier)


# ----------------------------------------------------------------------------------------------------------------------
def return_part():
    return key_return, Optional(return_distinct), return_items, Optional(return_order_by), Optional(
        return_skip), Optional(return_limit)


def return_distinct():
    return key_distinct


def return_items():
    return return_first, ZeroOrMore(',', return_item)


def return_first():
    return [return_item, return_all]


def return_item():
    return [return_coalesce, return_keys, return_properties, return_id, return_labels, return_types,
            return_tail, return_head, return_selector, return_value]


def return_all():
    return '*'


def return_coalesce():
    return key_coalesce, '(', return_parameter, return_property, Optional(return_default), ')', Optional(return_synonym)


def return_default():
    return ',', json_value


def return_keys():
    return key_keys, '(', return_parameter, ')', Optional(return_synonym)


def return_properties():
    return key_properties, '(', return_parameter, ')', Optional(return_synonym)


def return_id():
    return key_id, '(', return_parameter, ')', Optional(return_synonym)


def return_labels():
    return key_labels, '(', return_parameter, ')', Optional(return_synonym)


def return_types():
    return key_types, '(', return_parameter, ')', Optional(return_synonym)


def return_tail():
    return key_tail, '(', return_parameter, ')', Optional(return_synonym)


def return_head():
    return key_head, '(', return_parameter, ')', Optional(return_synonym)


def return_selector():
    return return_order_by_selector, Optional(return_synonym)


def return_value():
    return json_value, Optional(return_synonym)


def return_synonym():
    return key_as, json_key


def return_order_by():
    return key_order, key_by, return_order_by_items


def return_order_by_items():
    return return_order_by_item, ZeroOrMore(',', return_order_by_item)


def return_order_by_item():
    return [return_order_by_selector, return_order_by_name], Optional(return_ordering)


def return_order_by_selector():
    return return_parameter, Optional(return_property)


def return_parameter():
    return parameter


def return_property():
    return '.', json_key


def return_order_by_name():
    return json_key


def return_ordering():
    return [return_ordering_ascending, return_ordering_descending]


def return_ordering_ascending():
    return [key_asc, key_ascending]


def return_ordering_descending():
    return [key_desc, key_descending]


def return_skip():
    return key_skip, json_integer


def return_limit():
    return key_limit, json_integer


def json_object():
    return '{', Optional(json_members), '}'


def json_members():
    return json_member, ZeroOrMore(',', json_member)


def json_member():
    return json_key, ':', json_value


def json_key():
    return [json_string, identifier]


def json_value():
    return [json_string, json_real, json_integer, json_object, json_array, json_true, json_false, json_null, parameter]


def json_string():
    return [("'", RegExMatch(r"[^']*"), "'"), ('"', RegExMatch(r'[^"]*'), '"')]


def json_integer():
    return RegExMatch(r'-?\d+')


def json_real():
    return RegExMatch(r'-?\d*\.\d+(E-?\d+)?', ignore_case=True)


def json_array():
    return '[', Optional(json_elements), ']'


def json_elements():
    return json_value, ZeroOrMore(',', json_value)


def json_true():
    return RegExMatch(r'true', ignore_case=True)


def json_false():
    return RegExMatch(r'false', ignore_case=True)


def json_null():
    return RegExMatch(r'null', ignore_case=True)


def identifier():
    return RegExMatch(r'[A-Za-z_][A-Za-z_0-9]*')


def parameter():
    return RegExMatch(r'\$[A-Za-z_0-9]+')


def key_as():
    return RegExMatch(r'AS', ignore_case=True)


def key_asc():
    return RegExMatch(r'ASC', ignore_case=True)


def key_ascending():
    return RegExMatch(r'ASCENDING', ignore_case=True)


def key_by():
    return RegExMatch(r'BY', ignore_case=True)


def key_coalesce():
    return RegExMatch(r'coalesce', ignore_case=True)


def key_desc():
    return RegExMatch(r'DESC', ignore_case=True)


def key_descending():
    return RegExMatch(r'DESCENDING', ignore_case=True)


def key_distinct():
    return RegExMatch(r'DISTINCT', ignore_case=True)


def key_head():
    return RegExMatch(r'head', ignore_case=True)


def key_id():
    return RegExMatch(r'id', ignore_case=True)


def key_keys():
    return RegExMatch(r'keys', ignore_case=True)


def key_labels():
    return RegExMatch(r'labels', ignore_case=True)


def key_limit():
    return RegExMatch(r'LIMIT', ignore_case=True)


def key_match():
    return RegExMatch(r'MATCH', ignore_case=True)


def key_optional():
    return RegExMatch(r'OPTIONAL', ignore_case=True)


def key_order():
    return RegExMatch(r'ORDER', ignore_case=True)


def key_properties():
    return RegExMatch(r'properties', ignore_case=True)


def key_return():
    return RegExMatch(r'RETURN', ignore_case=True)


def key_rule():
    return RegExMatch(r'RULE', ignore_case=True)


def key_salience():
    return RegExMatch(r'SALIENCE', ignore_case=True)


def key_skip():
    return RegExMatch(r'SKIP', ignore_case=True)


def key_tail():
    return RegExMatch(r'tail', ignore_case=True)


def key_types():
    return RegExMatch(r'types', ignore_case=True)
