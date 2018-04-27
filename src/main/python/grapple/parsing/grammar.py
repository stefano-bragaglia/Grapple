from arpeggio import EOF, Optional, ParserPython, RegExMatch, ZeroOrMore, OneOrMore


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

def part_return(): return key_return, selectors
def selectors(): return selector, ZeroOrMore(",", selector)
def selector(): return content, synonym
def content(): return [value, labels, types, ident, accessor]
def value(): return json_value()
def labels(): return key_labels, "(", variable, ")"
def types(): return key_types, "(", variable, ")"
def ident(): return key_id, "(", variable, ")"
def accessor(): return variable, Optional(".", identifier)
def synonym(): return Optional(key_as, identifier)

def flag(): return RegExMatch(r":[a-zA-Z]\w*")
def identifier(): return RegExMatch(r"[a-zA-Z]\w*")
def variable(): return RegExMatch(r"\$[a-zA-Z]\w*")

def json_object(): return "{", Optional(json_members), "}"
def json_members(): return json_member, ZeroOrMore(",", json_member)
def json_member(): return json_string, ":", json_value
def json_value(): return [json_string, json_number, json_object, json_array, key_true, key_false, key_null]
def json_string(): return '"', RegExMatch('[^"]*'), '"'
def json_number(): return RegExMatch('-?\d+((\.\d*)?((e|E)(\+|-)?\d+)?)?')
def json_array(): return "[", Optional(json_elements), "]"
def json_elements(): return json_value, ZeroOrMore(",", json_value)

def key_as(): return RegExMatch(r"AS", ignore_case=True)
def key_false(): return RegExMatch(r"FALSE", ignore_case=True)
def key_id(): return RegExMatch(r"ID", ignore_case=True)
def key_labels(): return RegExMatch(r"LABELS", ignore_case=True)
def key_match(): return RegExMatch(r"MATCH", ignore_case=True)
def key_null(): return RegExMatch(r"NULL", ignore_case=True)
def key_return(): return RegExMatch(r"RETURN", ignore_case=True)
def key_rule(): return RegExMatch(r"RULE", ignore_case=True)
def key_salience(): return RegExMatch(r"SALIENCE", ignore_case=True)
def key_true(): return RegExMatch(r"TRUE", ignore_case=True)
def key_types(): return RegExMatch(r"TYPES", ignore_case=True)

def comment(): return [RegExMatch(r"/\*.*\*/"), RegExMatch(r"//.*")]
