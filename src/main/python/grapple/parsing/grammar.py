from arpeggio import EOF, OneOrMore, Optional, RegExMatch, ZeroOrMore

"""
// clause <- clause_reading / clause updating ;
// clause_reading <- rule_part reading_part* return_part ;
// clause_updating <- rule_part reading_part* updating_part+ return_part? ;
// reading_part <- match_part / unwind_part / in_query_call_part ;
// updating_part <- create_part / merge_part / delete_part / set_part / remove_part ;
"""


# ----------------------------------------------------------------------------------------------------------------------
def comment():
    return [RegExMatch("//.*"), RegExMatch("/\*.*\*/", multiline=True)]


# ----------------------------------------------------------------------------------------------------------------------
def cypher():
    return Optional(clauses), Optional(';'), EOF


def clauses():
    return clause, ZeroOrMore(';', clause)


def clause():
    return [clause_reading, clause_updating]


def clause_reading():
    return rule_part, ZeroOrMore(match_part), return_part


def clause_updating():
    return rule_part, ZeroOrMore(match_part), OneOrMore(updating_part), Optional(return_part)


def updating_part():
    return [create_part, remove_part, set_part, delete_part]


def rule_part():
    return description, Optional(salience)


def create_part():
    return key_create, pattern, ZeroOrMore(',', pattern)


def delete_part():
    return Optional(is_detach), key_delete, entity, ZeroOrMore(',', entity)


def match_part():
    return Optional(is_optional), key_match, pattern, ZeroOrMore(',', pattern)


def remove_part():
    return key_remove, removable, ZeroOrMore(',', removable)


def set_part():
    return key_set, settable, ZeroOrMore(',', settable)


def return_part():
    return key_return, Optional(is_distinct), items, Optional(order_by), Optional(skip), Optional(limit)


# ----------------------------------------------------------------------------------------------------------------------
def pattern():
    return Optional(entity, '='), start, Optional(chain)


def start():
    return node


def chain():
    return OneOrMore(step)


def step():
    return relation, node


def node():
    return '(', Optional(entity), Optional(labels), Optional(properties), ')'


def relation():
    return [dir_both, dir_back, dir_next, dir_none]


def dir_both():
    return '<-', Optional(details), '->'


def dir_back():
    return '<-', Optional(details), '-'


def dir_next():
    return '-', Optional(details), '->'


def dir_none():
    return '-', Optional(details), '-'


def details():
    return '[', Optional(entity), Optional(types), Optional(properties), ']'


# ----------------------------------------------------------------------------------------------------------------------
def removable():
    return [descriptor, selector]


def selector():
    return entity, field


# ----------------------------------------------------------------------------------------------------------------------
def settable():
    return [descriptor, replace_map, assign_map, assign_value]


def descriptor():
    return entity, OneOrMore(flag)


def replace_map():
    return entity, '+=', [parameter, properties]


def assign_map():
    return entity, '=', [parameter, properties]


def assign_value():
    return selector, '=', [parameter, value]


def sortable():
    return [selector, entity, name], Optional([asc, desc])


# ----------------------------------------------------------------------------------------------------------------------
def items():
    return first, ZeroOrMore(',', item)


def first():
    return [item, item_all]


def item():
    return [item_coalesce, item_keys, item_properties, item_id, item_labels, item_types,
            item_tail, item_head, item_length, item_nodes, item_relations, item_selector, item_value]


def item_all():
    return '*'


def item_coalesce():
    return func_coalesce, '(', parameter, field, ',', value, ')', Optional(synonym)


def item_keys():
    return func_keys, '(', parameter, ')', Optional(synonym)


def item_properties():
    return func_properties, '(', parameter, ')', Optional(synonym)


def item_id():
    return func_id, '(', parameter, ')', Optional(synonym)


def item_labels():
    return func_labels, '(', parameter, ')', Optional(synonym)


def item_types():
    return func_types, '(', parameter, ')', Optional(synonym)


def item_tail():
    return func_tail, '(', parameter, ')', Optional(synonym)


def item_head():
    return func_head, '(', parameter, ')', Optional(synonym)


def item_length():
    return func_length, '(', parameter, ')', Optional(synonym)


def item_nodes():
    return func_nodes, '(', parameter, ')', Optional(synonym)


