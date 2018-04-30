from arpeggio import EOF, OneOrMore, Optional, ParserPython, RegExMatch, ZeroOrMore


def _(name):
    return RegExMatch(name, ignore_case=True)


def resource():
    return ZeroOrMore(single_query), EOF


def statement():
    return single_query, ";"


def single_query():
    return [reading_clause, updating_clause]


def reading_clause():
    return ZeroOrMore(reading_body), return_body


def updating_clause():
    return ZeroOrMore(reading_body), OneOrMore(updating_body), Optional(return_body)


def updating_body():
    return [create, merge, delete, set_, remove]


def reading_body():
    return [match, unwind, in_query_call]


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

def properties():
    return "{", Optional(members), "}"


def members():
    return member, ZeroOrMore(",", member)


def member():
    return string, ":", value


def value():
    return [string, integer, real, properties, array, key_true, key_false, key_null]


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

def literal():
    return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]")


def parameter():
    return RegExMatch(r"\$[A-Za-z_][A-Za-z_0-9]")


def tag():
    return RegExMatch(r":[A-Za-z_][A-Za-z_0-9]")


def variable():
    return RegExMatch(r"[A-Za-z_][A-Za-z_0-9]")


# ----------------------------------------------------------------------------------------------------------------------

def comment(): return [RegExMatch(r"//.*"), RegExMatch(r"/\*.*\*/", multiline=True)]


# ----------------------------------------------------------------------------------------------------------------------


def base(): ZeroOrMore(rule), EOF


def rule(): return match_, pattern, return_, requests, ";"


def match_(): return RegExMatch(r"MATCH", ignore_case=True)


def pattern(): return node, ZeroOrMore(relation, node)


def node(): return "(", Optional(variable), Optional(labels), Optional(json_object), ")"


def labels(): return label, ZeroOrMore(label)


def relation(): return [relation_rwd, relation_fwd, relation_any]


def relation_rwd(): return "<-", Optional(relation_def), "-"


def relation_fwd(): return "-", Optional(relation_def), "->"


def relation_any(): return "-", Optional(relation_def), "-"


def relation_def(): return "[", Optional(variable), Optional(labels), Optional(json_object), "]"


def variable(): return RegExMatch(r"\$[a-zA-Z]\w*")


def label(): return RegExMatch(r":[a-zA-Z]\w*")


def json_object(): return "{", Optional(json_members), "}"


def json_members(): return json_member, ZeroOrMore(",", json_member)


def json_member(): return json_string, ":", json_value


def json_value(): return [json_string, json_number, json_object, json_array, true_, false_, null_]


def json_string(): return '"', RegExMatch('[^"]*'), '"'


def json_number(): return RegExMatch('-?\d+((\.\d*)?((e|E)(\+|-)?\d+)?)?')


def json_array(): return "[", Optional(json_elements), "]"


def json_elements(): return json_value, ZeroOrMore(",", json_value)


def true_(): return RegExMatch(r"TRUE", ignore_case=True)


def false_(): return RegExMatch(r"FALSE", ignore_case=True)


def null_(): return RegExMatch(r"NULL", ignore_case=True)


def return_(): return RegExMatch(r"RETURN", ignore_case=True)


def requests(): return request, ZeroOrMore(",", request)


def request(): return [identifier, constant], Optional(as_, symbol)


def constant(): return json_value


def identifier(): return reference, Optional(field)


def reference(): return variable


def field(): return RegExMatch(r"\.[a-zA-Z]\w*")


def as_(): return RegExMatch(r"AS", ignore_case=True)


def symbol(): return RegExMatch(r"[a-zA-Z]\w*")


parser = ParserPython(base, comment)
