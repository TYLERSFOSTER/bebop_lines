from __future__ import annotations

import math


def pivot_score(degree_list : list[int]) -> list[float]:
  degree_list = [degree_list[0]] + degree_list + [degree_list[-1]]

  pivot_score_list = []
  for idx in range(1, len(degree_list) - 1): # All degrees except first and last
    vel0 = degree_list[idx] - degree_list[idx - 1]
    vel1 = degree_list[idx + 1] - degree_list[idx]

    acc = vel1 - vel0
    abs_acc = math.abs(acc)
    pivot_score_list.append(abs_acc)

  return pivot_score_list


def to_midi_vol(pivot_score_list : list[int]) -> list[int]:
  pass


