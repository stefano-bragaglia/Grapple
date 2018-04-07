class Rule(object):

    def __init__(self, pattern: 'Pattern', action: 'Action', salience: int = 0) -> None:
        self._pattern = pattern
        self._action = action
        self._salience = salience

    @property
    def salience(self) -> int:
        return self._salience

    @property
    def pattern(self) -> 'Pattern':
        return self._pattern

    @property
    def action(self) -> 'Action':
        return self._action

    def apply(self, params: 'Params') -> 'Record':
        return self._action.apply(params)
