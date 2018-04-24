from typing import Dict, List, Optional

from grapple.parsing.support.accessors import Accessor, AccessorList
from grapple.parsing.support.patterns import MatchPattern, PathPattern


class Rule(object):
    def __init__(self, rule: Dict[str, object]):
        self._description = rule['description'] if 'description' in rule and rule['description'] else None
        self._salience = rule['salience'] if 'salience' in rule and rule['salience'] else 0
        self._pattern = MatchPattern(rule['match'] if 'match' in rule and rule['match'] else [])
        self._accessors = AccessorList(rule['return']) if 'result' in rule and rule['result'] else []

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def salience(self) -> float:
        return self._salience

    @property
    def pattern(self) -> List[PathPattern]:
        return self._pattern.paths

    @property
    def accessors(self) -> List[Accessor]:
        return self._accessors
