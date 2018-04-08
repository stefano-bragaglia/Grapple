from grapple.engine.activation import Params

Record = Params


class ActionError(Exception):
    pass


class Action(object):

    def apply(self, params: Params, graph: 'Graph') -> Record:
        raise NotImplementedError('To be implemented')


class ReturnAction(Action):

    def __init__(self, descriptor: 'ReturnDescriptor'):
        self._descriptor = descriptor

    @property
    def descriptor(self) -> 'ReturnDescriptor':
        return self._descriptor

    def apply(self, params: Params, graph: 'Graph') -> Record:
        record = {}
        for descriptor in self._descriptor.records:
            if descriptor.variable not in params:
                raise ValueError("Variable '%s' not defined" % descriptor.variable)

            if descriptor.name:
                key = descriptor.name
            elif descriptor.property:
                key = '.'.join([descriptor.variable, descriptor.name])
            else:
                key = descriptor.variable

            value = params[descriptor.variable]
            if descriptor.property:
                value = value.get_property(descriptor.property)

            record[key] = value

        return record
