from __future__ import annotations

import math

import pytest

import bebop_lines.group_action as grp
import bebop_lines.melody.bars as bars


@pytest.mark.parametrize("permutation_group", 
  [grp.PermutationGroup(n) for n in range(5, 7)],
)
@pytest.mark.parametrize("start_idx", 
  [n for n in range(0, 2)],
)
def test_PermutationBar__init(permutation_group, start_idx):
  for permutation in permutation_group:
    bar = bars.PermutationBar(permutation, start_idx, start_idx + 2, 0, 0)

    assert bar.permutation_group.number_of_elements == permutation_group.number_of_elements
    assert bar.start_idx == start_idx
    assert bar.end_idx == start_idx + 2


@pytest.mark.parametrize("permutation_group", 
  [grp.PermutationGroup(n) for n in range(5, 7)],
)
@pytest.mark.parametrize("start_idx", 
  [n for n in range(0, 2)],
)
def test_PermutationBar_change_bounds(permutation_group, start_idx):
  for permutation in permutation_group:
    bar = bars.PermutationBar(permutation, start_idx, start_idx + 1, 0, 0)

    bar.change_bounds(0, permutation_group.number_of_elements - 1)

    assert bar.start_idx == 0
    assert bar.end_idx == permutation_group.number_of_elements - 1


@pytest.mark.parametrize("permutation_group", 
  [grp.PermutationGroup(n) for n in range(4, 6)],
)
@pytest.mark.parametrize("start_idx", 
  [n for n in range(0, 2)],
)
@pytest.mark.parametrize("value_shift", 
  [n for n in range(-2, 3)],
)
@pytest.mark.parametrize("tonic_degree", 
  [n for n in range(55, 57)],
)
def test_PermutationBar__first_degree(permutation_group, start_idx, value_shift, tonic_degree):
  for permutation in permutation_group:
    bar = bars.PermutationBar(permutation, start_idx, start_idx + 2, 0, value_shift, tonic_degree=tonic_degree)

    assert bar.first_degree() == permutation[start_idx] + tonic_degree + value_shift