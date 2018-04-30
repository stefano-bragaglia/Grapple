from typing import List, Optional


class ReturnItem(object):

    def __init__(self, variable: str = None):
        self._variable = variable

    @property
    def variable(self) -> Optional[str]:
        return self._variable


class ReturnPart(object):
    def __init__(self, distinct: bool = False, result_items: List[dict] = None, skip: int = 0, limit: int = -1):
        self._distinct = distinct
        self._return_items = [ReturnItem(**result_item) for result_item in result_items] if result_items else []
        self._skip = skip
        self._limit = limit

    def __getitem__(self, index: int) -> ReturnItem:
        return self._return_items[index]

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def items(self) -> List(ReturnItem):
        return self._return_items

    @property
    def skip(self) -> int:
        return self._skip

    @property
    def limit(self) -> int:
        return self._limit


if __name__ == '__main__':
    example = {
        "return": {
            "distinct": True,
            "return_items": [],
            "order_by": [
                {}
            ],
            "skip": 0,
            "limit": -1
        }
    }
