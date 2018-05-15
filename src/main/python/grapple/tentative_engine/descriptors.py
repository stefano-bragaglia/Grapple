from enum import Enum

from valid_model import Object
from valid_model.descriptors import Dict, EmbeddedObject, Integer, List, String


class Direction(Enum):
    INCOMING = 1,
    OUTGOING = 2,
    ANY = 0


class RelationDesc(Object):
    variable = String()
    direction = Integer(default=Direction.ANY, nullable=False)
    types = List(value=String(nullable=False))
    properties = Dict(key=String(nullable=False))


class NodeDesc(Object):
    variable = String()
    labels = List(value=String(nullable=False))
    properties = Dict(key=String(nullable=False))


class StepDesc(Object):
    relation = EmbeddedObject(RelationDesc)
    node = EmbeddedObject(NodeDesc)


class PathDesc(Object):
    source = EmbeddedObject(NodeDesc)
    steps = List(value=EmbeddedObject(StepDesc))


class RecordDesc(Object):
    variable = String(nullable=False)
    property = String()
    title = String()


class ReturnDesc(Object):
    records = List(value=EmbeddedObject(RecordDesc))


class RuleDesc(Object):
    pattern = List(value=EmbeddedObject(PathDesc))
    result = EmbeddedObject(ReturnDesc)


class BaseDesc(Object):
    rules = List(value=EmbeddedObject(RuleDesc))
