from typing import List, Union

from arpeggio import NonTerminal, PTNodeVisitor, Terminal

Node = Union[Terminal, NonTerminal]


# noinspection PyMethodMayBeStatic
class KnowledgeVisitor(PTNodeVisitor):
    def visit_cypher(self, node: Node, children: List) -> object:
        if children and children[0] != ';':
            content = children[0]['data']
        else:
            content = []

        return {'data': content}

    def visit_clauses(self, node: Node, children: List) -> object:
        return {'data': [child['data'] for child in children] if children else []}

    def visit_clause(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_clause_reading(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'clause_reading': content}}

    def visit_clause_updating(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'clause_updating': content}}

    def visit_updating_part(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_rule_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'rule_part': content}}

    def visit_create_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'create_part': content}}

    def visit_delete_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'delete_part': content}}

    def visit_match_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'match_part': content}}

    def visit_remove_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'remove_part': content}}

    def visit_set_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'set_part': content}}

    def visit_return_part(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'return_part': content}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_pattern(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'pattern': content}}

    def visit_chain(self, node: Node, children: List) -> object:
        content = [child['data']['next'] for child in children]

        return {'data': {'chain': content}}

    def visit_next(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'next': content}}

    def visit_node(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'node': content}}

    def visit_relation(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_dir_both(self, node: Node, children: List) -> object:
        content = {'direction': 'any'}
        content.update(children[0]['data']['relation'])

        return {'data': {'relation': content}}

    def visit_dir_back(self, node: Node, children: List) -> object:
        content = {'direction': 'incoming'}
        content.update(children[0]['data']['relation'])

        return {'data': {'relation': content}}

    def visit_dir_next(self, node: Node, children: List) -> object:
        content = {'direction': 'ongoing'}
        content.update(children[0]['data']['relation'])

        return {'data': {'relation': content}}

    def visit_dir_none(self, node: Node, children: List) -> object:
        content = {'direction': 'any'}
        content.update(children[0]['data']['relation'])

        return {'data': {'relation': content}}

    def visit_details(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'relation': content}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_removable(self, node: Node, children: List) -> object:
        return {'data': {'settable': next(children[0]['data'].values())}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_settable(self, node: Node, children: List) -> object:
        return {'data': {'settable': next(children[0]['data'].values())}}

    def visit_replace_map(self, node: Node, children: List) -> object:
        content = {'function': 'replace'}
        for child in children:
            content.update(child['data'])

        return {'data': {'settable': content}}

    def visit_assign_map(self, node: Node, children: List) -> object:
        content = {'function': 'assign'}
        for child in children:
            content.update(child['data'])

        return {'data': {'settable': content}}

    def visit_assign_value(self, node: Node, children: List) -> object:
        content = {'function': 'assign'}
        for child in children:
            content.update(child['data'])

        return {'data': {'settable': content}}

    def visit_sortable(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': {'sortable': content}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_items(self, node: Node, children: List) -> object:
        return {'data': {'items': [child['data']['item'] for child in children]}}

    def visit_first(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_item(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_item_all(self, node: Node, children: List) -> object:
        return {'data': {'item': {'function': 'all'}}}

    def visit_item_coalesce(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_keys(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_properties(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_id(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_labels(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_types(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_tail(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_head(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_length(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_nodes(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_relations(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_selector(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_item_value(self, node: Node, children: List) -> object:
        return {'data': {'item': [child['data'] for child in children]}}

    def visit_order_by(self, node: Node, children: List) -> object:
        return {'data': {'order_by': [child['data'] for child in children[2:]]}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_asc(self, node: Node, children: List) -> object:
        return {'data': {'ordering': True}}

    def visit_desc(self, node: Node, children: List) -> object:
        return {'data': {'ordering': False}}

    def visit_description(self, node: Node, children: List) -> object:
        return {'data': {'description': children[1]['data'] if len(children) > 1 else None}}

    def visit_descriptor(self, node: Node, children: List) -> object:
        content = {
            'entity': children[0]['data']['entity'],
            'flag': []}
        for child in children[:1]:
            content['flag'].append(child['data']['flag'])

        return {'data': {'descriptor': content}}

    def visit_entity(self, node: Node, children: List) -> object:
        return {'data': {'entity': children[0]['data']}}

    def visit_field(self, node: Node, children: List) -> object:
        return {'data': {'field': children[0]['data']}}

    def visit_flag(self, node: Node, children: List) -> object:
        return {'data': {'flag': children[0]['data']}}

    def visit_is_detach(self, node: Node, children: List) -> object:
        return {'data': {'detach': True}}

    def visit_is_distinct(self, node: Node, children: List) -> object:
        return {'data': {'distinct': True}}

    def visit_is_optional(self, node: Node, children: List) -> object:
        return {'data': {'optional': True}}

    def visit_labels(self, node: Node, children: List) -> object:
        return {'data': {'labels': [child['data'] for child in children]}}

    def visit_limit(self, node: Node, children: List) -> object:
        return {'data': {'limit': children[1]['data']}}

    def visit_name(self, node: Node, children: List) -> object:
        return {'data': {'name': children[0]['data']}}

    def visit_parameter(self, node: Node, children: List) -> object:
        return {'data': {'parameter': children[0]['data']}}

    def visit_properties(self, node: Node, children: List) -> object:
        return {'data': {'properties': children[0]['data']}}

    def visit_salience(self, node: Node, children: List) -> object:
        return {'data': {'salience': children[1]['data']}}

    def visit_selector(self, node: Node, children: List) -> object:
        return {'data': {key: value for child in children for key, value in child['data'].items()}}

    def visit_skip(self, node: Node, children: List) -> object:
        return {'data': {'skip': children[1]['data']}}

    def visit_synonym(self, node: Node, children: List) -> object:
        return {'data': {'synonym': children[1]['data']}}

    def visit_types(self, node: Node, children: List) -> object:
        return {'data': {'types': [child['data'] for child in children]}}

    def visit_value(self, node: Node, children: List) -> object:
        return {'data': {'value': children[0]['data']}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_identifier(self, node: Node, children: List) -> object:
        return {'data': node.value}

    def visit_variable(self, node: Node, children: List) -> object:
        return {'data': node.value}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_json_object(self, node: Node, children: List) -> object:
        return {'data': children[0]['data'] if children else {}}

    def visit_json_members(self, node: Node, children: List) -> object:
        content = {}
        for child in children:
            content.update(child['data'])

        return {'data': content}

    def visit_json_member(self, node: Node, children: List) -> object:
        return {'data': {children[0]['data']: children[1]['data']}}

    def visit_json_key(self, node: Node, children: List) -> object:
        return {'data': children[0]['data']}

    def visit_json_string(self, node: Node, children: List) -> object:
        return {'data': children[0] if children else ''}

    def visit_json_integer(self, node: Node, children: List) -> object:
        return {'data': int(node.value)}

    def visit_json_real(self, node: Node, children: List) -> object:
        return {'data': float(node.value)}

    def visit_json_array(self, node: Node, children: List) -> object:
        return {'data': children[0]['data'] if children else []}

    def visit_json_elements(self, node: Node, children: List) -> object:
        return {'data': [child['data'] for child in children]}

    def visit_json_true(self, node: Node, children: List) -> object:
        return {'data': True}

    def visit_json_false(self, node: Node, children: List) -> object:
        return {'data': False}

    def visit_json_null(self, node: Node, children: List) -> object:
        return {'data': None}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_func_coalesce(self, node: Node, children: List) -> object:
        return {'data': {'function': 'coalesce'}}

    def visit_func_head(self, node: Node, children: List) -> object:
        return {'data': {'function': 'head'}}

    def visit_func_id(self, node: Node, children: List) -> object:
        return {'data': {'function': 'id'}}

    def visit_func_keys(self, node: Node, children: List) -> object:
        return {'data': {'function': 'keys'}}

    def visit_func_labels(self, node: Node, children: List) -> object:
        return {'data': {'function': 'labels'}}

    def visit_func_length(self, node: Node, children: List) -> object:
        return {'data': {'function': 'length'}}

    def visit_func_nodes(self, node: Node, children: List) -> object:
        return {'data': {'function': 'nodes'}}

    def visit_func_relations(self, node: Node, children: List) -> object:
        return {'data': {'function': 'relations'}}

    def visit_func_properties(self, node: Node, children: List) -> object:
        return {'data': {'function': 'properties'}}

    def visit_func_tail(self, node: Node, children: List) -> object:
        return {'data': {'function': 'tail'}}

    def visit_func_types(self, node: Node, children: List) -> object:
        return {'data': {'function': 'types'}}

    # ------------------------------------------------------------------------------------------------------------------
    def visit_key_as(self, node: Node, children: List) -> object:
        return {'data': 'AS'}

    def visit_key_asc(self, node: Node, children: List) -> object:
        return {'data': 'ASC'}

    def visit_key_ascending(self, node: Node, children: List) -> object:
        return {'data': 'ASCENDING'}

    def visit_key_by(self, node: Node, children: List) -> object:
        return {'data': 'BY'}

    def visit_key_create(self, node: Node, children: List) -> object:
        return {'data': 'CREATE'}

    def visit_key_skip(self, node: Node, children: List) -> object:
        return {'data': 'SKIP'}

    def visit_key_delete(self, node: Node, children: List) -> object:
        return {'data': 'DELETE'}

    def visit_key_detach(self, node: Node, children: List) -> object:
        return {'data': 'DETACH'}

    def visit_key_desc(self, node: Node, children: List) -> object:
        return {'data': 'DESC'}

    def visit_key_descending(self, node: Node, children: List) -> object:
        return {'data': 'DESCENDING'}

    def visit_key_distinct(self, node: Node, children: List) -> object:
        return {'data': 'DISTINCT'}

    def visit_key_limit(self, node: Node, children: List) -> object:
        return {'data': 'LIMIT'}

    def visit_key_match(self, node: Node, children: List) -> object:
        return {'data': 'MATCH'}

    def visit_key_optional(self, node: Node, children: List) -> object:
        return {'data': 'OPTIONAL'}

    def visit_key_order(self, node: Node, children: List) -> object:
        return {'data': 'ORDER'}

    def visit_key_remove(self, node: Node, children: List) -> object:
        return {'data': 'REMOVE'}

    def visit_key_return(self, node: Node, children: List) -> object:
        return {'data': 'RETURN'}

    def visit_key_rule(self, node: Node, children: List) -> object:
        return {'data': 'RULE'}

    def visit_key_salience(self, node: Node, children: List) -> object:
        return {'data': 'SALIENCE'}

    def visit_key_set(self, node: Node, children: List) -> object:
        return {'data': 'SET'}

    def visit_key_skip(self, node: Node, children: List) -> object:
        return {'data': 'SKIP'}
