from __future__ import annotations

import random

import torch

from bebop_lines.group_action.permutations import PermutationGroup
from bebop_lines.melody.bars import PermutationBar
from bebop_lines.melody.phrases import PermutationPhrase
from bebop_lines.solvers.conv_match import MotionAnalyzer
from bebop_lines.solvers.key_match import Scale
from bebop_lines.print_sound.midi import save_midi


N = number_of_elements = 8

kernel_0 = kernel_2 = kernel_4 = torch.zeros((8, 2))
kernel_0[0, 0] = kernel_2[0, 0] = kernel_4[0, 0] = 1.0
kernel_0[7, 1] = kernel_2[5, 1] = kernel_4[4, 1] = 1.0

kernel_1 = kernel_0[:, [1, 0]]
kernel_3 = kernel_2[:, [1, 0]]
kernel_5 = kernel_4[:, [1, 0]]

kernel_list = [
    kernel_0,
    kernel_1,
    kernel_2,
    kernel_3,
    kernel_4,
    kernel_5,
]

group = PermutationGroup(number_of_elements)

for _ in range(50):
    perm_idx = random.randrange(0, len(group))
    permutation = group[perm_idx]
    # print("\nPERMUTATION:", permutation)

    idx_shift = 0
    value_shift = 0 
    bars = [PermutationBar(
        permutation,
        1,
        number_of_elements - 1,
        idx_shift + 2 * k,
        value_shift + 2 * k
                                )
            for k in range(8)]

    phrase = PermutationPhrase(bars)
    
    analyzer = MotionAnalyzer(kernel_list, motion_weights=[1.0]) # type: ignore

    analysis = analyzer(phrase)

    # print("ANALYSIS:", analysis)

    degree_list = [0, 4, 5, 7]
    scale = Scale(degree_list, repeat_mod_12=True)

    matching_score = scale.dot(phrase)

    # print("MATCHING_SCORE:", matching_score)

    if matching_score >= 37.0 and analysis >= 24.0:
        save_midi(phrase, use_curve_amplitude=True)