from __future__ import annotations

import math

import pytest

import bebop_lines.group_action as grp
import bebop_lines.melody.bars as bars
import bebop_lines.melody.phrases as phrases


# @pytest.mark.parametrize("permutation_group", 
#   [grp.PermutationGroup(n) for n in range(5, 7)],
# )
# @pytest.mark.parametrize("start_idx", 
#   [n for n in range(0, 2)],
# )
# def test_PermutationBar__init(permutation_group, start_idx):
#   for permutation in permutation_group:
#     bar = bars.PermutationBar(permutation, start_idx, start_idx + 2, 0, 0)

#     assert bar.permutation_group.number_of_elements == permutation_group.number_of_elements
#     assert bar.start_idx == start_idx
#     assert bar.end_idx == start_idx + 2