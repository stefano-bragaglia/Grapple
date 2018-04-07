from typing import Optional, List, Union, Dict

Value = Union[bool, int, float, str, List[bool], List[int], List[float], List[str]]


class Container(object):

    def __init__(self):
        self._properties = {}

    @property
    def keys(self) -> List[str]:
        return list(self._properties.keys())

    def get_properties(self, keys: List[str] = None) -> Dict[str, Value]:
        if keys is None:
            keys = list(self._properties.keys())

        return {key: self._properties[key] for key in keys if key in self._properties}

    def has_property(self, key: str) -> bool:
        return key in self._properties

    def get_property(self, key: str, default: Value = None) -> Optional[Value]:
        if key not in self._properties:
            return default

        return self._properties[key]

    def set_property(self, key: str, value: Value):
        if value:
            self._properties[key] = value

        elif key in self._properties:
            self._properties.pop(key)

    def remove_property(self, key: str) -> Optional[Value]:
        if key in self._properties:
            return self._properties.pop(key)
