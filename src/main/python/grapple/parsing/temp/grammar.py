from arpeggio import EOF, OneOrMore, Optional, RegExMatch, ZeroOrMore


def resource():
    return ZeroOrMore(statement), EOF


def statement():
    return single_query, ";"


def single_query():
    return ZeroOrMore(match_body), return_body


# def single_query():
#     return [reading_clause, updating_clause]


# def reading_clause():
#     return ZeroOrMore(reading_body), return_body


# def updating_clause():
#     return ZeroOrMore(reading_body), OneOrMore(updating_body), Optional(return_body)


# def updating_body():
#     return [create, merge, delete, set_, remove]


# def reading_body():
#     return [match, unwind, in_query_call]
# ----------------------------------------------------------------------------------------------------------------------
def match_body():
    return Optional(_(r"OPTIONAL")), _(r"MATCH"), pattern_list  # , Optional(where)


def pattern_list():
    return pattern, ZeroOrMore(",", pattern)


def pattern():
    return Optional(variable, "="), anonymous_pattern


def anonymous_pattern():
    return node_pattern, Optional(pattern_chain)


def pattern_chain():
    return OneOrMore(pattern_next)


def pattern_next():
    return relation_pattern, node_pattern


def node_pattern():
    return "(", Optional(variable), Optional(tags), Optional(properties), ")"


def relation_pattern():
    return [relation_both_pattern, relation_back_pattern, relation_next_pattern, relation_none_pattern]


def relation_both_pattern():
    return "<-", Optional(relation_details), "->"


def relation_back_pattern():
    return "<-", Optional(relation_details), "-"


def relation_next_pattern():
    return "-", Optional(relation_details), "->"


def relation_none_pattern():
    return "-", Optional(relation_details), "-"


def relation_details():
    return "[", Optional(variable), Optional(tags), Optional(properties), "]"


def tags():
    return OneOrMore(tag)


# ----------------------------------------------------------------------------------------------------------------------
def return_body():
    return _(r"RETURN"), Optional(_(r"DISTINCT")), return_items, Optional(order), Optional(skip), Optional(limit)


def limit():
    return _(r"LIMIT"), integer


def skip():
    return _(r"SKIP"), integer


def order():
    return _(r"ORDER"), _(r"BY"), order_items


def order_items():
    return order_item, ZeroOrMore(",", order_item)


def order_item():
    return variable, Optional(".", key), Optional(ordering)


def ordering():
    return [_(r"ASC"), _(r"ASCENDING"), _(r"DESC"), _(r"DESCENDING")]


def return_items():
    return [return_all, return_item], ZeroOrMore(return_item)


def return_all():
    return "*"


def return_item():
    return [return_coalesce, return_keys, return_properties, return_id, return_labels, return_types, return_tail,
            return_head, return_selector, return_value]


def return_coalesce():
    return _(r"COALESCE"), "(", variable, ".", key, ",", value, ")", Optional(_(r"AS"), identifier)


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
    return variable, Optional(".", key), Optional(_(r"AS"), identifier)


def return_value():
    return value, Optional(_(r"AS"), identifier)


# ----------------------------------------------------------------------------------------------------------------------
def properties():
    return "{", Optional(members), "}"


def members():
    return member, ZeroOrMore(",", member)


def member():
    return key, ":", value


def key():
    return [identifier, single, double]


def value():
    return [string, integer, real, properties, array, true, false, null]


def string():
    return [single, double]


def single():
    return '"', RegExMatch(r'[^"]*'), '"'


def double():
    return "'", RegExMatch(r"[^']*"), "'"


def integer():
    return RegExMatch(r"-?\d+")


def real():
    return RegExMatch(r"-?\d*\.\d+"), Optional(RegExMatch(r"E-?\d+"))


def array():
    return "[", Optional(elements), "]"


def elements():
    return value, ZeroOrMore(",", value)


def true():
    return RegExMatch(r"TRUE", ignore_case=True)


def false():
    return RegExMatch(r"FALSE", ignore_case=True)


def null():
    return RegExMatch(r"NULL", ignore_case=True)


# ----------------------------------------------------------------------------------------------------------------------
def identifier():
    return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]")


def parameter():
    return RegExMatch(r"\$[A-Za-z_][A-Za-z_0-9]")


def tag():
    return RegExMatch(r":[A-Za-z_][A-Za-z_0-9]")


def variable():
    return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]")


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def comment(): return [RegExMatch(r"//.*"), RegExMatch(r"/\*.*\*/", multiline=True)]


# ----------------------------------------------------------------------------------------------------------------------
def _(name):
    return RegExMatch(name, ignore_case=True)

# parser = ParserPython(base, comment)
