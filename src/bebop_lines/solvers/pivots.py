"""
Tool for computing the local curvature in a melodic line
"""
from __future__ import annotations

def pivot_score(degree_list : list[int]) -> list[float]:
  """
  Given a list of integers (aka degrees), return a list of the same
  length, where the entry at index n measures the discrete curvature
  at index n in the original list of integers.

  Args
    `degree_list` : A list of integers

  Returns
    A list of integers measuring local curvature in input `degree_list`
  """
  assert len(degree_list) > 0

  degree_list = [degree_list[0]] + degree_list + [degree_list[-1]]

  pivot_score_list = []
  for idx in range(1, len(degree_list) - 1): # All degrees except first and last
    vel0 = degree_list[idx] - degree_list[idx - 1]
    vel1 = degree_list[idx + 1] - degree_list[idx]

    acc = vel1 - vel0
    abs_acc = abs(acc)
    pivot_score_list.append(abs_acc)

  return pivot_score_list


def to_midi_velocity(pivot_score_list : list[int]) -> list[int]:
  """
  Converts a list of integers into an appropriate list integer of MIDI velocities

  Args:
    pivot_score_list : A list of integers

  Returns
    List of integers between 0 and 127, representing MIDI note velocities
  """
  max_score = max(pivot_score_list)
  min_score = min(pivot_score_list)

  pivot_range = [min_score, max_score]
  pivot_delta = max_score - min_score

  midi_vol_list = [abs(int(64 + 63 * (pivot_score - min_score)/pivot_delta)) for pivot_score in pivot_score_list]

  return midi_vol_list
