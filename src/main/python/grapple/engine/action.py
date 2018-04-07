from grapple.engine.activation import Params

Record = Params


class Action(object):

    def __init__(self, pattern: 'Pattern') -> None:
        self._pattern = pattern

    @property
    def pattern(self) -> 'Pattern':
        return self._pattern

    def apply(self, params: Params) -> Record:
        raise NotImplementedError()
