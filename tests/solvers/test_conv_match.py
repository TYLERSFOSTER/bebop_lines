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


TEST_KERNEL = torch.zeros((8, 128))
TEST_KERNEL[0, 127] = TEST_KERNEL[1,126]= 1.0


@pytest.mark.parametrize("number_of_elements, idx_shift, value_shift, kernel_list", 
    [
        (8, 0, 0, [TEST_KERNEL]),
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
    phrase.degree_phrase = [127, 126, 125, 124, 123, 122, 121, 120]
    

    analyzer = sol.MotionAnalyzer(kernel_list, motion_weights=[1.0]) # type: ignore

    analysis = analyzer(phrase)
    print("ANALYSIS:", analysis)

    assert False