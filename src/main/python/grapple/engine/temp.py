from typing import List

from grapple.engine.agenda import Agenda
from grapple.engine.condition import IsNode, HasLabel, HasProperty, IsRelation, HasType, Condition, AreEqual
from grapple.engine.descriptors import BaseDesc, RuleDesc, PathDesc, NodeDesc, RecordDesc, ReturnDesc, RelationDesc, \
    Direction
from grapple.engine.rete import Root, Alpha, Beta, Leaf


def node_conditions(node: NodeDesc) -> List[Condition]:
    conditions = [IsNode()]

    for label in node.labels:
        condition = HasLabel(label)
        if condition not in conditions:
            conditions.append(condition)

    for key, value in node.properties.items():
        condition = HasProperty(key, value)
        if condition not in conditions:
            conditions.append(condition)

    return conditions


def relation_conditions(relation: RelationDesc) -> List[Condition]:
    conditions = [IsRelation()]
    if relation.direction == Direction.OUTGOING:
        conditions.append(IsOutgoing())
    elif relation.direction == Direction.OUTGOING:
        conditions.append(IsIncoming())

    for type in relation.types:
        condition = HasType(type)
        if condition not in conditions:
            conditions.append(condition)

    for key, value in relation.properties.items():
        condition = HasProperty(key, value)
        if condition not in conditions:
            conditions.append(condition)

    return conditions


def something(*bases: 'BaseDesc'):
    agenda = Agenda()
    alphas = {}

    root = Root()
    for base in bases:
        for rule in base.rules:
            for path in rule.pattern:
                current = None
                for condition in node_conditions(path.source):
                    alpha = alphas.setdefault(condition.signature, Alpha(condition, root))
                    current = Beta(AreEqual(), current, alpha) if current else alpha

                for step in path.steps:
                    relation = None
                    for condition in relation_conditions(step.relation):
                        alpha = alphas.setdefault(condition.signature, Alpha(condition, root))
                        relation = Beta(AreEqual(), relation, alpha) if relation else alpha

                    current = Beta(None, current, relation)

                    node = None
                    for condition in node_conditions(step.node):
                        alpha = alphas.setdefault(condition.signature, Alpha(condition, root))
                        node = Beta(AreEqual(), node, alpha) if node else alpha

                    current = Beta(None, current, node)

                    # Relation is FWD, RWD, ANY
                    # Relation HasTail Current
                    # Relation HasHead Current

                current = Leaf(current, rule, agenda)


if __name__ == '__main__':
    rec0 = RecordDesc(variable='n')
    rec1 = RecordDesc(variable='n', property='gender')
    rec2 = RecordDesc(variable='n', property='name', title='name')
    ret = ReturnDesc(records=[rec0, rec1, rec2])

    node = NodeDesc(variable='n', labels=['person'], properties={'gender': 'male'})
    path = PathDesc(source=node)

    rule = RuleDesc(pattern=[path], result=ret)
    base = BaseDesc(rules=[rule])

    # print(json.dumps(base.__json__(), indent=4, sort_keys=True))

    something(base)
