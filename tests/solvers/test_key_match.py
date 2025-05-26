"""
Test ./src/bebop_lines/solvers/key_match.py
"""
from __future__ import annotations

import random

import numpy as np
import pytest

import bebop_lines.group_action as grp
import bebop_lines.melody as line
import bebop_lines.solvers as sol


@pytest.mark.parametrize("number_of_elements", list(range(5, 8)))
@pytest.mark.parametrize("idx_shift", [0, 1, 2])
@pytest.mark.parametrize("value_shift", list(range(-5, 5)))
def test_proj_to_degree(
    number_of_elements : int,
    idx_shift : int,
    value_shift : int
) -> None:
    """Test that proj_to_degree returns expected values"""
    group = grp.PermutationGroup(number_of_elements)
    permutation = group[number_of_elements//2]

    bars = [line.PermutationBar(
        permutation,
        1,
        number_of_elements - 1,
        idx_shift + 2 * k,
        value_shift
                                )
            for k in range(4)]

    phrase = line.PermutationPhrase(bars)

    char_vector = sol.proj_to_degree(phrase)
    
    assert char_vector.shape == (128,)


@pytest.mark.parametrize("repeat_mod_12", [True, False])
def test_scale__init(repeat_mod_12 : bool) -> None:
    """Test that Scale.__init__ produces class with expected attributes"""
    degree_list = []
    for _ in range(30):
        value = random.choice(list(range(128)))
        degree_list.append(value)

    scale = sol.Scale(degree_list, repeat_mod_12=repeat_mod_12)

    assert isinstance(scale, sol.Scale)
    assert scale.char_vector.shape == (128,)
    assert scale.repeat_mod_12 == repeat_mod_12
    if not repeat_mod_12:
        assert scale.degree_list == degree_list


@pytest.mark.parametrize("number_of_elements", list(range(5, 7)))
@pytest.mark.parametrize("idx_shift", [0, 1])
@pytest.mark.parametrize("value_shift", list(range(-2, 2)))
@pytest.mark.parametrize("repeat_mod_12", [True, False])
def test_scale__dot(
    number_of_elements : int,
    idx_shift : int,
    value_shift : int,
    repeat_mod_12 : bool
) -> None:
    """Test that Scale.dot returns expected values"""
    group = grp.PermutationGroup(number_of_elements)
    permutation = group[number_of_elements//2]

    bars = [line.PermutationBar(
        permutation,
        1,
        number_of_elements - 1,
        idx_shift + 2 * k,
        value_shift
                                )
            for k in range(4)]

    phrase = line.PermutationPhrase(bars)

    degree_list = []
    for k in range(30):
        value = random.choice(list(range(128)))
        degree_list.append(value)

    scale = sol.Scale(degree_list, repeat_mod_12=repeat_mod_12)

    matching_score = scale.dot(phrase)/len(phrase)

    assert isinstance(matching_score, float)
    assert 0<= matching_score
