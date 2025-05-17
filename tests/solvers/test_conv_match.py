"""
Test ./src/bebop_lines/solvers/con_match.py
"""
from __future__ import annotations

import random

import numpy as np
import torch
import pytest

import bebop_lines.group_action as grp
import bebop_lines.melody as line
import bebop_lines.solvers as sol


@pytest.mark.parametrize("number_of_elements", list(range(5, 7)))
@pytest.mark.parametrize("idx_shift", [0, 1, 2])
@pytest.mark.parametrize("value_shift", list(range(-3, 3)))
@pytest.mark.parametrize("kernel_list", 
    [
        [
            torch.rand((2, 2)),
            torch.rand((3, 3)),
            torch.rand((4, 4)),
         ]
    ]
)
def test_MotionAnalyzer(
    number_of_elements : int,
    idx_shift : int,
    value_shift : int,
    kernel_list : list[torch.Tensor],
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

    analyzer = sol.MotionAnalyzer(kernel_list) # type: ignore

    analysis = analyzer(phrase)
    print("ANALYSIS:", analysis)

    assert False