def item_relations():
    return func_relations, '(', parameter, ')', Optional(synonym)


def item_selector():
    return entity, Optional(field), Optional(synonym)


def item_value():
    return value, Optional(synonym)


def order_by():
    return key_order, key_by, sortable, ZeroOrMore(',', sortable)


# ----------------------------------------------------------------------------------------------------------------------
def asc():
    return [key_asc, key_ascending]


def desc():
    return [key_desc, key_descending]


def description():
    return key_rule, Optional(json_string)


def entity():
    return variable


def field():
    return '.', json_key


def flag():
    return ':', identifier


def is_detach():
    return key_detach


def is_distinct():
    return key_distinct


def is_optional():
    return key_optional


def labels():
    return OneOrMore(flag)


def limit():
    return key_limit, json_integer


def name():
    return json_key


def parameter():
    return variable


def properties():
    return json_object


def salience():
    return key_salience, json_integer


def skip():
    return key_skip, json_integer


def synonym():
    return key_as, json_key


def types():
    return OneOrMore(flag)


def value():
    return json_value


# ----------------------------------------------------------------------------------------------------------------------
def identifier():
    return RegExMatch(r'[A-Za-z_][A-Za-z_0-9]*')


def variable():
    return RegExMatch(r'\$[A-Za-z_0-9]+')


# ----------------------------------------------------------------------------------------------------------------------
def json_object():
    return '{', Optional(json_members), '}'


def json_members():
    return json_member, ZeroOrMore(',', json_member)


def json_member():
    return json_key, ':', json_value


def json_key():
    return [json_string, identifier]


def json_value():
    return [json_string, json_real, json_integer, json_object, json_array, json_true, json_false, json_null, variable]


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


# ----------------------------------------------------------------------------------------------------------------------
def func_coalesce():
    return RegExMatch(r'coalesce', ignore_case=True)


def func_head():
    return RegExMatch(r'head', ignore_case=True)


def func_id():
    return RegExMatch(r'id', ignore_case=True)


def func_keys():
    return RegExMatch(r'keys', ignore_case=True)


def func_labels():
    return RegExMatch(r'labels', ignore_case=True)


def func_length():
    return RegExMatch(r'length', ignore_case=True)


def func_nodes():
    return RegExMatch(r'nodes', ignore_case=True)


def func_relations():
    return RegExMatch(r'relations', ignore_case=True)


def func_properties():
    return RegExMatch(r'properties', ignore_case=True)


def func_tail():
    return RegExMatch(r'tail', ignore_case=True)


def func_types():
    return RegExMatch(r'types', ignore_case=True)


# ----------------------------------------------------------------------------------------------------------------------
def key_as():
    return RegExMatch(r'AS', ignore_case=True)


def key_asc():
    return RegExMatch(r'ASC', ignore_case=True)


def key_ascending():
    return RegExMatch(r'ASCENDING', ignore_case=True)


def key_by():
    return RegExMatch(r'BY', ignore_case=True)


def key_create():
    return RegExMatch(r'CREATE', ignore_case=True)


def key_delete():
    return RegExMatch(r'DELETE', ignore_case=True)


def key_detach():
    return RegExMatch(r'DETACH', ignore_case=True)


def key_desc():
    return RegExMatch(r'DESC', ignore_case=True)


def key_descending():
    return RegExMatch(r'DESCENDING', ignore_case=True)


def key_distinct():
    return RegExMatch(r'DISTINCT', ignore_case=True)


def key_limit():
    return RegExMatch(r'LIMIT', ignore_case=True)


def key_match():
    return RegExMatch(r'MATCH', ignore_case=True)


def key_optional():
    return RegExMatch(r'OPTIONAL', ignore_case=True)


def key_order():
    return RegExMatch(r'ORDER', ignore_case=True)


def key_remove():
    return RegExMatch(r'REMOVE', ignore_case=True)


def key_return():
    return RegExMatch(r'RETURN', ignore_case=True)


def key_rule():
    return RegExMatch(r'RULE', ignore_case=True)


def key_salience():
    return RegExMatch(r'SALIENCE', ignore_case=True)


def key_set():
    return RegExMatch(r'SET', ignore_case=True)


def key_skip():
    return RegExMatch(r'SKIP', ignore_case=True)
