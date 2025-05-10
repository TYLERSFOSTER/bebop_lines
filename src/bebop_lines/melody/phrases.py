from __future__ import annotations

import math

import bebop_lines.group_action as ga
from bebop_lines.melody.bars import PermutationBar


class PermutationPhrase():
  def __inti__(self, bars_list : list[PermutationBar]):
    assert isinstance(bars_list, list)
    for entry in bars_list:
      assert isinstance(entry, PermutationBar)

    self.bars_list = bars_list
    self.permutations_list = [bar.permutation for bar in bar_list]
    
    degree_phrase = []
    duration_phrase = []
    barline_degrees = []
    for k, bar in enumerate(self.bars_list):
        barline_degrees.append(k)

        degree_list, duration_list = bar.print_line()

        degree_phrase = degree_phrase + degree_list
        duration_phrase = duration_phrase + duration_list
    self.barline_degrees = barline_degrees
    self.degree_phrase = degree_phrase
    self.duration_phrase = duration_phrase
