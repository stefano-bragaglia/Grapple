from typing import List, Union

from arpeggio import NonTerminal, PTNodeVisitor, SemanticError, Terminal

Node = Union[Terminal, NonTerminal]


# noinspection PyMethodMayBeStatic
class KnowledgeVisitor(PTNodeVisitor):
    """
    def knowledge():
        return Optional(clauses), Optional(';'), EOF
    """

    def visit_knowledge(self, node: Node, children: List) -> object:
        if children and children[0] != ';':
            content = children[0]['value']
        else:
            content = []

        return {'value': content}

    def visit_clauses(self, node: Node, children: List) -> object:
        return {'value': [child['value'] for child in children] if children else []}

    def visit_clause(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': {'rule': content}}

    def visit_rule_part(self, node: Node, children: List) -> object:
        content = {'salience': 0}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_rule_description(self, node: Node, children: List) -> object:
        return {'value': {'description': children[1]['value'] if len(children) > 1 else None}}

    def visit_rule_salience(self, node: Node, children: List) -> object:
        value = children[1]['value']
        if value < 0:
            raise SemanticError("'salience' expected to be non-negative")

        return {'value': {'salience': value}}

    def visit_match_part(self, node: Node, children: List) -> object:
        content = {'optional': False}
        for child in children:
            content.update(child['value'])

        return {'value': {'match': content}}

    def visit_match_optional(self, node: Node, children: List) -> object:
        return {'value': {'optional': True}}

    def visit_match_patterns(self, node: Node, children: List) -> object:
        return {'value': {'pattern': [child['value'] for child in children[1:]]}}

    def visit_match_pattern(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_anonymous(self, node: Node, children: List) -> object:
        return {'value': {'pattern': {
            'start': children[0]['value'],
            'chain': [child['value'] for child in children[1:]]
        }}}

    def visit_match_start(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': {'node': content}}

    def visit_match_chain(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_node(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': {'node': content}}

    def visit_match_relation(self, node: Node, children: List) -> object:
        return {'value': {'relation': children[0]['value']}}

    def visit_match_both(self, node: Node, children: List) -> object:
        content = {'direction': 'any'}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_back(self, node: Node, children: List) -> object:
        content = {'direction': 'incoming'}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_next(self, node: Node, children: List) -> object:
        content = {'direction': 'outgoing'}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_none(self, node: Node, children: List) -> object:
        content = {'direction': 'any'}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_details(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_match_properties(self, node: Node, children: List) -> object:
        return {'value': {'properties': children[0]['value'] if children else {}}}

    def visit_match_labels(self, node: Node, children: List) -> object:
        return {'value': {'labels': [child['value'] for child in children]}}

    def visit_match_types(self, node: Node, children: List) -> object:
        return {'value': {'types': [child['value'] for child in children]}}

    def visit_return_part(self, node: Node, children: List) -> object:
        content = {'distinct': False}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': {'return': content}}

    def visit_return_distinct(self, node: Node, children: List) -> object:
        return {'value': {'distinct': True}}

    def visit_return_items(self, node: Node, children: List) -> object:
        return {'value': {'items': [child['value'] for child in children]}}

    def visit_return_first(self, node: Node, children: List) -> object:
        return {'value': children[0]['value']}

    def visit_return_item(self, node: Node, children: List) -> object:
        return {'value': children[0]['value']}

    def visit_return_all(self, node: Node, children: List) -> object:
        return {'value': {'function': 'all'}}

    def visit_return_coalesce(self, node: Node, children: List) -> object:
        content = {'function': 'coalesce', 'default': None}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_default(self, node: Node, children: List) -> object:
        return {'value': {'default': children[0]['value']}}

    def visit_return_keys(self, node: Node, children: List) -> object:
        content = {'function': 'keys'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_properties(self, node: Node, children: List) -> object:
        content = {'function': 'properties'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_id(self, node: Node, children: List) -> object:
        content = {'function': 'id'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_labels(self, node: Node, children: List) -> object:
        content = {'function': 'labels'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_types(self, node: Node, children: List) -> object:
        content = {'function': 'types'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_tail(self, node: Node, children: List) -> object:
        content = {'function': 'tail'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_head(self, node: Node, children: List) -> object:
        content = {'function': 'head'}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_selector(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_return_value(self, node: Node, children: List) -> object:
        content = {'value': children[0]['value']}
        for child in children[1:]:
            content.update(child['value'])

        return {'value': content}

    def visit_return_synonym(self, node: Node, children: List) -> object:
        return {'value': {'as': children[1]['value']}}

    def visit_return_order_by(self, node: Node, children: List) -> object:
        return {'value': {'order': children[2]['value']}}

    def visit_return_order_by_items(self, node: Node, children: List) -> object:
        return {'value': [child['value'] for child in children]}

    def visit_return_order_by_item(self, node: Node, children: List) -> object:
        content = {'ascending': True}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_return_order_by_selector(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_return_parameter(self, node: Node, children: List) -> object:
        return {'value': {'parameter': node.value}}

    def visit_return_property(self, node: Node, children: List) -> object:
        return {'value': {'property': children[0]['value']}}

    def visit_return_order_by_name(self, node: Node, children: List) -> object:
        return {'value': {'name': children[0]['value']}}

    def visit_return_ordering(self, node: Node, children: List) -> object:
        return {'value': children[0]['value']}

    def visit_return_ordering_ascending(self, node: Node, children: List) -> object:
        return {'value': {'ascending': True}}

    def visit_return_ordering_descending(self, node: Node, children: List) -> object:
        return {'value': {'ascending': False}}

    def visit_return_skip(self, node: Node, children: List) -> object:
        value = children[1]['value']
        if value < 0:
            raise SemanticError("'skip' expected to be non-negative")

        return {'value': {'skip': value}}

    def visit_return_limit(self, node: Node, children: List) -> object:
        value = children[1]['value']
        if value < 0:
            raise SemanticError("'limit' expected to be non-negative")

        return {'value': {'limit': value}}

    def visit_json_object(self, node: Node, children: List) -> object:
        return {'value': children[0]['value'] if children else {}}

    def visit_json_members(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['value'])

        return {'value': content}

    def visit_json_member(self, node: Node, children: List) -> object:
        return {'value': {children[0]['value']: children[1]['value']}}

    def visit_json_key(self, node: Node, children: List) -> object:
        return {'value': children[0]['value']}

    def visit_json_string(self, node: Node, children: List) -> object:
        return {'value': children[0] if children else ''}

    def visit_json_integer(self, node: Node, children: List) -> object:
        return {'value': int(node.value)}

    def visit_json_real(self, node: Node, children: List) -> object:
        return {'value': float(node.value)}

    def visit_json_array(self, node: Node, children: List) -> object:
        return {'value': children[0]['value'] if children else []}

    def visit_json_elements(self, node: Node, children: List) -> object:
        return {'value': [child['value'] for child in children]}

    def visit_json_true(self, node: Node, children: List) -> object:
        return {'value': True}

    def visit_json_false(self, node: Node, children: List) -> object:
        return {'value': False}

    def visit_json_null(self, node: Node, children: List) -> object:
        return {'value': None}

    def visit_identifier(self, node: Node, children: List) -> object:
        return {'value': node.value}

    def visit_parameter(self, node: Node, children: List) -> object:
        return {'value': node.value}

    def visit_key_as(self, node: Node, children: List) -> object:
        return {'value': 'AS'}

    def visit_key_asc(self, node: Node, children: List) -> object:
        return {'value': 'ASC'}

    def visit_key_ascending(self, node: Node, children: List) -> object:
        return {'value': 'ASCENDING'}

    def visit_key_by(self, node: Node, children: List) -> object:
        return {'value': 'BY'}

    def visit_key_coalesce(self, node: Node, children: List) -> object:
        return {'value': 'coalesce'}

    def visit_key_desc(self, node: Node, children: List) -> object:
        return {'value': 'DESC'}

    def visit_key_descending(self, node: Node, children: List) -> object:
        return {'value': 'DESCENDING'}

    def visit_key_distinct(self, node: Node, children: List) -> object:
        return {'value': 'DISTINCT'}

    def visit_key_head(self, node: Node, children: List) -> object:
        return {'value': 'head'}

    def visit_key_id(self, node: Node, children: List) -> object:
        return {'value': 'id'}

    def visit_key_keys(self, node: Node, children: List) -> object:
        return {'value': 'keys'}

    def visit_key_labels(self, node: Node, children: List) -> object:
        return {'value': 'labels'}

    def visit_key_limit(self, node: Node, children: List) -> object:
        return {'value': 'LIMIT'}

    def visit_key_match(self, node: Node, children: List) -> object:
        return {'value': 'MATCH'}

    def visit_key_optional(self, node: Node, children: List) -> object:
        return {'value': 'OPTIONAL'}

    def visit_key_order(self, node: Node, children: List) -> object:
        return {'value': 'ORDER'}

    def visit_key_properties(self, node: Node, children: List) -> object:
        return {'value': 'properties'}

    def visit_key_return(self, node: Node, children: List) -> object:
        return {'value': 'RETURN'}

    def visit_key_rule(self, node: Node, children: List) -> object:
        return {'value': 'RULE'}

    def visit_key_salience(self, node: Node, children: List) -> object:
        return {'value': 'SALIENCE'}

    def visit_key_skip(self, node: Node, children: List) -> object:
        return {'value': 'SKIP'}

    def visit_key_tail(self, node: Node, children: List) -> object:
        return {'value': 'tail'}

    def visit_key_types(self, node: Node, children: List) -> object:
        return {'value': 'types'}
