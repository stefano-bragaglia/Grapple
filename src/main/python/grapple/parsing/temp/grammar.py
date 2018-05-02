from arpeggio import EOF, OneOrMore, Optional, RegExMatch, ZeroOrMore


def knowledge():
    return Optional(clause_list), Optional(";"), EOF


def clause_list():
    return clause, ZeroOrMore(";", clause)


def clause():
    # return [clause_reading, clause_updating]
    return clause_reading


def clause_reading():
    return rule_part, ZeroOrMore(reading_part), return_part


# def clause_updating():
#     return rule_part, ZeroOrMore(reading_part), OneOrMore(updating_part), Optional(return_part)


# def updating_part():
#     return [create, merge, delete, set_, remove]


def reading_part():
    # return [match, unwind, in_query_call]
    return match_part


# ----------------------------------------------------------------------------------------------------------------------
def rule_part():
    return _(r"RULE"), Optional(json_key), Optional(salience)


def salience():
    return _(r"SALIENCE"), json_integer


# ----------------------------------------------------------------------------------------------------------------------
def match_part():
    return Optional(optional), match  # , Optional(where)


def optional():
    return _(r"OPTIONAL")


def match():
    return _(r"MATCH"), pattern_list


def pattern_list():
    return pattern, ZeroOrMore(",", pattern)


def pattern():
    return Optional(variable, "="), pattern_anonymous


def pattern_anonymous():
    return pattern_start, Optional(pattern_chain)


def pattern_start():
    return node_pattern


def pattern_chain():
    return OneOrMore(pattern_next)


def pattern_next():
    return relation_pattern, node_pattern


def node_pattern():
    return "(", Optional(variable), Optional(labels), Optional(properties), ")"


def relation_pattern():
    return [relation_pattern_both, relation_pattern_back, relation_pattern_next, relation_pattern_none]


def relation_pattern_both():
    return "<-", Optional(relation_details), "->"


def relation_pattern_back():
    return "<-", Optional(relation_details), "-"


def relation_pattern_next():
    return "-", Optional(relation_details), "->"


def relation_pattern_none():
    return "-", Optional(relation_details), "-"


def relation_details():
    return "[", Optional(variable), Optional(types), Optional(properties), "]"


def labels():
    return tag_list


def types():
    return tag_list


def tag_list():
    return OneOrMore(tag)


def properties():
    return json_properties


# ----------------------------------------------------------------------------------------------------------------------
def return_part():
    return _(r"RETURN"), Optional(distinct), return_item_list, Optional(order), Optional(skip), Optional(limit)


def distinct():
    return _(r"DISTINCT")


def return_item_list():
    return return_first, ZeroOrMore(",", return_item)


def return_first():
    return [return_all, return_item]


def return_all():
    return "*"


def return_item():
    return [return_coalesce, return_keys, return_properties, return_id, return_labels, return_types, return_tail,
            return_head, return_selector, return_value]


def return_coalesce():
    return _(r"COALESCE"), "(", variable, ".", json_key, ",", json_value, ")", Optional(_(r"AS"), identifier)


def return_keys():
    return _(r"KEYS"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_properties():
    return _(r"PROPERTIES"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_id():
    return _(r"ID"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_labels():
    return _(r"LABELS"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_types():
    return _(r"TYPES"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_tail():
    return _(r"TAIL"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_head():
    return _(r"HEAD"), "(", variable, ")", Optional(_(r"AS"), identifier)


def return_selector():
    return variable, Optional(".", json_key), Optional(_(r"AS"), identifier)


def return_value():
    return json_value, Optional(_(r"AS"), identifier)


def order():
    return _(r"ORDER"), _(r"BY"), order_item_list


def order_item_list():
    return order_item, ZeroOrMore(",", order_item)


def order_item():
    return [selector, identifier], Optional(ordering)


def selector():
    return variable, Optional(".", json_key)


def ordering():
    return [_(r"ASC"), _(r"ASCENDING"), _(r"DESC"), _(r"DESCENDING")]


def limit():
    return _(r"LIMIT"), json_integer


def skip():
    return _(r"SKIP"), json_integer


# ----------------------------------------------------------------------------------------------------------------------
def json_properties():
    return "{", Optional(json_member_list), "}"


def json_member_list():
    return json_member, ZeroOrMore(",", json_member)


def json_member():
    return json_key, ":", json_value


def json_key():
    return [identifier, json_string_single, json_string_double]


def json_value():
    return [json_string, json_real, json_integer, json_properties, json_array, true, false, null]


def json_string():
    return [json_string_single, json_string_double]


def json_string_single():
    return '"', RegExMatch(r'[^"]*'), '"'


def json_string_double():
    return "'", RegExMatch(r"[^']*"), "'"


def json_integer():
    return RegExMatch(r"-?\d+")


def json_real():
    return RegExMatch(r"-?\d*\.\d+(E-?\d+)?")


def json_array():
    return "[", Optional(json_element_list), "]"


def json_element_list():
    return json_value, ZeroOrMore(",", json_value)


# ----------------------------------------------------------------------------------------------------------------------
def true():
    return RegExMatch(r"TRUE", ignore_case=True)


def false():
    return RegExMatch(r"FALSE", ignore_case=True)


def null():
    return RegExMatch(r"NULL", ignore_case=True)


# ----------------------------------------------------------------------------------------------------------------------
def identifier():
    return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]*")


# def parameter():
#     return RegExMatch(r"\$[A-Za-z_][A-Za-z_0-9]*")


def tag():
    return RegExMatch(r":[A-Za-z_][A-Za-z_0-9]*")


def variable():
    return RegExMatch(r"\$[A-Za-z_][A-Za-z_0-9]*")
    # return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]*")


# ----------------------------------------------------------------------------------------------------------------------
def comment():
    return [RegExMatch(r"//.*"), RegExMatch(r"/\*.*\*/", multiline=True)]


# ----------------------------------------------------------------------------------------------------------------------
def _(name):
    return RegExMatch(name, ignore_case=True)

# parser = ParserPython(base, comment)
