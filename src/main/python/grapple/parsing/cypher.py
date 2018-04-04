from arpeggio import *
from arpeggio import RegExMatch as _


def comment():
    return [_(r'//.*'), _(r'/\*.*\*/')]


def MATCH():
    return _(r'MATCH', ignore_case=True)


def label():
    return _(r':[a..zA..Z][a..zA..Z0..9_]*')


def labels():
    return label, ZeroOrMore(label)


def variable():
    return _(r'\$?[a..zA..Z][a..zA..Z0..9_]*')


def node():
    return "(", Optional(variable), ")"


def rule():
    return MATCH, node, ';'


def base():
    return ZeroOrMore(rule), EOF


if __name__ == '__main__':
    data = 'match (  ); /* Skip */ MATCH ($var); Match(var); /* MATCH ($VAR); */'
    parser = ParserPython(base, comment, debug=True)
    tree = parser.parse(data)
