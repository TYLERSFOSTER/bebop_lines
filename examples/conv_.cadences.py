from __future__ import annotations

import random

import torch

from bebop_lines.group_action.permutations import PermutationGroup
from bebop_lines.melody.bars import PermutationBar
from bebop_lines.melody.phrases import PermutationPhrase
from bebop_lines.solvers.conv_match import MotionAnalyzer


N = number_of_elements = 8

kernel = torch.zeros((8, 2))
kernel[0, 0] = 1.0
kernel[7, 1] = 1.0
print("KERNEL:", kernel)

kernel_list = [kernel]

group = PermutationGroup(number_of_elements)

for _ in range(50):
    perm_idx = random.randrange(0, len(group))
    permutation = group[perm_idx]
    print("PERMUTATION:", permutation)

    idx_shift = 0
    value_shift = 0 
    bars = [PermutationBar(
        permutation,
        1,
        number_of_elements - 1,
        idx_shift + 2 * k,
        value_shift
                                )
            for k in range(8)]

    phrase = PermutationPhrase(bars)
    print("PHRASE.DEGREE_PHRASE:", phrase.degree_phrase)
    analyzer = MotionAnalyzer(kernel_list, motion_weights=[1.0]) # type: ignore

    analysis = analyzer(phrase)
    print("ANALYSIS:", analysis)