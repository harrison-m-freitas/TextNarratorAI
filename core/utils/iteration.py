from typing import Iterable, List, TypeVar

Item = TypeVar("Item")


def chunk_list(items: List[Item], size: int) -> Iterable[List[Item]]:
    """
    Divide uma lista em chunks de tamanho `size`.
    """
    for i in range(0, len(items), size):
        yield items[i : i + size]
