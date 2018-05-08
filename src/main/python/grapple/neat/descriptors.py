from typing import Optional


class RuleDesc(object):
    def __init__(self, description: str, salience: int):
        self._description = description
        self._salience = salience

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def salience(self) -> int:
        return self._salience


class Something(object):

    def __init__(self, skip: int, limit: int):
        self._skip = skip
        self._limit = limit

    @property
    def skip(self) -> int:
        return self._skip

    @property
    def limit(self) -> int:
        return self._limit