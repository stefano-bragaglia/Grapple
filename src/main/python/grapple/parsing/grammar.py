from arpeggio import EOF, Optional, ParserPython, RegExMatch, ZeroOrMore


def comment(): return [RegExMatch(r"/\*.*\*/"), RegExMatch(r"//.*")]

def base(): Optional(rules), EOF

def rules(): return rule, ZeroOrMore(rule)
def rule(): return part_return, ";"

def part_return(): return key_return, selectors()
def selectors(): return selector, ZeroOrMore(",", selector)
def selector(): return content, synonym
def content(): return [json_value, labels, types, ident, accessor]
def labels(): return key_labels, "(", variable, ")"
def types(): return key_types, "(", variable, ")"
def ident(): return key_id(), "(", variable, ")"
def accessor(): return variable, Optional(".", identifier)
def synonym(): return Optional(key_as, identifier)

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
def key_null(): return RegExMatch(r"NULL", ignore_case=True)
def key_return(): return RegExMatch(r"RETURN", ignore_case=True)
def key_true(): return RegExMatch(r"TRUE", ignore_case=True)
def key_types(): return RegExMatch(r"TYPES", ignore_case=True)
