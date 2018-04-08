from valid_model import Object
from valid_model.descriptors import String, List, Dict


class NodeDescriptor(Object):
    variable = String()
    labels = List(value=String(nullable=False))
    properties = Dict(key=String(nullable=False), value=)
    pass
