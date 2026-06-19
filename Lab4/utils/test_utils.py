import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
from utils import clamp, merge_sorted, parse_pair, unique_sorted

def test_clamp():
    assert clamp(5, 0, 10) == 5

def test_merge_sorted():
    assert merge_sorted([1, 3], [2, 4]) == [1, 2, 3, 4]

def test_parse_pair():
    assert parse_pair("1:2") == (1, 2)
    with pytest.raises(ValueError):
        parse_pair("hello")

def test_unique_sorted():
    assert unique_sorted([1, 1, 1]) == [1]

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a

@given(st.integers(), st.integers(), st.integers())
def test_clamp_in_bounds(x, lo, hi):
    assume(lo <= hi)
    res = clamp(x, lo, hi)
    assert lo <= res <= hi

@given(st.lists(st.integers()).map(sorted), st.lists(st.integers()).map(sorted))
def test_merge_sorted_hypothesis(a, b):
    res = merge_sorted(a, b)
    assert res == sorted(a + b)