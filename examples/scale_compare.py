"""
Generate and export a MIDI file of a melodic phrase using permutation-based bars.

This script constructs a melodic phrase from a randomly chosen permutation in a specified
permutation group. Each bar in the phrase is created from the same permutation, but with
different start indices and onset times. The resulting phrase is exported as a MIDI file,
with note velocities determined by the curvature of the phrase.

Dependencies:
  - bebop_lines.group_action : for generating permutation groups
  - bebop_lines.melody       : for defining melodic bars and phrases based on permutations
  - bebop_lines.print_sound.midi : for saving the melodic phrase as a MIDI file
"""
from __future__ import annotations

import math
import random

import tqdm

import bebop_lines.group_action as grp
import bebop_lines.melody as line
import bebop_lines.solvers as sol
import bebop_lines.print_sound.midi as midi

# Define the number of elements in the permutation group
N = number_of_elements = 8
group = grp.PermutationGroup(number_of_elements)

for _ in tqdm.tqdm(range(100)):
  # Randomly choose one permutation from the group
  sample_idx = random.choice(list(range(math.factorial(number_of_elements))))
  permutation = group[sample_idx]
  reversed_permutation  = [permutation[N-i] for i in range(1, N+1)]

  # Construct a list of PermutationBar objects using the selected permutation
  bars = [line.PermutationBar(
    reversed_permutation,
    k,
    k+5,
    0,
    abs(4-k),
    duration_list=[2, 1, 2, 1, 2, 1, 2, 1],
                              )
          for k in range(0, number_of_elements, 2)
          ]
  phrase = line.PermutationPhrase(bars)

  degree_list = [0, 4, 5, 7]

  scale = sol.Scale(degree_list, repeat_mod_12=True)

  matching_score = scale.dot(phrase)

  if matching_score > 65.0:
    print("MATCHING_SCORE:", matching_score)
    midi.save_MIDI(phrase, use_curve_amplitude=True)

