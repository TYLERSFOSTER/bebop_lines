"""
Test ./src/bebop_lines/solvers/conv_match.py
"""
from __future__ import annotations

import random

import torch
import pytest

import bebop_lines.group_action as grp
import bebop_lines.melody as line
import bebop_lines.solvers as sol


TEST_KERNEL = torch.zeros((128, 8))
TEST_KERNEL[127, 0] = TEST_KERNEL[126, 1]= 1.0

TEST_KERNEL_B = torch.zeros((128, 8))
for k in range(8):
    TEST_KERNEL_B[127 - k, 7 - k] = 1.0

TEST_KERNEL_C = torch.zeros((128, 8))
for k in range(8):
    TEST_KERNEL_C[127 - k, k] = (-1)**k * 1.0

TEST_KERNEL_Z = torch.ones((128, 8))


@pytest.mark.parametrize("number_of_elements, idx_shift, value_shift, kernel_list, answer", 
    [
        (8, 0, 0, [TEST_KERNEL_Z], 17.0),
    ]
)
def test_MotionAnalyzer(
    number_of_elements : int,
    idx_shift : int,
    value_shift : int,
    kernel_list : list[torch.Tensor],
    answer,
) -> None:
    """Test that proj_to_degree returns expected values"""
    group = grp.PermutationGroup(number_of_elements)

    bars = [line.PermutationBar(
        group[random.randrange(0, number_of_elements)],
        1,
        number_of_elements - 1,
        idx_shift + 2 * k,
        value_shift) for k in range(4)]

    phrase = line.PermutationPhrase(bars)
    
    analyzer = sol.MotionAnalyzer(kernel_list, threshhold=0.0) # type: ignore
    analysis = analyzer(phrase)

    assert analysis == answer