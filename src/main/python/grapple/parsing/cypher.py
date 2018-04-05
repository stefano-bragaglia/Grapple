from arpeggio import *
from arpeggio import RegExMatch as _


def comment():
    return [_(r'//.*'), _(r'/\*.*\*/')]


def MATCH():
    return _(r'MATCH', ignore_case=True)


def label():
    return _(r'\:\w+')


def labels():
    return label, ZeroOrMore(label)


def variable():
    return _(r'\$?\w+')


def TRUE():
    return "true"


def FALSE():
    return "false"


def NULL():
    return "null"


def jsonString():
    return '"', _('[^"]*'), '"'


def jsonNumber():
    return _('-?\d+((\.\d*)?((e|E)(\+|-)?\d+)?)?')


def jsonValue():
    return [jsonString, jsonNumber, jsonObject, jsonArray, TRUE, FALSE, NULL]


def jsonArray():
    return "[", Optional(jsonElements), "]"


def jsonElements():
    return jsonValue, ZeroOrMore(",", jsonValue)


def jsonDefinition():
    return jsonString, ":", jsonValue


def jsonMembers():
    return jsonDefinition, ZeroOrMore(",", jsonDefinition)


def jsonObject():
    return "{", Optional(jsonMembers), "}"


def details():
    return "[", Optional(variable), Optional(labels), Optional(jsonObject), "]"


def undirected():
    return "-", Optional(details), "-"


def incoming():
    return "<-", Optional(details), "-"


def outgoing():
    return "-", Optional(details), "->"


def relation():
    return [outgoing, incoming, undirected]


def node():
    return "(", Optional(variable), Optional(labels), Optional(jsonObject), ")"


def path():
    return node, ZeroOrMore(relation, node)


def rule():
    return MATCH, path, ';'  # CREATE DELETE SET RETURN


def base():
    return ZeroOrMore(rule), EOF


if __name__ == '__main__':
    data = 'MATCH ( $var :lab1 :lab2 {"key1": "value", "key2": 0, "key3": 0.0, "key4": true, "key5": null, "key6": [], "key7": [1, 2, 3], ' \
           '"key8": {}, "key9": {"key0": null}} )-[$r:type{"time":"str"}]->(); /* skip me */'
    parser = ParserPython(base, comment, debug=True)
    tree = parser.parse(data)
    print('Done.')
