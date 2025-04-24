import pytest
from core.utils.iteration import chunk_list
    
def test_chunk_list_basic():
    assert list(chunk_list([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(chunk_list([1, 2, 3], 2)) == [[1, 2], [3]]
    assert list(chunk_list([1], 2)) == [[1]]
    assert list(chunk_list([], 3)) == []

@pytest.mark.parametrize("items,size,expected", [
    ([1, 2, 3, 4, 5, 6], 3, [[1, 2, 3], [4, 5, 6]]),
    ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
    ([1, 2, 3], 10, [[1, 2, 3]]),
    ([], 1, []),
    (["a", "b", "c", "d"], 3, [["a", "b", "c"], ["d"]]),
])
def test_chunk_list_parametrized(items, size, expected):
    assert list(chunk_list(items, size)) == expected
