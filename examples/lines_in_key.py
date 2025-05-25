
from __future__ import annotations

import tqdm

import numpy as np

import bebop_lines.group_action as grp
import bebop_lines.solvers as sol
import bebop_lines.melody as line
import bebop_lines.print_sound.midi as midi

# Define the number of elements in the permutation group
number_of_elements = 9
group = grp.PermutationGroup(number_of_elements)

# Define the "key" by defining a Scale instnace
scale_degrees = [0, 4, 5, 7, 11]
scale_degree = [69 + degree for degree in scale_degrees]
degree_weights = [0 for _ in range(69)] + [1, 0, 0, 0, 1/5, 1/3, 0, 1/3, 0, 0, 0, 1/7] + [0 for _ in range(69+12,128)]
scale = sol.Scale(scale_degrees, repeat_mod_12=True, degree_weights=np.array(degree_weights))

# Collect and save permutations with pivots matching key degrees sufficiently well
all_scores = []
for idx in tqdm.tqdm(range(len(group))):
  permutation = group[idx]
  bar = line.PermutationBar(permutation, 0, len(permutation), 0, 0, permutation_group=group)
  phrase = line.PermutationPhrase([bar])

  present_score = float(scale.dot(phrase))

  all_scores.append(present_score)

  if present_score > 80.0:
    midi.save_midi(phrase, use_curve_amplitude=True)