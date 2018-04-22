from arpeggio import EOF, Optional, ParserPython, RegExMatch, ZeroOrMore


def comment(): return [RegExMatch(r"//.*"), RegExMatch(r"/\*.*\*/")]


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
