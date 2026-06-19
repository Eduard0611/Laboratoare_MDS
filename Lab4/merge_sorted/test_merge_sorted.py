from merge_sorted import merge_sorted

def test_merge_sorted_static():
    assert merge_sorted([1, 3], [2, 4]) == [1, 2, 3, 4]
    assert merge_sorted([], [1]) == [1]

def test_merge_sorted_stability():
    assert merge_sorted([1, 1], [1, 1]) == [1, 1, 1, 1]

def test_kill_mutant_7():
    assert merge_sorted([1, 2], [3, 4]) == [1, 2, 3, 4]