import pytest
from game.plate.fragment import find_glue_side


def test_simple_adjacent():
    a1 = [True] + [False] * 7
    a2 = [False, True] + [False] * 6
    assert find_glue_side(a1, a2) == (False, True)


def test_wrap_around_adjacent():
    a1 = [False] * 7 + [True]
    a2 = [True] + [False] * 7
    assert find_glue_side(a1, a2) == (False, True)


def test_both_sides():
    a1 = [True] + [False] * 7
    a2 = [False] * 8
    a2[7] = True
    a2[1] = True
    assert find_glue_side(a1, a2) == (True, True)


def test_no_glue_when_other_absent():
    a1 = [True] + [False] * 7
    a2 = [False] * 8
    assert find_glue_side(a1, a2) == (False, False)


def test_contiguous_run_right():
    a1 = [False, True, True] + [False] * 5
    a2 = [False] * 8
    a2[3] = True
    assert find_glue_side(a1, a2) == (False, True)
