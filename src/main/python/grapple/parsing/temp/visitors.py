from arpeggio import PTNodeVisitor

# noinspection PyMethodMayBeStatic


# noinspection PyMethodMayBeStatic
from grapple.engine.descriptors import Direction


class GrammarVisitor(PTNodeVisitor):

    def visit_comment(self, node, children):
        return

    def visit_base(self, node, children):
        return list(children)

    def visit_rule(self, node, children):
        return {'pattern': children[1], 'requests': children[2]}

    def visit_match(self, node, children):
        return

    def visit_pattern(self, node, children):
        return list(children)

    def visit_node(self, node, children):
        entity = {'name': None, 'labels': [], 'properties': {}}
        for child in children:
            if type(child) is str:
                entity['name'] = child
            elif type(child) is list:
                entity['labels'] = child
            elif type(child) is dict:
                entity['properties'] = child
            else:
                raise ValueError('Unexpected type')

        return entity

    def visit_relation(self, node, children):
        return children[0]

    def visit_relation_rwd(self, node, children):
        entity = children[0]
        entity['direction'] = Direction.INCOMING

        return entity

    def visit_relation_fwd(self, node, children):
        entity = children[0]
        entity['direction'] = Direction.OUTGOING

        return entity

    def visit_relation_any(self, node, children):
        entity = children[0]
        entity['direction'] = Direction.ANY

        return entity

    def visit_relation_def(self, node, children):
        entity = {'name': None, 'types': [], 'properties': {}}
        for child in children:
            if type(child) is str:
                entity['name'] = child
            elif type(child) is list:
                entity['types'] = child
            elif type(child) is dict:
                entity['properties'] = child
            else:
                raise ValueError('Unexpected type')

        return entity

    def visit_variable(self, node, children):
        return node.value

    def visit_labels(self, node, children):
        return list(children)

    def visit_label(self, node, children):
        return node.value[1:]

    def visit_json_object(self, node, children):
        return children[0]

    def visit_json_members(self, node, children):
        return {child[0]: child[1] for child in children}

    def visit_json_member(self, node, children):
        return children[0], children[1]

    def visit_json_value(self, node, children):
        return children[0]

    def visit_json_string(self, node, children):
        return children[0]

    def visit_json_number(self, node, children):
        try:
            return int(node.value)
        except ValueError:
            return float(node.value)

    def visit_json_array(self, node, children):
        return children[0]

    def visit_json_elements(self, node, children):
        return list(children)

    def visit_true_(self, node, children):
        return True

    def visit_false_(self, node, children):
        return False

    def visit_null_(self, node, children):
        return None

    def visit_return_(self, node, children):
        return

    def visit_requests(self, node, children):
        return list(children)

    def visit_request(self, node, children):
        return {key: child[key] for child in children for key in child}

    def visit_constant(self, node, children):
        return {'value': children[0]}

    def visit_identifier(self, node, children):
        return {key: child[key] for child in children for key in child}

    def visit_reference(self, node, children):
        return {'variable': node.value}

    def visit_field(self, node, children):
        return {'field': node.value[1:]}

    def visit_as_(self, node, children):
        return

    def visit_symbol(self, node, children):
        return {'name': node.value}
