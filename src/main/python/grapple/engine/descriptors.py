from valid_model import Object
from valid_model.descriptors import String, List, Dict, EmbeddedObject, Bool, Integer


class EntityDescriptor(Object):
    variable = String()
    labels = List(value=String(nullable=False))
    properties = Dict(key=String(nullable=False))


class PathDescriptor(Object):
    variable = String()
    entities = List(value=EmbeddedObject(EntityDescriptor))


class PatternDescriptor(Object):
    paths = List(value=EmbeddedObject(PathDescriptor))


class RecordDescriptor(Object):
    variable = String(nullable=False)
    property = String()
    name = String()


class OrderDescriptor(Object):
    variable = String()
    property = String()
    name = String()
    asc = Bool(default=True)


class ReturnDescriptor(Object):
    records = List(value=EmbeddedObject(RecordDescriptor(nullable=False)))
    ordering = List(value=EmbeddedObject(OrderDescriptor(nullable=False)))
    limit = Integer(default=-1)


if __name__ == '__main__':
