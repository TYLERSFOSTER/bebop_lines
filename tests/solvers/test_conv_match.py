"""
Test ./src/bebop_lines/solvers/conv_match.py
"""
from __future__ import annotations

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


@pytest.mark.parametrize("number_of_elements, idx_shift, value_shift, kernel_list, answer", 
    [
        (8, 0, 0, [TEST_KERNEL], 2.0),
        (8, 0, 0, [2 * TEST_KERNEL], 4.0),
        (8, 0, 0, [TEST_KERNEL_B], 8.0),
        (8, 0, 0, [TEST_KERNEL_C], 0.0),
        (8, 0, 0, [TEST_KERNEL, 2 * TEST_KERNEL, TEST_KERNEL_B, TEST_KERNEL_C], 14.0),
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
    print("MotionAnalyzer.motion_instances:", analyzer.motion_instances)

    analysis = analyzer(phrase)
    print("ANALYSIS:", analysis)

    assert analysis == answer