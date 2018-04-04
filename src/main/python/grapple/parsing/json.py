from arpeggio import *
from arpeggio import RegExMatch as _


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


def memberDef():
    return jsonString, ":", jsonValue


def jsonMembers():
    return memberDef, ZeroOrMore(",", memberDef)


def jsonObject():
    return "{", Optional(jsonMembers), "}"


def jsonFile():
    return jsonObject, EOF


if __name__ == "__main__":
    data = '{"key1": "value", "key2": 0, "key3": 0.0, "key4": true, "key5": null, "key6": [], "key7": [1, 2, 3], ' \
           '"key8": {}, "key9": {"key0": null}}'

    # Creating parser from parser model.
    parser = ParserPython(jsonFile, debug=True)
    # Parse json string
    parse_tree = parser.parse(data)
    # parse_tree can now be analysed and transformed to some other form
    # using e.g. visitor support. See http://igordejanovic.net/Arpeggio/semantics/

    # In debug mode dot (graphviz) files for parser model
    # and parse tree will be created for visualization.
    # Checkout current folder for .dot files.
