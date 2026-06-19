from hypothesis import given, assume
from hypothesis import strategies as st
from clamp import clamp

def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(15, 0, 10) == 10
    assert clamp(-5, 0, 10) == 0

@given(st.integers(), st.integers(), st.integers())
def test_clamp_always_within_bounds(x, lo, hi):
    assume(lo <= hi)
    res = clamp(x, lo, hi)
    assert lo <= res <= hi

def test_clamp_logic_branches():
    assert clamp(5, 10, 20) == 10

@given(st.lists(st.integers(), min_size=3, max_size=3).map(sorted))
def test_clamp_identity_inside_bounds(values):
    # 'values' este mereu o listă de 3 elemente deja sortate crescător
    lo, x, hi = values
    assert clamp(x, lo, hi) == x

def test_clamp_boundary_explicit():
    assert clamp(2, 2, 5) == 2