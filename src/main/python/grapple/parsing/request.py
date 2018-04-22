from typing import Optional


class Selector(object):

    def __init__(self, var: str, field: str = None, tag: str = None):
        self._var = var
        self._field = field
        self._tag = tag

    @property
    def var(self) -> str:
        return self._var

    @property
    def field(self) -> Optional[str]:
        return self._field

    @property
    def tag(self) -> Optional[str]:
        return self._tag

    def get_name(self) -> str:
        if self._tag:
            return self._tag

        if self._field:
            return '%s.%s' % (self._var, self._field)

        return self._var
