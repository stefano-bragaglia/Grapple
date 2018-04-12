from typing import List

from grapple.engine.condition import IsNode, AlphaCondition, HasLabel, HasProperty, IsRelation, HasType
from grapple.engine.descriptors import BaseDesc, RuleDesc, PathDesc, NodeDesc, RecordDesc, ReturnDesc, RelationDesc
from grapple.engine.rete import Root, Alpha, Beta


def node_conditions(node: NodeDesc) -> List[AlphaCondition]:
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


def relation_conditions(relation: RelationDesc) -> List[AlphaCondition]:
    conditions = [IsRelation()]

    for type in node.types:
        condition = HasType(type)
        if condition not in conditions:
            conditions.append(condition)

    for key, value in node.properties.items():
        condition = HasProperty(key, value)
        if condition not in conditions:
            conditions.append(condition)

    return conditions


def something(*bases: 'BaseDesc'):
    alphas = {}

    root = Root()
    for base in bases:
        for rule in base.rules:
            for path in rule.pattern:
                current = None

                conditions = node_conditions(path.source)

                for condition in conditions:
                    alpha = alphas.setdefault(condition.signature, Alpha(condition, root))
                    if current:
                        beta = Beta()
                        beta.hook(current)
                        beta.hook(alpha)
                        current = beta

                    else:
                        current = alpha


                    if current:
                    else:
                        current = alpha

                for label in path.source.labels:
                    HasLabel(label)

                path.source

                print(path)


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
